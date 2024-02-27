"""
排程帮助类
"""
import importlib
import logging
import pkgutil
from inspect import isfunction, ismethod
from typing import Any, Callable, Dict, List, TypeVar

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from dependency_injector.wiring import inject
from infra_basic.errors.input import InvalidInputError

from infra_backbone.data.scheduler_jobs_config import SchedulerJobsConfig
from infra_backbone.model.scheduler_job_model import EnumSchedulerJobTriggerCategory

SchedulerType = TypeVar("SchedulerType", BaseScheduler, BlockingScheduler, BackgroundScheduler)

interval_init_settings = {
    "seconds": 0,
    "minutes": 0,
    "hours": 0,
    "days": 0,
    "weeks": 0,
    "start_date": None,
    "end_date": None,
}

cron_init_settings = {
    "year": "*",
    "month": "*",
    "day": "*",
    "week": "*",
    "day_of_week": "*",
    "hour": "*",
    "minute": "*",
    "second": "*",
    "start_date": None,
    "end_date": None,
}


@inject
def _f_inject():
    pass


InjectFunctionType = type(_f_inject)


def parse_interval_setting(trigger_expression: str) -> Dict[str, Any]:
    """
    解析时间间隔表达式，合计五位：秒 分 小时 天 周
    :param trigger_expression:
    :return:
    """
    result = interval_init_settings.copy()
    try:
        config_list = trigger_expression.split(" ")
        result["seconds"] = int(config_list[0])
        result["minutes"] = int(config_list[1])
        result["hours"] = int(config_list[2])
        result["days"] = int(config_list[3])
        result["weeks"] = int(config_list[4])
    except (ValueError, IndexError):
        raise InvalidInputError("{0} 不是有效的时间间隔表达式".format(trigger_expression))
    return result


def parse_cron_setting(trigger_expression: str) -> Dict[str, Any]:
    """
    解析Cron间隔表达式，合计6-7位：秒 分 小时 天 月 周中天 年，其中年可忽略
    :param trigger_expression:
    :return:
    """
    result = cron_init_settings.copy()
    try:
        config_list = trigger_expression.split(" ")
        result["second"] = config_list[0]
        result["minute"] = config_list[1]
        result["hour"] = config_list[2]
        result["day"] = config_list[3]
        result["month"] = config_list[4]
        result["day_of_week"] = config_list[5]
        if len(config_list) > 6:
            result["year"] = config_list[6]
    except (ValueError, IndexError):
        raise InvalidInputError(f"{trigger_expression} 不是有效的时间间隔表达式")
    return result


def scan_scheduler_func(scan_package, job_prefix: str = "job_") -> Dict[str, Callable]:
    """
    将任务从包中扫出，只将指定前缀的作为任务加入，系统默认为job_开头
    :param scan_package:
    :param job_prefix:
    :return:
    """
    func_result = {}
    for _, model_name, is_pkg in pkgutil.iter_modules(
        scan_package.__path__, scan_package.__name__ + "."
    ):
        if not is_pkg:
            sub_model = importlib.import_module(model_name)
            for sub_item in dir(sub_model):
                sub_item = getattr(sub_model, sub_item)
                if (
                    ismethod(sub_item)
                    or isfunction(sub_item)
                    or isinstance(sub_item, InjectFunctionType)
                ):
                    # TODO: "str" has no attribute "__name__"; maybe "__ne__"?
                    if str(sub_item.__name__).startswith(job_prefix):
                        func_result[sub_item.__name__] = sub_item
    return func_result


def _add_cron_job(
    job_name: str,
    job_id: str,
    scheduler: SchedulerType,
    func: Callable,
    job_param: SchedulerJobsConfig,
):
    """
    给排程添加cron间隔型的任务
    :param job_name:
    :param job_id:
    :param scheduler:
    :param func:
    :param job_param:
    :return:
    """
    cron_settings = cron_init_settings.copy()
    for cron_setting_item in cron_settings:
        if hasattr(job_param, cron_setting_item):
            cron_settings[cron_setting_item] = getattr(job_param, cron_setting_item)
    scheduler_job = scheduler.add_job(
        func,
        trigger="cron",
        name=job_name,
        id=job_id,
        year=cron_settings["year"],
        month=cron_settings["month"],
        day=cron_settings["day"],
        week=cron_settings["week"],
        day_of_week=cron_settings["day_of_week"],
        hour=cron_settings["hour"],
        minute=cron_settings["minute"],
        second=cron_settings["second"],
        start_date=cron_settings["start_date"],
        end_date=cron_settings["end_date"],
        replace_existing=True,
        kwargs=job_param.dict(),
    )
    logging.debug("cron job {0} id [{1}] added".format(job_name, job_id))
    return scheduler_job


def _add_interval_job(
    job_name: str,
    job_id: str,
    scheduler: SchedulerType,
    func: Callable,
    job_param: SchedulerJobsConfig,
):
    """
    给排程添加时间间隔型的任务
    :param job_name:
    :param job_id:
    :param scheduler:
    :param func:
    :param job_param:
    :return:
    """
    interval_settings = interval_init_settings.copy()
    for interval_setting_item in interval_settings:
        if hasattr(job_param, interval_setting_item):
            interval_settings[interval_setting_item] = getattr(job_param, interval_setting_item)
    scheduler_job = scheduler.add_job(
        func,
        trigger="interval",
        name=job_name,
        id=job_id,
        seconds=interval_settings["seconds"],
        minutes=interval_settings["minutes"],
        hours=interval_settings["hours"],
        days=interval_settings["days"],
        weeks=interval_settings["weeks"],
        start_date=interval_settings["start_date"],
        end_date=interval_settings["end_date"],
        replace_existing=True,
        kwargs=job_param.dict(),
    )
    logging.debug("interval job {0} id [{1}] added".format(job_name, job_id))
    return scheduler_job


def load_scheduler_jobs(
    scheduler: SchedulerType,
    scan_package,
    jobs_config: List[SchedulerJobsConfig],
):
    """
    为scheduler批量加载任务
    :param scheduler:
    :param scan_package:
    :param jobs_config:
    :return:
    """
    find_jobs_func = scan_scheduler_func(scan_package=scan_package)
    for job_config in jobs_config:
        job_func_name = job_config.func_name
        job_id = job_config.id
        if job_func_name in find_jobs_func:
            add_scheduler_job(
                scheduler=scheduler,
                job_name=job_func_name,
                job_id=job_id,
                func=find_jobs_func[job_func_name],
                job_param=job_config,
            )


def add_scheduler_job(
    scheduler: SchedulerType,
    job_name: str,
    job_id: str,
    func: Callable,
    job_param: SchedulerJobsConfig,
) -> Job:
    """
    为scheduler添加任务
    :param scheduler:
    :param job_name:
    :param job_id:
    :param func:
    :param job_param:
    :return:
    """
    if (
        ismethod(func)
        or isfunction(func)
        or isinstance(func, InjectFunctionType)
        and hasattr(job_param, "trigger_category")
    ):
        if job_param.trigger_category == EnumSchedulerJobTriggerCategory.INTERVAL.name:
            return _add_interval_job(
                job_name=job_name,
                job_id=job_id,
                scheduler=scheduler,
                func=func,
                job_param=job_param,
            )
        elif job_param.trigger_category == EnumSchedulerJobTriggerCategory.CRON.name:
            return _add_cron_job(
                job_name=job_name,
                job_id=job_id,
                scheduler=scheduler,
                func=func,
                job_param=job_param,
            )
    raise Exception("请指定排程任务需要执行的方法或者指定触发器的类型")
