# aw_api.py
import requests
import datetime

BASE_URL = "http://localhost:5600/api/0"

def get_all_buckets():
    """
    获取 ActivityWatch 中当前所有的 buckets 列表
    """
    try:
        response = requests.get(f"{BASE_URL}/buckets")
        response.raise_for_status()
        return response.json()  # 返回一个列表，里面是各个 bucket 的信息
    except requests.exceptions.RequestException as e:
        print("请求 ActivityWatch /buckets 出错：", e)
        return []

def get_bucket_events(bucket_id, start_time, end_time):
    """
    获取指定 bucket 在给定时间区间内的所有事件数据
    start_time, end_time 应为 datetime 对象
    """
    params = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat()
    }
    try:
        response = requests.get(f"{BASE_URL}/buckets/{bucket_id}/events", params=params)
        response.raise_for_status()
        return response.json()  # 返回事件列表
    except requests.exceptions.RequestException as e:
        print(f"请求 bucket={bucket_id} 的 events 出错：", e)
        return []
