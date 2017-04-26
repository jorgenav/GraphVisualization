import twitter
import pandas as pd

#Twitter app information
# KEY - 1
consumer_secret='P6sc6XsM6h2ne9XZtT1RKHRCODb4snHKEp1MmA9jloMhEaSnbA'
consumer_key='5zlB3yBmTW04agzm3KoBUknft'
access_token='796306387903070208-HTGwSGUE4hqnjQdCG4M0zfeLPrwKPOK'
access_token_secret='6YtVR1OLvbwteaEL5jS6QpIFmBqJ3eKfdorL0yNgwIhEC'

# KEY - 2
# consumer_secret='FuH4nRi6DLEAeWTtkFk0rltSPqCZLffHugSIS2zJ4gg1sDFdB7'
# consumer_key='b7qyY4pXGA7lNmduwYD3CZvkC'
# access_token='796306387903070208-E2BVN16Ye9au8EhjPp0DTA3XqdKpDKF'
# access_token_secret='g4dXXuB2FN6XhJgTI1ali4xHp72fqP9hGhoG4ksSL3iyW'

# # KEY - 3
# consumer_secret='gGMatXDbkzmd98Zlcpp0iIAaQ4oVoep6FYETc54vPKCjbZ3vm6'
# consumer_key='0NFMwVw2kk3ozt2ee8JbC1YJR'
# access_token='796306387903070208-sl3weFGdmpHrcnWpdcIHYjC09ro1TYq'
# access_token_secret='R7Y0RHniM39NjNMsU5wth5JddCfnd2d1hV115VLgLIOhL'

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
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token_key=access_token, access_token_secret=access_token_secret)

    users = api.GetFriends(screen_name='coralpintado') # , cursor=cursor


    # ALMACENAMIENTO DE DATOS DE USUARIO: Lo ideal sería recorrer users e ir creando nodos con atributos para cada uno




    # data = pd.DataFrame()

    for u in users:

        # Nombre
        u.name
        # Número de seguidores
        # u.followers_count
        # Número de personas a las que sigue el usuario
        u.friends_count
        # Fecha de creación de la cuenta
        u.created_at
        # Número de favoritos que ha marcado el usuario
        u.favourites_count
        # Enlace http a la imagen del usuario
        # u.profile_image_url
        # Si True -> El usuario tiene los tweets protegidos
        # u.protected
        # Alias (nombre tras @)
        u.screen_name
        # Número de tweets del usuario
        u.statuses_count

