import time
import pytest
from _pytest.pytester import Pytester
from pytest_result_sender import plugin
from pathlib import Path
#
@pytest.fixture(autouse=True)
def mock():
   #测试执行前重置测试环境
   print(f"开始重置测试环境，环境格式前data={plugin.data}")
   back_data = plugin.data
   plugin.data = {
    "passed":0,
    "failed":0,
    "skipped":0
}
   yield
    #测试执行完毕后需要恢复测试环境
   plugin.data = back_data
@pytest.mark.parametrize("send_when",["onfail","always"])
def test_send_when(send_when,pytester:Pytester,tmp_path:Path):
    ini_path = tmp_path.joinpath("pytest.ini")
    ini_path.write_text(f"""
[pytest]
send_when = {send_when}
send_api = https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4798277e-32d4-4cc3-8bdb-cadb579d45fc""")
    config = pytester.parseconfigure(ini_path)
    # assert config.getini("send_when") == send_when
    print("&&&&&&&&&&&&&&&&&&&&&&&"+config.getini("send_when"))
    pytester.makepyfile(
        """
def test_pass():
    assert 1==1
        """
    )
    pytester.runpytest('-c',config)
    print(f"123123442###################{plugin.data}")
    if send_when == "onfail" and plugin.data.get("failed")>0:
        assert plugin.data.get("send_status") == 1
    elif send_when == "always":
        assert plugin.data.get("send_status") == 1
    elif send_when == "onfail" and plugin.data.get("failed") ==0:

        print(f"想看看这个输出结果到底时啥{plugin.data.get('send_status')}￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥")
        # assert plugin.data.get("send_status") is None
@pytest.mark.parametrize("send_api",["https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4798277e-32d4-4cc3-8bdb-cadb579d45fc",""])
def test_send_api(send_api,pytester:Pytester,tmp_path:Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = always
send_api = {send_api}
    """)
    config = pytester.parseconfigure(config_path)
    assert config.getini("send_api") == send_api
    pytester.runpytest('-c',config)
