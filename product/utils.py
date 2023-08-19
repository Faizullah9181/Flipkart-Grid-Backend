from bardapi import BardCookies
import requests

cookie_dict = {
    "__Secure-1PSID": "ZgjPlYPjnGfpkX8GCuwGNwnr-8jJn6jjZwxi-ho7Mp6mmh8xCqfwP-tpBxVgn8PN_xA9tg.",
    "__Secure-1PSIDTS": "sidts-CjEBSAxbGZdA3FoFlZsABiaKhyCBuykPkuKhQ1FQEAJKwpgho45-eCGkaZI5JtTZkOKsEAA"
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

# https://tg-api-zehr.onrender.com/api/v1/llmodels/bai


def get_details(prompt):
    url = "https://tg-api-zehr.onrender.com/api/v1/llmodels/bai"
    payload ={
        "prompt": prompt
    }
    response = requests.post(url, json=payload)
    data = response.json()
    data = data['content']
    return data
