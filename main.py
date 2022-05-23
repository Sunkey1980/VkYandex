import yadisk
import requests
import json


# HS2AIwI9FbTrZ7Cpcjwg  a8a87daaa8a87daaa8a87daa5da8d4c75daa8a8a8a87daaca23154ed94ed1fe9890f718
# 552934290
# AQAAAABhgcB4AADLW9120MOiHUUKnkynmtWgB_k

def get_id():
    vk_id = input('Введите идентификатор пользователя VK ')
    url = 'https://vk.com/id' + vk_id
    if requests.get(url).status_code == 200:
        return vk_id
    else:
        print('Перепроверьте Id!')


def get_response(id):
    query = {'access_token': 'a8a87daaa8a87daaa8a87daa5da8d4c75daa8a8a8a87daaca23154ed94ed1fe9890f718',
             'owner_id': id, 'album_id': 'profile', 'extended': '1', 'photo_sizes': '1', 'v': '5.131'}
    responce = requests.get('https://api.vk.com/method/photos.get', params=query)
    data = responce.json()
    return data


def get_url(data):
    photo_dict = {}
    items = data['response']['items']
    for item in items:
        sizes = item['sizes']
        photo_url = ''
        photo_height = 0
        photo_type = ''
        for size in sizes:
            if int(size['height']) > photo_height:
                photo_height = size['height']
                photo_url = size['url']
                photo_type = size['type']
        name = str(item['likes']['count'])
        if name in photo_dict:
            name += str(item['date'])
        photo_dict[name] = (photo_url, photo_type)
    print(photo_dict)
    return photo_dict


def file_path(vk_id):
    filepath = '/VK ' + vk_id
    return filepath


def get_ya_token():
    ya_token = input('Введите токен Яндекс.Диск  ')
    ya_object = yadisk.YaDisk(token=ya_token)
    if ya_object.check_token(ya_token):
        print(f'Токен {ya_token} валиден')
        return ya_object
    else:
        print('Токен не валиден')


def making_dir(ya_object, path):
    if not ya_object.is_dir(path):
        ya_object.mkdir(path)
    else:
        print('Папка уже была создана ранее')


def upload_file(ya_object, file_dict, file_path):
    for note in file_dict:
        url = file_dict[note][0]
        name = file_path + '/' + note
        ya_object.upload_url(url, path=name)


vk_id = get_id()
vk_data = get_response(vk_id)
vk_dict = get_url(vk_data)
y = get_ya_token()
filepath = file_path(vk_id)
making_dir(y, filepath)
upload_file(y, vk_dict, filepath)
