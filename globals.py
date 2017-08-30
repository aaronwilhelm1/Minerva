artFolderName = "articles/"
artFileEnding = ".art"
wlFolderName = "wordlists/"
wlFileEnding = ".wl"
languages = ["German", "Chinese", "Spanish"]
# The language codes for each of the above language options. Note that they are little weird since they are the Yandex Translate codes
languageCodes = ["de", "zh", "es"]


def translate_error_message(word):
    return (word + "\n   1.) " + word + " [Could not find a definition. Feel free to write your own.]")
