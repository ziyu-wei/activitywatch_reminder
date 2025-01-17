# main_day2_test.py
from activity_analyzer import ActivityAnalyzer
import datetime

def main():
    analyzer = ActivityAnalyzer()
    buckets = analyzer.get_buckets()

    # 打印所有 buckets 名称，验证能拿到数据
    print("===> Buckets list:")
    for b in buckets:
        print(" - ", b)

    # 选择一个 bucket 做测试（如窗口监控）
    # 也可以自动筛选包含 'aw-watcher-window' 的
    window_buckets = [b for b in buckets if 'aw-watcher-window' in b]
    if not window_buckets:
        print("未找到窗口 bucket，请先确认 ActivityWatch 是否监控到桌面窗口。")
        return
    
    bucket_id = window_buckets[0]
    events = analyzer.get_today_events(bucket_id)
    print(f"\n===> {bucket_id} 过去24小时事件数: {len(events)}")

    # 简单统计 usage
    app_usage = {}
    for e in events:
        app_name = e['data'].get('app', 'unknown')
        duration = e.get('duration', 0)
        app_usage[app_name] = app_usage.get(app_name, 0) + duration
    
    # 打印结果
    print("\n===> 应用使用统计(秒):")
    for app, sec in app_usage.items():
        print(f"{app}: {sec} 秒 / {sec//60} 分钟")

if __name__ == "__main__":
    main()
