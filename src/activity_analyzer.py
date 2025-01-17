import requests
from datetime import datetime, timedelta
import json
import threading
import time
import math

class ActivityAnalyzer:
    def __init__(self):
        self.base_url = "http://localhost:5600/api/0"
        
    def get_buckets(self):
        """获取所有可用的数据桶"""
        response = requests.get(f"{self.base_url}/buckets")
        return response.json()
    
    def get_today_events(self, bucket_id):
        """获取最近24小时的事件数据"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        params = {
            'start': start_time.isoformat(),
            'end': end_time.isoformat()
        }
        
        try:
            print(f"\n调试信息 - {bucket_id} 的请求时间范围:")
            print(f"开始时间: {start_time}")
            print(f"结束时间: {end_time}")
            
            response = requests.get(
                f"{self.base_url}/buckets/{bucket_id}/events",
                params=params
            )
            print(f"调试信息 - {bucket_id} 的响应:")
            print(f"状态码: {response.status_code}")
            print(f"URL: {response.url}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"获取到的事件数量: {len(data)}")
                if len(data) > 0:
                    print("第一个事件示例:")
                    print(json.dumps(data[0], indent=2, ensure_ascii=False))
                return data
            else:
                print(f"请求失败: {response.text}")
                return []
        except Exception as e:
            print(f"获取 {bucket_id} 数据时出错: {str(e)}")
            return []

    def analyze_window_usage(self):
        """分析窗口使用情况"""
        buckets = self.get_buckets()
        window_buckets = [
            bucket_id for bucket_id in buckets
            if 'aw-watcher-window' in bucket_id
        ]
        
        print(f"\n调试信息 - 找到的窗口数据桶: {window_buckets}")
        
        if not window_buckets:
            print("未找到窗口数据桶")
            return {}
            
        window_bucket = window_buckets[0]
        events = self.get_today_events(window_bucket)
        
        app_usage = {}
        for event in events:
            app = event['data'].get('app', 'unknown')
            duration = event.get('duration', 0)
            app_usage[app] = app_usage.get(app, 0) + duration
            
        return app_usage

    def analyze_web_usage(self):
        """分析网页使用情况"""
        buckets = self.get_buckets()
        web_buckets = [
            bucket_id for bucket_id in buckets
            if 'aw-watcher-web' in bucket_id
        ]
        
        print(f"\n调试信息 - 找到的网页数据桶: {web_buckets}")
        
        if not web_buckets:
            print("未找到网页数据桶")
            return {}
        
        web_usage = {}
        for web_bucket in web_buckets:
            print(f"\n分析数据桶: {web_bucket}")
            events = self.get_today_events(web_bucket)
            
            for event in events:
                title = event['data'].get('title', 'unknown')
                duration = event.get('duration', 0)
                web_usage[title] = web_usage.get(title, 0) + duration
                
        return web_usage

class ActivityMonitor:
    """
    后台周期性拉取 ActivityWatch 的数据，
    并根据简单阈值进行提醒或打印。
    """
        
    def __init__(self, check_interval=30, usage_threshold=1800):
        """
        :param check_interval: 拉取间隔（秒），默认 300s = 5分钟
        :param usage_threshold: 使用阈值（秒），默认 1800s = 30分钟
        """
        self.check_interval = check_interval
        self.usage_threshold = usage_threshold
    
        self.analyzer = ActivityAnalyzer()
        # 用于缓存累计时长 {"app_name": total_seconds}
        self.usage_stats = {}
    
        # 线程开关
        self.monitoring = False
        self.monitor_thread = None
    
    def _fetch_and_update_usage(self):
        """
        核心逻辑：从 ActivityWatch 获取最新数据，更新 usage_stats 并做阈值判断
        """
        # 1. 获取窗口使用情况
        window_usage = self.analyzer.analyze_window_usage()  # {app: seconds}
        # 2. 获取网页使用情况
        web_usage = self.analyzer.analyze_web_usage()        # {title: seconds}
    
        # 打印调试信息（可选）
        print(f"[DEBUG] 本次获取到窗口数量: {len(window_usage)}, 网页数量: {len(web_usage)}")
    
        # 3. 合并到 self.usage_stats
        #    注意：这里的 usage 是过去 24 小时的总量，你可能需要做“增量”判断，见下文注释
        self._accumulate_usage(window_usage)
        self._accumulate_usage(web_usage)
    
        # 4. 阈值检查
        self._check_threshold()
    
    def _accumulate_usage(self, new_usage):
        """
        将本次获取的 usage 叠加到 self.usage_stats
        :param new_usage: dict, {app_name or title: usage_in_seconds}
        """
        for name, duration in new_usage.items():
            # 这里假设 new_usage 的时长是“过去24小时的累积”、
            # 但 self.usage_stats 也在记录累计。会出现重复统计的问题吗？
            #
            # 解决方法之一：只记录 "本次 - 上次" 的增量。（可参考 ActivityWatch 的 "latest events" 做增量）
            # 在 Day 3 简化处理：直接把 new_usage 加到 usage_stats 里
            self.usage_stats[name] = self.usage_stats.get(name, 0) + duration
    
    def _check_threshold(self):
        """
        判断哪几个应用/网站使用时长 >= threshold，并打印提醒
        """
        for name, total_sec in self.usage_stats.items():
            if total_sec >= self.usage_threshold:
                total_min = math.floor(total_sec / 60)
                print(f"[提醒] {name} 已累计使用超过 {total_min} 分钟，请注意休息或切换任务！")
                # 如果不想重复提醒，可以考虑在提醒后把该应用移除或标记
    
    def start_monitoring(self):
        """
        启动后台线程，定时执行 _fetch_and_update_usage()
        """
        if self.monitoring:
            print("监控已在进行中！")
            return
    
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.monitor_thread.start()
    
    def _run_loop(self):
        """
        后台线程循环，每隔 check_interval 秒执行一次
        """
        while self.monitoring:
            self._fetch_and_update_usage()
            time.sleep(self.check_interval)
    
    def stop_monitoring(self):
        """
        停止监控
        """
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            self.monitor_thread = None
        print("监控已停止。")
    
    def print_usage_stats(self):
        """
        打印当前缓存的 usage_stats
        """
        print("\n=== 当前累计使用统计 ===")
        total_all = sum(self.usage_stats.values())
        for name, sec in sorted(self.usage_stats.items(), key=lambda x: x[1], reverse=True):
            mins = math.floor(sec / 60)
            print(f"{name}: {sec:.1f} 秒 / {mins} 分钟")
        print(f"共计：{total_all:.1f} 秒\n")
