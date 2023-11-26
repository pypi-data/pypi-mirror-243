from .monitor import Monitor
from .ding import Ding
import time
from dotenv import load_dotenv

load_dotenv()

monitor = Monitor()
ding = Ding()


def run():
    while True:
        monitor.run()
        print(monitor.is_failed(), monitor.failed_status, monitor.check.get("failed_time"))
        if monitor.is_failed() and monitor.check.get("failed_time") \
                and ((time.time() - monitor.check.get("failed_send_time")) > 20 or
                     not monitor.check.get("failed_send_time")):
            monitor.check.update({"failed_send_time": time.time()})
            msg = [k + " 服务停止了.<br> " for (k, v) in monitor.status.items() if not v]
            msg = "".join(msg)
            msg = """**机器地址**: {} <br> 
    **发生时间**: {} <br>
    **问题描述**: <font color=#FF0000 size=6 face="黑体">{}</font>
""".format(monitor.ip, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg)
            if ding.send_text(msg):
                monitor.failed_send_time = time.time()
        elif not monitor.is_failed() and monitor.check.get("failed_time"):
            msg = [k + " 服务恢复了.<br> " for (k, v) in monitor.failed_status.items() if not v]
            msg = "".join(msg)
            msg = """**机器地址**: {} <br>
                **发生时间**: {} <br>
                **问题修复**: <font color=#00BB00 size=6 face="黑体">{}</font>
            """.format(monitor.ip, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg)
            monitor.check.update({"failed_time": 0.0})
            monitor.failed_status = {}
            ding.send_text(msg)

        time.sleep(3)
