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


# if __name__ == '__main__':
#     key_store = KeyStore('../../twitter_keys.txt')
#     tries = 0
#     requests = 0
#     while True:
#         try:
#             print("Entro en while!")
#             following = key_store.api.GetFriends(screen_name='coralpintado')
#             print("Abro conexion!")
#             requests += 1
#             print('Requests: ', requests)
#         except TwitterError as e:
#             if str(e.message) in ("[{'message': 'Rate limit exceeded', 'code': 88}]",
#                                   "[{'code': 88, 'message': 'Rate limit exceeded'}]"):
#                 tries += 1
#                 if tries == len(key_store.keys):
#                     print('All credentials limit reached, sleeping ...')
#                     tries = 0
#                     time.sleep(30)
#                 else:
#                     requests = 0
#                     print('Rate limit reached with credential ', key_store.idx, ' trying next ...')
#                     key_store.change_credentials()
#         except:
#             print('Generic error, retrying in one minute')
#             time.sleep(60)




if __name__ == '__main__':
    key_store = KeyStore('../../twitter_keys.txt')
    tries = 0
    requests = 0


    # following = key_store.api.GetFriendIDs(screen_name='coralpintado')
    following = key_store.api.GetFriendIDs(screen_name='manubarba')

    # followers = key_store.api.GetFollowers(screen_name='coralpintado')
    followers = key_store.api.GetFollowers(screen_name='manubarba')

    print("following y followers almacenados")

    i = 1

    dict_json = OrderedDict()
    lst_nodes = []

    lst_dict_json = []
    # dict_json['id'] = []
    # dict_json['name'] = []
    # dict_json['n_followers'] = []
    # dict_json['n_friends'] = []
    # dict_json['img'] = []
    # dict_json['alias'] = []
    # dict_json['n_tweets'] = []
    # dict_json['geo'] = []
    # dict_json['location'] = []
    # dict_json['verified'] = []

    # with open('data_twitter_C.json', 'w') as f:
    #     print("fichero abierto")
    with open('data_twitter_M.json', 'w') as f:
        for u in followers:
            for u2 in following:
                if (u.id == u2) and (not u.protected):
                    try:
                        print("Usuario de following: ", u2)
                        print("Entro en try")
                        # Número de usuario -> Crear
                        # dict_json['id'] = i
                        dict_json['id'] = u.id
                        # dict_json['id'].append(i)
                        i += 1
                        # Nombre
                        dict_json['name'] = u.name
                        # dict_json['name'].append(u.name)
                        # Número de seguidores
                        dict_json['n_followers'] = u.followers_count
                        # dict_json['n_followers'].append(u.followers_count)
                        # Número de personas a las que sigue el usuario
                        dict_json['n_friends'] = u.friends_count
                        # dict_json['n_friends'].append(u.friends_count)
                        # Enlace http a la imagen del usuario
                        dict_json['img'] = u.profile_image_url
                        # dict_json['img'].append(u.profile_image_url)
                        # Alias (nombre tras @)
                        dict_json['alias'] = u.screen_name
                        # dict_json['alias'].append(u.screen_name)
                        # Número de tweets del usuario
                        dict_json['n_tweets'] = u.statuses_count
                        # dict_json['n_tweets'].append(u.statuses_count)
                        # Geolocalización de tweets
                        dict_json['geo'] = u.geo_enabled
                        # dict_json['geo'].append(u.geo_enabled)
                        # User location -> Useful?
                        dict_json['location'] = u.location
                        # dict_json['location'].append(u.location)
                        # Cuenta verificada
                        dict_json['verified'] = u.verified
                        # dict_json['verified'].append(u.verified)

                        print("Guardo following de user")
                        # Almacenamiento de seguidos por el usuario
                        # dict_json['following'] = key_store.api.GetFriends(screen_name=u.screen_name)
                        dict_json['following'] = key_store.api.GetFriendIDs(screen_name=u.screen_name)

                        print("following de user guardado")

                        lst_dict_json.append(dict_json.copy())

                        # Se añade el usuario a la lista de nodos
                        lst_nodes.append(u.screen_name)

                    except TwitterError as e:
                        if str(e.message) in ("[{'message': 'Rate limit exceeded', 'code': 88}]",
                                              "[{'code': 88, 'message': 'Rate limit exceeded'}]"):
                            tries += 1
                            if tries == len(key_store.keys):
                                print('All credentials limit reached, sleeping ...')
                                tries = 0
                                time.sleep(30)
                            else:
                                requests = 0
                                print('Rate limit reached with credential ', key_store.idx, ' trying next ...')
                                key_store.change_credentials()
                    except:
                        print('Generic error, retrying in one minute')
                        time.sleep(60)




        # Volcado a fichero json
        # f.write(json.dumps(lst_dict_json))

        for user in lst_dict_json:
            f.write(json.dumps(user, ensure_ascii=False) + '\n')

    # for user in lst_nodes:
    #     following_user = api.GetFriends(screen_name=user)
    #     followers_user = api.GetFollowers(screen_name=user)

    # print(lst_nodes)

    # print(json.dumps(lst_dict_json))
    # for item in lst_nodes:
    #     print(item)

    # for item in lst_dict_json:
    #     print(item)
    # print(lst_dict_json)