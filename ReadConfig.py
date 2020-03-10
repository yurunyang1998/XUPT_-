import json
import os


def readconfig(path):
    try:
        config =  open(path,'r')
        data = ""
        for i in config:
            data = data+i
        jsondata = json.loads(data)
        return  jsondata

    except Exception as e:
        print(e)




if __name__ == '__main__':
    readconfig("./config.json")