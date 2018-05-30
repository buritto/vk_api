import requests
import time
import datetime

class VkPhotoalbum:

    def __init__(self, user_access_token, user_id):
        self.access_token = user_access_token
        self.albums = {}
        self.user_id = user_id
        self.version = '5.52'


    def require(self, method_name, **kwargs):
        args = ''.join(f'{arg_name}={arg_value}&' for arg_name, arg_value in kwargs.items())
        str  = f"https://api.vk.com/method/{method_name}?{args}v={self.version}&access_token={self.access_token}"
        print(str)
        responce = requests.get(str)
        return responce

    def get_user_photoalbums(self):
        owner = self.user_id
        kwargs = {'owner': owner}
        responce_jsone = self.require('photos.getAlbums', **kwargs)
        for photoalbum in responce_jsone.json()['response']['items']:
            self.albums[photoalbum['title']] = {'id': photoalbum['id'], 'description': photoalbum['description']}

    def print_photoalbums(self):
        discr = 'description'
        for key, value in self.albums.items():
            print(f'{key}: {value[discr].strip()}')

    def delete_photos(self, name_album, start, finish):
        self.get_user_photoalbums()
        try:
            id_album = self.albums[name_album]['id']
        except KeyError:
            print(f"{name_album} does not exist")
            return
        kwargs = {'owner_id': self.user_id, 'album_id': id_album}
        responce_jsone = self.require('photos.get', **kwargs)
        for photo in responce_jsone.json()['response']['items']:
            date = int(photo['date'])
            if finish.timestamp() >= date >= start.timestamp():
                newKwargs = {'owner_id': self.user_id, 'photo_id':photo['id']}
                responce_jsone = self.require('photos.delete', **newKwargs)
                #print(responce_jsone)

    def delete_album(self, name):
        self.get_user_photoalbums()
        try:
            id = self.albums[name]['id']
        except KeyError:
            print(f"{name} does not exist")
            return
        kwargs = {'album_id': id}
        responce_jsone = self.require('photos.deleteAlbum', **kwargs)
        print(responce_jsone.json())


#responce = requests.get(f"https://api.vk.com/method/photos.get?owner_id=489381104"
 #                     f"&album_id=253010691&v=5.52&access_token=bf981de756fc746e2738f7f9a8e5cf3225e2d167bdcdb2a8e8e5d44b73cfcf8b3779903ae8dfd034a6eca")

#print(responce.json())

pa = VkPhotoalbum('02c0a7061a68bae939b36d771080ef3b9778d9b57b7e4095ea16e2d5b9468583b0855648f2a2e2faf6948', '489381104')
pa.get_user_photoalbums()
pa.print_photoalbums()
start = datetime.datetime(2017, 2, 2)
finish = datetime.datetime(2019, 10, 10)

pa.delete_photos('games', start, finish)
pa.delete_album('альбом который не существует')

