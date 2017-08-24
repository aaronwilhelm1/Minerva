import requests


baseUrl = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
key = "dict.1.1.20170823T200338Z.d66eba1c8ea121ff.d8d6268f2c83d0d80e2dd4a98cac17bbe936dcd6"


# slang and elang need to be in the two character language code that Yandex specifies
# returns a 2D list where first list are the different definitions and the second lists are synonyms for that definition
def getTranslation(text, slang, elang):
    langCode = slang + "-" + elang
    parameters = {"key": key, "lang": langCode, "text": text}
    response = requests.get(baseUrl, params=parameters)
    data = response.json()
    definitions = []
    for x in data["def"][0]["tr"]:
        synonyms = []
        synonyms.append(x["text"])
        if "syn" in x:
            for syn in x["syn"]:
                synonyms.append(syn["text"])
        definitions.append(synonyms)
    return definitions


print(getTranslation("laufen", "de", "en"))
