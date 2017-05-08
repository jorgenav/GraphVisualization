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

    lst_dict_json = []
    dict_json = OrderedDict()
    users_read = []

    following_stored = False
    followers_stored = False
    origin_stored = False

    while not following_stored:
        try:
            following = key_store.api.GetFriends(screen_name='CaptainAmerica')
            following_stored = True
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


    following2 = []
    others = ['POTUS44','POTUS','Kevfeige','vincentdonofrio','Jady0ung']

    for u in following:
            if u.verified and u.screen_name not in others:
                try:
                    # Número de usuario
                    dict_json['id'] = u.id
                    users_read.append(u.id)
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
                    # # Cuenta verificada
                    # dict_json['verified'] = u.verified
                    # URL
                    dict_json['url'] = "http://www.twitter.com/" + u.screen_name

                    # Almacenamiento de seguidos por el usuario
                    dict_json['following'] = key_store.api.GetFriendIDs(screen_name=u.screen_name)
                    added = 0
                    for user in dict_json['following']:
                        if (user not in following2) and (len(following2) < 200) and (added < 20):
                            following2.append(user)
                            added += 1
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

    for u in following2:
        if u not in users_read:
            try:
                user = key_store.api.GetUser(user_id=u)
                if user.verified and not user.protected:

                    dict_json['id'] = user.id
                    users_read.append(user.id)
                    dict_json['name'] = user.name
                    dict_json['n_followers'] = user.followers_count
                    dict_json['n_following'] = user.friends_count
                    dict_json['img'] = user.profile_image_url
                    dict_json['alias'] = user.screen_name
                    dict_json['n_tweets'] = user.statuses_count
                    dict_json['url'] = "http://www.twitter.com/" + user.screen_name
                    dict_json['following'] = key_store.api.GetFriendIDs(screen_name=user.screen_name)

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

    with open('data_twitter_MARVEL.json', 'w') as f:
        for user in lst_dict_json:
            f.write(json.dumps(user, ensure_ascii=False) + '\n')
