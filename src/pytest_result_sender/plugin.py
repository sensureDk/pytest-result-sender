# _*_coding = UTF8 _*_
from _pytest.config import Config
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from datetime import datetime, timedelta
from pip._vendor import requests
from typing import List

data = {
    "passed":0,
    "failed":0,
    "skipped":0
}

def pytest_configure():
    # 配置文件加载完毕之后执行——即测试运行前运行
    start_time = datetime.now()
    data["start_time"] = start_time
    print(f"{start_time}开始执行了")
#
def pytest_collection_finish(session: "Session"):
    #测试用加载完毕后执行
    print(session.items)
    print(f"长度那么长+++++++++++++++++++{len(session.items)}")
    data["total_cases"] = len(session.items)

def pytest_runtest_logreport(report: "TestReport"):
    print(f"report对象值打印出来看下：{report}")
    if report.when == "call":
        if report.outcome == "passed":
            data["passed"] += 1
        if report.outcome == "failed":
            data["failed"] += 1
        if report.outcome == "skipped":
            data["skipped"] += 1
def pytest_unconfigure():
    # 测这执行完毕后，配置文件执行完毕后运行
    end_time = datetime.now()
    data["end_time"] = end_time
    print(f"{end_time}执行完毕了")
    durate_time = data["end_time"] - data["start_time"]
    data["durate_time"] = durate_time
    assert timedelta(seconds=3) > data["durate_time"] >timedelta(seconds=2.5)
    assert data["total_cases"] == 3
    assert data["passed"] == 2
    assert data["failed"] == 1
    data["passed_rate"] = data["passed"]/data["total_cases"] if data["total_cases"] >0 else 0
    data["failed_rate"] = data["failed"] / data["total_cases"] if data["total_cases"] > 0 else 0
    data["skipped_rate"] = data["skipped"] / data["total_cases"] if data["total_cases"] > 0 else 0
    data["cover_rate"] = data["passed_rate"]+data["failed_rate"]
    data["passed_rate"] = "{:.2%}".format(data["passed_rate"])
    data["failed_rate"] = "{:.2%}".format(data["failed_rate"])
    data["skipped_rate"] = "{:.2%}".format( data["skipped_rate"] )
    data["cover_rate"] = "{:.2%}".format(data["cover_rate"])

    assert data["passed_rate"] == "66.67%"
    assert data["failed_rate"] == "33.33%"
    assert data["skipped_rate"] == "0.00%"

    url = r"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4798277e-32d4-4cc3-8bdb-cadb579d45fc"
    json_date = {"msgtype": "markdown", "markdown": {"content":
                 f"""本次测试共执行案例<font color=\"warning\">{data['total_cases']}条</font>，请相关同事知悉！其中\n
        	     >测试通过数:<font color=\"green\">{data['passed']}</font>
        	     >测试失败数:<font color=\"red\">{data["failed"]}</font>
        	     >测试通过率:<font color=\"green\">{data['passed_rate']}</font>
    			 >测试失败率:<font color=\"red\">{data['failed_rate']}</font>
    			 >测试覆盖率:<font color=\"comment\">{data['cover_rate']}</font>
    			 >测试报告地址:<font color=\"green\">https://www.baidu.com</font>"""}, }
    response = requests.post( url=url, json=json_date )
    assert response.status_code == 200