from setuptools import setup

APP=['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'includes': ['bidict','certifi','chardet','cycler','idna','kiwisolver','matplotlib','numpy','Pillow','pyparsing','python-dateutil','python-engineio','python-socketio','requests','six','urllib3','websocket-client']
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=["py2app"],
)