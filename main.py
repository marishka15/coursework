import os
import requests
from pprint import pprint
import json
from dotenv import load_dotenv
from tqdm import trange
from time import sleep


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.id = user_id
        self.version = version
        self.params = {'access_token': access_token, 'v': version}

    def get_photos_info(self, count = 5):
       url = 'https://api.vk.com/method/photos.get'
       params = {
           'owner_id': user_id,
           'album_id': 'profile',
           'photo_sizes': '1',
           'extended': '1',
           'count' : count,
           **self.params
       }
       response = requests.get(url, params=params)
       result = response.json()
       data = result['response']['items']
       all_list = []
       for line in data:
           element = line['sizes']
           list_letter = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's']
           x = ''
           for letter in list_letter:
               if x!= '':
                   break
               for size in element:
                   if size['type'] == letter:
                       x = f'Самый большой размер - {letter}'
                       photo_url = size['url']
                       file_name = line['likes']['count']
                       dictionary = {
                           'file_name': f'{file_name}.jpg',
                           'size': x,
                           'url': f'{"".join(photo_url)}'
                       }
                       all_list.append(dictionary)
                       break

           with open('files.json', 'w', encoding='utf-8') as f:
               json.dump(all_list, f, ensure_ascii=False, indent=2)

       return all_list
class YandexDisk:
    def __init__(self, token):
        self.token = token

    def folder(self):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {'path': f'{vk_photo}', 'overwrite': 'true'}
        response = requests.put(folder_url, params=params, headers=headers)
        return response.json()

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        response = requests.get(files_url, headers=headers)
        return response.json()

    def upload_file_to_disk(self, vk_photo, file_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': f'{vk_photo}/{file_name}', 'url': json_data}
        response = requests.post(upload_url, params=params, headers=headers)
        return response.json()



if __name__ == '__main__':

    load_dotenv()
    access_token = os.getenv('token_vk')
    #VK
    user_id = str(input('Введите id пользователя VK: '))
    vk = VK(access_token, user_id)
    res = vk.get_photos_info()
    #pprint(res)

    #ЯндексДиск
    TOKEN = str(input('Введите токен ЯндексДиск: '))
    yd = YandexDisk(token=TOKEN)
    res_1 = yd.get_files_list()

    #Копирование фото на ЯД
    vk_photo = 'images_vk'
    result = ''
    for photo in res:
        file_name = photo['file_name']
        json_data = photo['url']
        result = yd.upload_file_to_disk(vk_photo, file_name)
    #pprint(result)

    #Прогресс выполнения
    for i in trange(100):
        sleep(0.01)







