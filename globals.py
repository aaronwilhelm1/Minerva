artFolderName = "articles/"
artFileEnding = ".art"
wlFolderName = "wordlists/"
wlFileEnding = ".wl"
read_display_intro = u"Words highlighted in gold are new words. Words highlighted in blue are words in the Learning List\u00ae.\n\n" \
    + u"Left click on a word on the left to display its definition here.\nIf you want, edit the definition and then click \"Add\" to add it to your Learning List.\n\n" \
    + u"If you have already saved an alternate defintion but want to see the original translation, click \"Refetch\". To save the word with the original translation, then hit \"Add\".\n\n" \
    + u"Finally, right click on a word to toggle it between a known word and a word in the Learning List\u00ae."
languages = ["German", "Chinese", "Spanish"]
# The language codes for each of the above language options. Note that they are little weird since they are the Yandex Translate codes
languageCodes = ["de", "zh", "es"]


def translate_error_message(word):
    return (word + "\n   1.) " + word + " [Could not find a definition. Feel free to write your own.]")


def have_not_translated_message(word):
    return ("A translation for \"" + word + "\" was never fetched. Fetch one using the button below or type in your own definition")
