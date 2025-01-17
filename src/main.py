# main.py
import datetime
from aw_api import get_all_buckets, get_bucket_events

def get_today_usage():
    """
    演示：获取“今天”在常见应用或网站上花费的总时长（分钟）。
    这里只是一个简单示例，可自行修改和扩展。
    """
    # 1. 获取全部 buckets
    buckets = get_all_buckets()
    if not buckets:
        print("无法获取任何 buckets，请检查 ActivityWatch 是否运行")
        return

    # 2. 找到自己需要统计的 bucket
    #    例如: aw-watcher-window_xxx_windows  (桌面应用使用时长)
    #         aw-watcher-web_xxx_chrome       (浏览器网页使用)
    target_buckets = []
    for b in buckets:
        bucket_id = b["id"]
        # 根据命名做一个简单的筛选
        if "aw-watcher-window" in bucket_id or "aw-watcher-web" in bucket_id:
            target_buckets.append(bucket_id)

    # 3. 确定时间区间：今天 0点 ~ 现在
    today = datetime.date.today()
    start_time = datetime.datetime.combine(today, datetime.time.min)
    end_time = datetime.datetime.now()

    usage_stats = {}

    # 4. 遍历每个目标 bucket，累积时长
    for bucket_id in target_buckets:
        events = get_bucket_events(bucket_id, start_time, end_time)

        # 遍历事件，将时长加和
        for event in events:
            # 不同 bucket 的 event 结构会不同，需根据实际情况解析
            # window-watcher 的事件一般有 "data" 字段，里面有 "app"、"title"
            # web-watcher 的事件有 "data" -> "url" / "title" 等
            data = event.get("data", {})
            start = event.get("timestamp")
            duration = event.get("duration", 0)  # 部分事件可能自带 duration

            if not duration:
                # 如果没有 duration，需要根据 event 的开始和结束时间来计算
                # ActivityWatch v0.10+ 的 event 可能有 "duration" 或 "end"
                end_ts = event.get("end")
                if end_ts:
                    # 将 string 转成 datetime, 并计算秒数
                    dt_start = datetime.datetime.fromisoformat(start.replace("Z", ""))
                    dt_end = datetime.datetime.fromisoformat(end_ts.replace("Z", ""))
                    duration = (dt_end - dt_start).total_seconds()
                else:
                    # 如果连 end 也没有，就暂时忽略或当作 0
                    pass

            # 根据 app 或 url 进行分类统计
            # 桌面应用： 'app': 'notepad.exe'
            # 网页： 'url': 'https://youtube.com/xxx'
            app_name = data.get("app") or data.get("title") or data.get("url") or "Unknown"

            usage_stats[app_name] = usage_stats.get(app_name, 0) + duration

    # 转换为分钟并打印结果
    for name, total_sec in usage_stats.items():
        total_min = round(total_sec / 60, 1)
        print(f"{name} : {total_min} 分钟")

if __name__ == "__main__":
    get_today_usage()
