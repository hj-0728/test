from backend.scheduler_jobs.jobs_cron import job_sync_dingtalk, job_sync_context


def test_job_sync_dingtalk(prepare_app_container):
    """
    测试同步钉钉定时任务
    """
    func_args = {"dingtalk_corp_id": "b51e6648-7947-4969-8c1f-52051ecb5673"}
    job_sync_dingtalk(func_args=func_args)


def test_job_sync_context(prepare_app_container):
    """
    测试同步上下文定时任务
    """
    func_args = {"dingtalk_corp_id": "b51e6648-7947-4969-8c1f-52051ecb5673"}
    job_sync_context(func_args=func_args)
