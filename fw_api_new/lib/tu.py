

from lib import globalName



def kktest():
    global device_cid

    globalName.device_cid = "454545"

def fsf():
    print(globalName.device_cid)

kktest()
fsf()
# print(globalName.device_cid)
