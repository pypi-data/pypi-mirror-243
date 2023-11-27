# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2023-02-10 09:28:07
@LastEditTime: 2023-11-27 11:46:16
@LastEditors: HuangJianYi
@Description: console引用
"""
# 框架引用
from seven_framework.console.base_console import *
from seven_cloudapp_frame.libs.common import *

# 初始化配置,执行顺序需先于调用模块导入
share_config.init_config("share_config.json")  # 全局配置,只需要配置一次


work_process_date_dict = {} # 作业心跳监控时间

def heart_beat_monitor(work_name, interval_time = 30, data={}):
    """
    :description: 作业心跳监控
    :param work_name: 作业名称
    :param interval_time: 上报间隔时间，单位：秒
    :param data: 数据字典
    :return: 
    :last_editors: HuangJianYi
    """
    from seven_cloudapp_frame.libs.customize.redis_helper import RedisExHelper
    is_heart_beat_monitor = share_config.get_value("is_heart_beat_monitor",True)
    if is_heart_beat_monitor == True:
        try:
            now_date = TimeHelper.get_now_format_time()
            process_date = work_process_date_dict.get(work_name)
            if not process_date:
                work_process_date_dict[work_name] = now_date
                process_date = now_date
            if abs(TimeHelper.difference_seconds(process_date, now_date)) > interval_time:
                RedisExHelper.init().set(f"heart_beat_monitor:{work_name}", JsonHelper.json_dumps({"process_date":now_date,"data":data}), 30*24*3600)
                work_process_date_dict[work_name] = now_date
        except Exception as ex:
            logger_error.error(f"{work_name}-作业心跳监控异常,ex:{traceback.format_exc()}")

def heart_beat_check(interval_time = 60):
    """
    :description: 作业心跳检测
    :param interval_time: 预警间隔时间，单位：分钟
    :return: 
    :last_editors: HuangJianYi
    """
    from seven_cloudapp_frame.libs.customize.redis_helper import RedisExHelper
    while True:
        try:
            time.sleep(60)
            init = RedisExHelper.init()
            match_result = init.scan_iter(match=f'heart_beat_monitor:*')
            for item in match_result:
                work_name = item
                info_json = init.get(work_name)
                if info_json:
                    info = json.loads(info_json)
                    process_date = info.get("process_date","")
                    if process_date:
                        now_date = TimeHelper.get_now_format_time()
                        if abs(TimeHelper.difference_minutes(process_date, now_date)) > interval_time:
                            logger_error.error(f"{work_name}-作业没有检测到心跳")
        except Exception as ex:
            logger_error.error(f"{work_name}-作业心跳检测异常,ex:{traceback.format_exc()}")

