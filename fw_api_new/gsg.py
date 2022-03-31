# _*_ coding:utf-8 _*_

# ==================================================
#
#
#
# 步骤
# 1、
# 描述：测试mode
# ==================================================


import unittest, requests, time
from lib.commonData import *
import json, ddt, random
from lib.retryRun import Retry
from unittestreport import rerun

nonSupportMode = [1,2,3,4,5]
# 测试体
# @Retry(max_n=5, interErrVal=5)

@ddt.ddt
class cosoriTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    @ddt.data(*nonSupportMode)
    # @ddt.unpac
    @rerun(count=4, interval=3)
    def testNonsupportMode(self, modeVal):
        print("=================开始测试模式下发=====================", modeVal)

        self.assertEqual(modeVal, 1)



if __name__ == "__main__":
    unittest.main(verbosity=1)
