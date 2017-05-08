# -*- coding: utf-8 -*-

from twitter import *
from collections import OrderedDict
import json
import time

LIMIT_REACHED_ERROR = 88


class KeyStore:

    def __init__(self, keyfile):
        self.keys = [line.rstrip('\n') for line in open(keyfile)]
        self.idx = 0
        key = self.keys[self.idx].split()
        self.api = Api(consumer_key=key[0], consumer_secret=key[1],
                       access_token_key=key[2], access_token_secret=key[3])

    def size(self):
        return len(self.keys)

    def change_credentials(self):
        self.idx = (self.idx + 1) % len(self.keys)
        key = self.keys[self.idx].split()
        self.api = Api(consumer_key=key[0], consumer_secret=key[1],
                       access_token_key=key[2], access_token_secret=key[3])


if __name__ == '__main__':
    key_store = KeyStore('../../twitter_keys.txt')
    tries = 0
    requests = 0

    lst_dict_json = []
    dict_json = OrderedDict()
    users_read = []
    following2 = []

    following_stored = False
    followers_stored = False
    origin_stored = False

    while not following_stored:
        try:
            # Descarga inicial de seguidos por Capitan America
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

    while not origin_stored:
        try:
            # Descarga de datos sobre Capitan America
            u_origin = key_store.api.GetUser(screen_name='CaptainAmerica')

            dict_json['id'] = u_origin.id
            users_read.append(u_origin.id)
            dict_json['name'] = u_origin.name
            dict_json['n_followers'] = u_origin.followers_count
            dict_json['n_following'] = u_origin.friends_count
            dict_json['img'] = u_origin.profile_image_url
            dict_json['alias'] = u_origin.screen_name
            dict_json['n_tweets'] = u_origin.statuses_count
            dict_json['url'] = "http://www.twitter.com/" + u_origin.screen_name
            dict_json['following'] = key_store.api.GetFriendIDs(screen_name=u_origin.screen_name)

            lst_dict_json.append(dict_json.copy())

            origin_stored = True
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

    # Descarga de datos sobre seguidos por Capitan America
    for u in following:
            if u.verified:
                try:
                    dict_json['id'] = u.id
                    users_read.append(u.id)
                    dict_json['name'] = u.name
                    dict_json['n_followers'] = u.followers_count
                    dict_json['n_following'] = u.friends_count
                    dict_json['img'] = u.profile_image_url
                    dict_json['alias'] = u.screen_name
                    dict_json['n_tweets'] = u.statuses_count
                    dict_json['url'] = "http://www.twitter.com/" + u.screen_name
                    dict_json['following'] = key_store.api.GetFriendIDs(screen_name=u.screen_name)

                    # Almacenamiento de seguidos de segundo orden
                    added = 0
                    for user in dict_json['following']:
                        if (user not in following2) and (added < 20):
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

    # Descarga de datos de seguidos de segundo orden
    for u in following2:
        if u not in users_read and (len(users_read) < 200):
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

    with open('../data/data_twitter.json', 'w') as f:
        for user in lst_dict_json:
            f.write(json.dumps(user, ensure_ascii=False) + '\n')
