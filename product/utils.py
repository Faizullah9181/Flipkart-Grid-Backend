from bardapi import BardCookies
import requests

cookie_dict = {
    "__Secure-1PSID": "ZAjvGgqx4zAG7KQlHaBRC4c61hOdgfIzr-wUjYoUZn1LDMldXvIXSlFb_pUt49YSTtIHwQ.",
    "__Secure-1PSIDTS": "sidts-CjIBSAxbGWETevrjlsjtrxTO7OFB1vyQL0TslROI1J55qXzq54aYA7JDeM1RRNJ1WaeoxxAA"
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
    res['content'] = res['content'].split(':')[1]

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




