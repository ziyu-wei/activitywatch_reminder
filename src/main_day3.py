# main_day3.py
import time
import threading
import math
from activity_analyzer import ActivityAnalyzer, ActivityMonitor


# 可选：你也可以使用第三方库 'schedule'
# import schedule
def main():
    monitor = ActivityMonitor(
        check_interval=30,    # 每5分钟拉取一次
        usage_threshold=1800,  # 30分钟阈值
    )
    monitor.start_monitoring()

    print("监控已启动，按 Ctrl+C 停止...\n")

    try:
        # 主线程可以做别的事，也可以空跑
        while True:
            time.sleep(10)  # 让主线程保持活跃
            # 期间可以随时调用 monitor.print_usage_stats() 看看情况
    except KeyboardInterrupt:
        # 用户 Ctrl + C
        monitor.stop_monitoring()
        monitor.print_usage_stats()
        print("退出程序。")

if __name__ == "__main__":
    main()

