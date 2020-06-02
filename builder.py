import subprocess
from pathlib import Path
from typing import List
import zipfile
import configparser
from loguru import logger


class Builder(object):

    """
    https://pyinstaller.readthedocs.io/en/stable/usage.html
    """
    def __init__(self):
        self.main: str = 'main'
        self.name: str = 'ee'
        self.dist: str = './'
        self.temp: str = 'temp'

        self.option: List[str] = [
            'pyinstaller',
            '%s.py' % self.main,
            '-F',
            # '--clean',
            '--distpath=%s' % self.dist,
            '--specpath=%s' % self.temp,
            '--workpath=%s' % self.temp,
            '--name=%s' % self.name,
        ]

        self.hiddenImports: List[str] = [
            'uvicorn.loops',
            'uvicorn.loops.auto',
            'uvicorn.protocols',
            'uvicorn.protocols.http',
            'uvicorn.protocols.http.auto',
            'uvicorn.protocols.websockets',
            'uvicorn.protocols.websockets.auto',
            'uvicorn.lifespan',
            'uvicorn.lifespan.on',
            # 'uvicorn.logging',
        ]

        for h in self.hiddenImports:
            self.option.append('--hidden-import=%s' % h)  # なんでやねん!?

        subprocess.call(args=self.option)


if __name__ == '__main__':
    builder = Builder()
