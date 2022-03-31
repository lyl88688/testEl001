import pytest


def test_case01():
    print('执行用例01.......')
    assert 1  # 断言失败


def test_case02():
    print('执行用例02.......')
    assert 1  # 断言成功


def test_custom_case03():
    print('执行用例03.......')
    assert 1  # 断言成功


if __name__ == '__main__':
    pytest.main(["-s", "test_case_01.py"])
    # pytest.main("-s demo1.py")