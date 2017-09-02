import os

rootDirectory = os.path.expanduser("~/Minerva/")
artFolderName = rootDirectory + "articles/"
artFileEnding = ".art"
wlFolderName = rootDirectory + "wordlists/"
wlFileEnding = ".wl"
resourceDirectory = "res/"
icoFile = resourceDirectory + "minerva_icon.ico"

import_hint = "Copy and paste an article into the \"Title\" and \"Text\" entries.\n\nAlso, be sure to set the language of the article from the drop down menu above.\n\n" \
    + "When finished, click the \"Add to Library\" button below to add it your reading library."

read_display_intro = u"Words highlighted in gold are new words. Words highlighted in blue are words in the Learning List\u00ae.\n\n" \
    + u"Left click on a word on the left to display its definition here.\nIf you want, edit the definition and then click \"Add/Save\" to add it to your Learning List.\n\n" \
    + u"If you have already saved an alternate defintion but want to see the original translation, click \"Refetch\". To save the word with the original translation, then hit \"Add/Save\".\n\n" \
    + u"Finally, right click on a word to toggle it between a known word and a word in the Learning List\u00ae.\n\n" \
    + u"Assuming nothing goes wrong, the word lists are automatically and periodically saved. However, for those who are paranoid, feel free to save at anytime with the \"Save\" button in the menu."
languages = ["German", "French", "Spanish"]
# The language codes for each of the above language options. Note that they are little weird since they are the Yandex Translate codes
languageCodes = ["de", "fr", "es"]


def translate_error_message(word):
    return (word + "\n   1.) " + word + " [Could not find a definition. Feel free to write your own.]")


def have_not_translated_message(word):
    return ("A translation for \"" + word + "\" was never fetched.\nFetch one using the \"Refetch\" button below or type in your own definition.\n"
            + "To then save that translation click the \"Add/Save\" button.")
