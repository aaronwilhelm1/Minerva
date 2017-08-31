artFolderName = "articles/"
artFileEnding = ".art"
wlFolderName = "wordlists/"
wlFileEnding = ".wl"
read_display_intro = u"Words highlighted in gold are new words. Words highlighted in blue are words in the Learning List\u00ae.\n\n" \
    + u"Left click on a word on the left to display its definition here.\nIf you want, edit the definition and then click \"Add/Save\" to add it to your Learning List.\n\n" \
    + u"If you have already saved an alternate defintion but want to see the original translation, click \"Refetch\". To save the word with the original translation, then hit \"Add/Save\".\n\n" \
    + u"Finally, right click on a word to toggle it between a known word and a word in the Learning List\u00ae."
languages = ["German", "French", "Spanish"]
# The language codes for each of the above language options. Note that they are little weird since they are the Yandex Translate codes
languageCodes = ["de", "fr", "es"]


def translate_error_message(word):
    return (word + "\n   1.) " + word + " [Could not find a definition. Feel free to write your own.]")


def have_not_translated_message(word):
    return ("A translation for \"" + word + "\" was never fetched.\nFetch one using the \"Refetch\" button below or type in your own definition.\n"
            + "To then save that translation click the \"Add/Save\" button.")
