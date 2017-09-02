Minerva is a language learning tool to simplify reading texts in foreign languages and improve vocabulary aquisition.

Dependencies: Requests (HTTP for Humans), Unidecode

Check the builds directory for an executable for your machine. If not present, a build can be generated using PyInstaller once the necessary dependencies have been installed.

For Windows or Mac, execute the following command from within the project directory:
pyinstaller window.py -n Minerva -w -F

For Unix, execute the following command from within the project directory:
pyinstaller window.py -n Minerva -F

The generated executable should be runnable from any directory on your machine.