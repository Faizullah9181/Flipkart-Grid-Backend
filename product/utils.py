from bardapi import BardCookies
import requests

cookie_dict = {
   "YOUR KEY": "YOUR VALUE"
}

bard = BardCookies(cookie_dict=cookie_dict)


def getMainContent(req):
    return req['content']


def getImages(req):
    return req['images']


def getDetails(req):
    content = getMainContent(req)
    res = {}
    res['content'] = content
    res['content'] = res['content'].replace('\n', '')
    res['content'] = res['content'].replace('**', '')
    res['content'] = res['content'].replace('[', '')
    res['content'] = res['content'].replace(']', '')
    res['content'] = res['content'].replace('*', '')
    res['content'] = res['content'].replace('`', '')
    res['content'] = res['content'].replace('>', '')
    res['content'] = res['content'].replace('`', '')
    res['content'] = res['content'].replace('\'', '')
    res['content'] = res['content'].replace('\"', '')
    res['content'] = res['content'].replace('(', '')
    res['content'] = res['content'].replace(')', '')
    res['content'] = res['content'].split(':')

    return res


def getImagesFromBard(req):
    images = getImages(req)
    res = {}
    res['images'] = images
    return res


def strUtiltext(str):
    data = bard.get_answer(str)
    return getDetails(data)


def strUtilimage(str):
    data = bard.get_answer(str)
    return getImagesFromBard(data)

def get_details(prompt,engine):
    url = "yourllmapiurl"+engine
    payload ={
        "prompt": prompt
    }
    response = requests.post(url, json=payload)
    data = response.json()
    data = data['content']
    return data