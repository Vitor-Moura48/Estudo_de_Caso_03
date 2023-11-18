import click

from flask import Flask
from core import init_gui

app = Flask(__name__)

from view.routes import *

@click.command()
@click.option('--inspector', is_flag=True, help='Enable debugging mode')
@click.option('--page', default='splash', help='Page to be loaded')

def suri_init(inspector, page):
    if page:
        print(f"\n=> Você requisitou a página: [/{page}] \n")

    init_gui(app, port=5200, router=page, window_title="Convenience Swap", inspector_mode=inspector)

if __name__ == '__main__':
    suri_init()
