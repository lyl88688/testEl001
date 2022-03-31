
import time
import subprocess

def cmd(command):
    subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    subp.wait(2)
    print(subp.communicate()[1])
    if subp.poll() == 0:
        print(subp.communicate()[1])
    else:
        print("失败")


cmd("allure serve C:/Users/ylliu/OneDrive/Automatic/pytestDemo/report/result")

cmd("java -version")

# cmd("exit 1")


"""
pytest --alluredir=./report/result


allure serve C:/Users/ylliu/OneDrive/Automatic/pytestDemo/report/result


allure generate C:/Users/ylliu/OneDrive/Automatic/pytestDemo/report/result -o C:/Users/ylliu/OneDrive/Automatic/pytestDemo/report/reporthtml/ --clean 


"""

