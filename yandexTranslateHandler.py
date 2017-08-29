import requests


dictionaryUrl = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
dictionaryKey = "dict.1.1.20170823T200338Z.d66eba1c8ea121ff.d8d6268f2c83d0d80e2dd4a98cac17bbe936dcd6"
translateUrl = "https://translate.yandex.net/api/v1.5/tr.json/translate"
translateKey = "trnsl.1.1.20170823T182626Z.f5a3113f7a4ee957.6d70c86f561411cc055b9bfb0666d8433c2afaf7"


# slang and elang need to be in the two character language code that Yandex specifies
# returns an object where it is [every part of speech(word, [defs[synonyms for that def]], part of speech, gen, num)]
# note that gen and num may not be supplied (e.g. if not a noun or if the translator API had to be used)
def getTranslation(text, slang, elang):
    langCode = slang + "-" + elang
    results = checkDictionary(text, langCode)
    if len(results) == 0:
        results = checkTranslator(text, langCode)
    return results


def checkDictionary(text, langCode):
    parameters = {"key": dictionaryKey, "lang": langCode, "text": text}
    response = requests.get(dictionaryUrl, params=parameters)
    data = response.json()
    definitions = []
    for type in range(len(data["def"])):
        typeDefs = []
        for x in data["def"][type]["tr"]:
            synonyms = []
            synonyms.append(x["text"])
            if "syn" in x:
                for syn in x["syn"]:
                    synonyms.append(syn["text"])
            typeDefs.append(synonyms)
        definitions.append((data["def"][type]["text"], typeDefs, data["def"][type]["pos"], data["def"][type].get("gen"), data["def"][type].get("num")))
    return definitions


def checkTranslator(text, langCode):
    parameters = {"key": translateKey, "lang": langCode, "text": text}
    response = requests.get(translateUrl, params=parameters)
    data = response.json()
    definitions = []
    # Yandex will return the input text if it couldn't translate it.
    # This means that we could be throwing out translations where the words are actually the same, but they have no way around it.
    # However, this is unlikely as priority is given to the dictionary, which should detect that same-word translations.
    if text != data.get("text")[0]:
        definitions.append((text, [data.get("text")], None, None, None))
    return definitions

# print(checkDictionary("gibberish", "de-en"))
# print(checkTranslator("gibberish", "de-en"))
