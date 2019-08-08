#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from google.cloud import translate_v3beta1 as translate
import os
import requests
import json
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
KEY = "trnsl.1.1.20190808T044353Z.19212738127dc09d.6f794cd378e0669b093fa25b8f40bd6dbd70e092" #Это ваш API ключ
KEY_D = "dict.1.1.20190808T045857Z.77910a1ccc278937.2825356947febae0705673b0abcb77eaadfcd9cf"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="E:\\WORK\\untitled1\\key2.json"


client = translate.TranslationServiceClient()
location = 'global'
project_id = 'my-project-1565201444391'

parent = client.location_path(project_id, location)

def trans(text):

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code="en",
        target_language_code="ru")

    print(response)
    for translation in response.translations:
        print('Translated Text: {}'.format(translation))

    return response.translations[0]
def correct_word(text):

    params = {

        "text": text,
        #"lang": 'en-ru'  #Здесь мы указываем с какого языка на какой мы делаем переводим
    }
    response = requests.get("https://speller.yandex.net/services/spellservice.json/checkText" ,params=params)
    print(response.json())
    if len(response.json())!=0:
        return  response.json()[0]["s"][0]
    else:
        return text
def translate_me(mytext):

    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'  #Здесь мы указываем с какого языка на какой мы делаем переводим
    }
    response = requests.get(URL ,params=params)
    return response.json()

def yandexT(text):
    json = translate_me(text)
    print(json)
    return ''.join(json["text"])

def yandexD(text):
    params = {
        "key": KEY_D,
        "text": text,
        "lang": 'en-ru'  # Здесь мы указываем с какого языка на какой мы делаем переводим
    }
    response = requests.get("https://dictionary.yandex.net/api/v1/dicservice.json/lookup", params=params)
    print(response.json())
    todos = json.loads(response.text)
    if(len(todos["def"])>0):
        print(todos["def"][0]["tr"])

        result = []
        for item in todos["def"][0]["tr"]:
            result.append(item["text"])
            if("syn" in item):
                for syn in item["syn"]:
                    result.append(syn["text"])
            print(item["text"])



        return result
    else:
        return []
#print(correct_word("admission"))

#print(str(trans("python")))