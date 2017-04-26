import twitter
# from twitter import *
import json

#Twitter app information
# KEY - 1
# consumer_secret='P6sc6XsM6h2ne9XZtT1RKHRCODb4snHKEp1MmA9jloMhEaSnbA'
# consumer_key='5zlB3yBmTW04agzm3KoBUknft'
# access_token='796306387903070208-HTGwSGUE4hqnjQdCG4M0zfeLPrwKPOK'
# access_token_secret='6YtVR1OLvbwteaEL5jS6QpIFmBqJ3eKfdorL0yNgwIhEC'

# KEY - 2
# consumer_secret='FuH4nRi6DLEAeWTtkFk0rltSPqCZLffHugSIS2zJ4gg1sDFdB7'
# consumer_key='b7qyY4pXGA7lNmduwYD3CZvkC'
# access_token='796306387903070208-E2BVN16Ye9au8EhjPp0DTA3XqdKpDKF'
# access_token_secret='g4dXXuB2FN6XhJgTI1ali4xHp72fqP9hGhoG4ksSL3iyW'

# # KEY - 3
consumer_secret='gGMatXDbkzmd98Zlcpp0iIAaQ4oVoep6FYETc54vPKCjbZ3vm6'
consumer_key='0NFMwVw2kk3ozt2ee8JbC1YJR'
access_token='796306387903070208-sl3weFGdmpHrcnWpdcIHYjC09ro1TYq'
access_token_secret='R7Y0RHniM39NjNMsU5wth5JddCfnd2d1hV115VLgLIOhL'

# # KEY - 4
# consumer_secret=''
# consumer_key=''
# access_token=''
# access_token_secret=''

# # KEY - 5
# consumer_secret=''
# consumer_key=''
# access_token=''
# access_token_secret=''


if __name__ == '__main__':
    #Logging
    # auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
    # auth = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
    #                    access_token_key=access_token, access_token_secret=access_token_secret)
    # api = twitter.Twitter(auth=auth)

    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token_key=access_token, access_token_secret=access_token_secret)

    # api = twitter.Api(consumer_key=[consumer key],
    #                   consumer_secret=[consumer secret],
    #                   access_token_key=[access token],
    #                   access_token_secret=[access token secret])


    list = []
    cursor=-1
    while cursor != 0:
        users = api.GetFollowers(screen_name='coralpintado', cursor = cursor)
        # users = api.friends.list(screen_name = 'coralpintado', cursor = cursor)
        # print(users)
        list.append(users)
        print(users['next_cursor'])
        cursor = int(users['next_cursor'])

    # print json.dumps(,indent=1)

    with open("data_twitter.json", "w") as file:
        for line in list:
            file.write(json.dumps(line))
        print("Finished")
        # file.write(list)
