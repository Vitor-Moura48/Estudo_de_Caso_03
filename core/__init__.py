import sys
import os
from PyQt6 import QtCore, QtGui, QtWidgets, QtWebChannel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import *
from PyQt6.QtCore import QUrl
import socket

from core.util import resource_path

DEBUG_PORT = '5588'
DEBUG_URL = f'http://127.0.0.1:{DEBUG_PORT}'
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT

class ApplicationThread(QtCore.QThread):
    def __init__(self, application, port=5000):
        super(ApplicationThread, self).__init__()
        self.application = application
        self.port = port

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(port=self.port, threaded=True)


class WebPage(QWebEnginePage):
    def __init__(self, root_url):
        super(WebPage, self).__init__()
        self.root_url = root_url

    def home(self):
        self.load(QtCore.QUrl(self.root_url))

    def acceptNavigationRequest(self, url, kind, is_main_frame):
        ready_url = url.toEncoded().data().decode()
        is_clicked = kind == self.NavigationType.NavigationTypeLinkClicked
        if is_clicked and self.root_url not in ready_url:
            QtGui.QDesktopServices.openUrl(url)
            return False
        return super(WebPage, self).acceptNavigationRequest(url, kind, is_main_frame)

    def javaScriptAlert(self, securityOrigin, msg):

        icon = QtWidgets.QMessageBox.Icon.Warning
        title = "Aviso"

        # Verifica se a mensagem é um aviso, erro ou sucesso
        if msg.__contains__("Aviso:"):
            icon = QtWidgets.QMessageBox.Icon.Warning
            msg = msg.replace("Aviso:", "")
            title = "Aviso"
        if msg.__contains__("Erro:"):
            icon = QtWidgets.QMessageBox.Icon.Critical
            msg = msg.replace("Erro:", "")
            title = "Erro"
        elif msg.__contains__("Sucesso:"):
            icon = QtWidgets.QMessageBox.Icon.Information
            msg = msg.replace("Sucesso:", "")
            title = "Sucesso"

        msg_box = QtWidgets.QMessageBox()
        msg_box.setParent(self.parent())
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon(resource_path("appicon.png")))
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec()



def init_gui(application, port=0, width=800, height=600,
             window_title="Suricato", icon=resource_path("appicon.png"), router='splash', argv=None, inspector_mode=False):
    
    if argv is None:
        argv = sys.argv

    if port == 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()

    # Application Level
    qtapp = QtWidgets.QApplication(argv)
    webapp = ApplicationThread(application, port)
    webapp.start()
    qtapp.aboutToQuit.connect(webapp.terminate)

    # Main Window Level
    window = QtWidgets.QMainWindow()
    window.resize(width, height)
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)

    window.setWindowTitle(window_title)
    window.setWindowIcon(QtGui.QIcon(os.path.abspath(icon)))

    # WebView Level
    webView = QWebEngineView(window)

    webView.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    webView.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    webView.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)

    # Definir o caminho para o armazenamento local
    # webView.settings().setLocalStoragePath(os.path.abspath("database"))

    webView.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

    # # Remove o context menu
    # webView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    window.setCentralWidget(webView)

    # WebPage Level
    page = WebPage(f"http://localhost:{port}/{router}")
    page.home()
    webView.setPage(page)

    # Inspector Level
    if inspector_mode:
        inspector = QWebEngineView()
        inspector.setWindowTitle('Web Inspector')
        inspector.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        inspector.load(QtCore.QUrl("http://localhost:{}".format(DEBUG_PORT)))
        inspector.page().profile().setHttpUserAgent("Chrome/88.0.4324.182")
        inspector.setWindowIcon(QtGui.QIcon(resource_path("static/assets/webinspectoricon.png")))
        page.setDevToolsPage(inspector.page())
        inspector.show()

    window.show()
    return sys.exit(qtapp.exec())
