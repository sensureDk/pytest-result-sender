
from datetime import datetime


def pytest_configure():
	#配置文件加载完毕之后执行——即测试运行前运行
	print(f"{datetime.now()}开始执行了")


def pytest_unconfigure():
	#
	print(f"{datetime.now()}执行完毕了")