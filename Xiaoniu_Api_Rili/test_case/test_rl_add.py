#!/usr/bin/python
# -*- coding: UTF-8 _*_

import pytest
import json
import sys
import os
from common import Shell
from common.Request import RequestsHandler
from common.Logs import Log
from common.Yaml_Data import HandleYaml
from common.Retrun_Response import dict_style
from Conf.conf import *
import allure
from common import Assert
from common import Consts

handleyaml = HandleYaml()
yamldict = handleyaml.get_data()

# log = Log(__name__)
# logger = log.Logger

file = os.path.basename(sys.argv[0])
print(file)
log = Log(file)
logger = log.Logger

def test_one():
    x = "this"
    assert 'h' in x


def test_two():
    x = "hel"
    assert True


def test_three():
    a = "hello"
    b = "hello world"
    assert a in b