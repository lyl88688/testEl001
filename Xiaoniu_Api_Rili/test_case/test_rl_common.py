#!/usr/bin/python
# -*- coding: UTF-8 _*_

import pytest
import json
import sys
import os
from common.Retrun_Response import dict_style
from common import Shell
from common.Request import RequestsHandler
from common.Logs import Log
from common.Yaml_Data import HandleYaml
from Conf.conf import *
import allure
from common import Assert
from common import Consts

handleyaml = HandleYaml()
yamldict = handleyaml.get_data()

file = os.path.basename(sys.argv[0])
log = Log(file)
logger = log.Logger


@allure.description("测试http://calapi.51jirili.com/config/common接口")
@allure.testcase("http://calapi.51jirili.com/config/common", "测试用例地址👇")
def test_delete_1():
    assert True