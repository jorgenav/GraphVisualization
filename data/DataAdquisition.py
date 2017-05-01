# -*- coding: utf-8 -*-

import twitter
from twitter import TwitterError
from collections import OrderedDict
import json
import time

LIMIT_REACHED_ERROR = 88


class KeyStore:

    def __init__(self, keyfile):
        self.keys = [line.rstrip('\n') for line in open(keyfile)]
        self.idx = 0
        key = self.keys[self.idx].split()
        self.api = twitter.Api(consumer_key=key[0], consumer_secret=key[1],
                               access_token_key=key[2], access_token_secret=key[3])

    def size(self):
        return len(self.keys)

    def change_credentials(self):
        self.idx = (self.idx + 1) % len(self.keys)
        key = self.keys[self.idx].split()
        self.api = twitter.Api(consumer_key=key[0], consumer_secret=key[1],
                               access_token_key=key[2], access_token_secret=key[3])


if __name__ == '__main__':
    key_store = KeyStore('../../twitter_keys.txt')
    tries = 0
    requests = 0

    # following = key_store.api.GetFriendIDs(screen_name='coralpintado')
    following = key_store.api.GetFriendIDs(screen_name='manubarba')

    # followers = key_store.api.GetFollowers(screen_name='coralpintado')
    followers = key_store.api.GetFollowers(screen_name='manubarba', skip_status=True)
    followers = key_store.api.GetFollowers(screen_name='manubarba', skip_status=True)

    dict_json = OrderedDict()

    lst_dict_json = list()

    u_origin = key_store.api.GetUser(screen_name='manubarba')

    dict_json['id'] = u_origin.id
    dict_json['name'] = u_origin.name
    dict_json['n_followers'] = u_origin.followers_count
    dict_json['n_following'] = u_origin.friends_count
    dict_json['img'] = u_origin.profile_image_url
    dict_json['alias'] = u_origin.screen_name
    dict_json['n_tweets'] = u_origin.statuses_count
    dict_json['geo'] = u_origin.geo_enabled
    dict_json['location'] = u_origin.location
    dict_json['verified'] = u_origin.verified
    dict_json['following'] = key_store.api.GetFriendIDs(screen_name=u_origin.screen_name)

    lst_dict_json.append(dict_json)

    for u in followers:
        for u2 in following:
            if (u.id == u2) and (not u.protected):
                try:
                    # Número de usuario -> Crear
                    dict_json['id'] = u.id
                    # Nombre
                    dict_json['name'] = u.name
                    # Número de seguidores
                    dict_json['n_followers'] = u.followers_count
                    # Número de personas a las que sigue el usuario
                    dict_json['n_following'] = u.friends_count
                    # Enlace http a la imagen del usuario
                    dict_json['img'] = u.profile_image_url
                    # Alias (nombre tras @)
                    dict_json['alias'] = u.screen_name
                    # Número de tweets del usuario
                    dict_json['n_tweets'] = u.statuses_count
                    # Geolocalización de tweets
                    dict_json['geo'] = u.geo_enabled
                    # User location -> Useful?
                    dict_json['location'] = u.location
                    # Cuenta verificada
                    dict_json['verified'] = u.verified

                    # Almacenamiento de seguidos por el usuario
                    dict_json['following'] = key_store.api.GetFriendIDs(screen_name=u.screen_name)

                    lst_dict_json.append(dict_json.copy())

                except TwitterError as e:
                    if str(e.message) in ("[{'message': 'Rate limit exceeded', 'code': 88}]",
                                          "[{'code': 88, 'message': 'Rate limit exceeded'}]"):
                        tries += 1
                        if tries == len(key_store.keys):
                            print('All credentials limit reached, sleeping ...')
                            tries = 0
                            time.sleep(60)
                        else:
                            requests = 0
                            print('Rate limit reached with credential ', key_store.idx, ' trying next ...')
                            key_store.change_credentials()
                except:
                    print('Generic error, retrying in one minute')
                    time.sleep(60)


    # with open('data_twitter_C.json', 'w') as f:
    with open('data_twitter_M_test.json', 'w') as f:
        for user in lst_dict_json:
            f.write(json.dumps(user, ensure_ascii=False) + '\n')
