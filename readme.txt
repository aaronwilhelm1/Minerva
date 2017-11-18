Minerva is a language learning tool to simplify reading texts in foreign languages and improve vocabulary aquisition.

Dependencies: Requests (HTTP for Humans), Unidecode

Check the builds directory for an executable for your machine. If not present, a build can be generated using PyInstaller once the necessary dependencies have been installed.

To generate the build you will need to create a spec file for the executable. Right after the a variable is intialized, add the following line of code to add the german-to-english dictionary to the executable:
a.datas += [('./res/minerva_icon.ico', './res/minerva_icon.ico', 'DATA'), ('./res/deToEnDict.txt', './res/deToEnDict.txt', 'DATA')]

Additionally, within the exe variable initialization, define the following as well to set the icon:
icon='res\\minerva_icon.ico'

Then use the spec file to create the executable via PyInstaller. The generated executable should be runnable from any directory on your machine.

Note that word lists and articles will be stored in a Minerva folder created inside the user directory.