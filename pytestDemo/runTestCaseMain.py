import  pytest
from common import shell

if __name__ == '__main__':
    pytest.main(["-s", "./testCases/", "--alluredir", "./report/result/"])
    shell = shell.Shell()
    cmd = 'allure generate %s -o %s --clean' % ('./report/result', './report/reporthtml')

    # logger.info("开始执行报告生成")
    print("开始执行报告生成", cmd)
    #未响应shell.invoke(cmd)
    # shell.invoke(cmd)
