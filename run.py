# run.py
# This script is a dedicated entry point for PyInstaller.
# It uses an absolute import to allow the packaged executable to find the 'src' package.

from src.main import main

if __name__ == '__main__':
    main()
