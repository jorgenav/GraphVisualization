import pandas as pd
import json




list = []
list_data = []

# with open("../data/data_head") as f:
with open("../data/data_twitter.json") as f:
    for line in f:
        print(line)
        print("========================================================================================================================================================")

        # data = json.loads(line)
        # if data["type"] ==
        # list.append(line)

        # list_data.append(data)
        # print(line)
        # print("============================================================================================================")
        # print(data)

    # print(list)

    # for l in list:
    #     print(l)

    # data = f.read()





    # data = ujson.loads(line)
    # df = pd.read_json(f.read(), typ="series", orient='records')
    # df = pd.read_json(list, typ="series", orient='records')
    # df = pd.read_json(list_data, typ="series", orient='records')

    # print(df)

    # for line in data:
    #     print(line,'\n')



    # print(list)
    # print("============================================================================================================")
    # print(list_data)