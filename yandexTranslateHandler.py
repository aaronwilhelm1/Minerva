import requests


baseUrl = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
key = "dict.1.1.20170823T200338Z.d66eba1c8ea121ff.d8d6268f2c83d0d80e2dd4a98cac17bbe936dcd6"


# slang and elang need to be in the two character language code that Yandex specifies
# returns an object where it is [every part of speech(word, [defs[synonyms for that def]], part of speech, gen, num)]
# note that gen and num may not be supplied (i.e. if not a noun)
def getTranslation(text, slang, elang):
    langCode = slang + "-" + elang
    parameters = {"key": key, "lang": langCode, "text": text}
    response = requests.get(baseUrl, params=parameters)
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


# print(getTranslation("steuern", "de", "en"))
