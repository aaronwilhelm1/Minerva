# -*- coding: utf-8 -*-
import requests
import csv
from globals import deToEnDictionary


dictionaryUrl = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
dictionaryKey = "dict.1.1.20170823T200338Z.d66eba1c8ea121ff.d8d6268f2c83d0d80e2dd4a98cac17bbe936dcd6"
translateUrl = "https://translate.yandex.net/api/v1.5/tr.json/translate"
translateKey = "trnsl.1.1.20170823T182626Z.f5a3113f7a4ee957.6d70c86f561411cc055b9bfb0666d8433c2afaf7"

# dictionary is a dictionary of words/phrases mapped to lists, where each list contians all of the entries for that word
# first entry of list is a list of the translations for only that word
# second entry of list is a list of the translations for phrases that start with the word
dictionary = {}
with open(deToEnDictionary, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            words = row[0].split(' ')
            key = ''
            length = 0
            gender = ''
            for word in words:
                if len(word) != 0:  # some typos in the dictionary cause '' to be read as words...
                    if word[0] != '{':
                        key = key + word + ' '
                        length = length + 1
                    else:
                        gender = word.replace('{', "").replace('}', "")

            if words[0][-1] == '-':  # some words are in the form of 'Unterwasser-', so get rid of the '-'
                wordToAdd = words[0].lower()[:-1].decode('UTF-8')
            else:
                wordToAdd = words[0].lower().decode('UTF-8')
            if not (wordToAdd in dictionary):
                dictionary[wordToAdd] = [[] for x in range(2)]

            entry = row[:]  # make this row but add gender at end and make word not have def
            entry[0] = key.decode('UTF-8')
            for x in row[1:]:
                entry[row.index(x)] = x.decode('UTF-8')
            entry.append(gender)
            if length > 1:
                dictionary[wordToAdd][1].append(entry)
            else:
                dictionary[wordToAdd][0].append(entry)

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

    # First check for entries that are classified under that word, ignoring phrases
    definitions = []
    if text in dictionary:
        data = dictionary[text]
        for definition in data[0]:
            partOfSpeech = definition[-2]
            posIndex = -1
            if definition[-1] == "pl":
                gender = None
                plural = definition[-1]
            elif definition[-1] != "":
                gender = definition[-1]
                plural = None
            else:
                gender = None
                plural = None
            # see if we already have that part of speech (and if a noun, the same gender/plurality)
            for prevPos in definitions:
                if prevPos[2] == partOfSpeech and prevPos[3] == gender and prevPos[4] == plural:
                    posIndex = definitions.index(prevPos)
                    break
            if posIndex != -1:
                posGroup = definitions[posIndex]
                posGroup[1].append([definition[1]])
            else:
                definitions.append((definition[0], [[definition[1]]], partOfSpeech, gender, plural))

        # want to add some phrases as a) they're useful and b.) if the noun has multiple genders, it will be classified as a phrase
        # don't want to do it though as some words have more than 20 phrases
        if len(data[1]) <= 2:
            if(len(definitions) == 0):  # we have a phrase but no defs - try to get an actual definition first then
                definitions = checkTranslator(text, langCode)
            for phrase in data[1]:
                if phrase[-1] == "pl":
                    gender = None
                    plural = phrase[-1]
                elif phrase[-1] != "":
                    gender = phrase[-1]
                    plural = None
                else:
                    gender = None
                    plural = None
                definitions.append((phrase[0], [[phrase[1]]], phrase[-2], gender, plural))

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
