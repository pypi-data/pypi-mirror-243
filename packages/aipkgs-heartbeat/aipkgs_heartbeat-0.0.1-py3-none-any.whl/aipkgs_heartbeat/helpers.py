import datetime
import enum

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from typing import Union

class TriggerEnum(str, enum.Enum):
    interval = 'interval'
    cron = 'cron'
    date = 'date'


def create_scheduler():
    _scheduler = APScheduler()
    return _scheduler


def create_background_scheduler():
    _scheduler = BackgroundScheduler(daemon=True)
    return _scheduler


class AIBackgroundScheduler(BackgroundScheduler):

    def __init__(self):
        super().__init__()

        self.ai = self.create_inner()

    def create_inner(self):
        return AIBackgroundScheduler.ai(self)

    class ai:
        def __init__(self, outer):
            self.outer: AIBackgroundScheduler = outer

        def start(self):
            if not self.outer.running:
                self.outer.start()

        def shutdown(self, wait: bool = None):
            if self.outer.running:
                self.outer.shutdown(wait=wait or False)

        def add_job(self, id: str, func, trigger: TriggerEnum, date: Union[str, datetime.datetime, datetime.date] = None, seconds: int = None, minutes: int = None, week: str = None, day_of_week: str = None,
                    misfire_grace_time: int = None):
            params = {
                "seconds": seconds,
                "minutes": minutes,
                "week": week,
                "day_of_week": day_of_week,
                "run_date": date,
                "misfire_grace_time": misfire_grace_time,
            }
            not_none_params = {k: v for k, v in params.items() if v is not None}
            self.outer.add_job(id=id, func=func, trigger=trigger.value, **not_none_params)

        def add_listener(self, func, job):
            self.outer.add_listener(func, job)

        def jobs(self):
            return self.outer.get_jobs()

        def job(self, _id: str):
            return self.outer.get_job(job_id=_id)

        def has_job(self, _id: str) -> bool:
            return self.outer.get_job(job_id=_id) is not None

        def remove_job(self, _id: str):
            if self.has_job(_id):
                return self.outer.remove_job(job_id=_id)


class AIScheduler(APScheduler):

    def __init__(self):
        super().__init__()

        self.ai = self.create_inner()

    def create_inner(self):
        return AIScheduler.ai(self)

    class ai:
        def __init__(self, outer):
            self.outer: AIScheduler = outer

        def start(self):
            if not self.outer.running:
                self.outer.start()

        def shutdown(self, wait: bool = None):
            if self.outer.running:
                self.outer.shutdown(wait=wait or False)

        def add_job(self, id: str, func, trigger: TriggerEnum, date: Union[str, datetime.datetime, datetime.date] = None, seconds: int = None, minutes: int = None, week: str = None,
                    day_of_week: str = None, misfire_grace_time: int = None):
            params = {
                "seconds": seconds,
                "minutes": minutes,
                "week": week,
                "day_of_week": day_of_week,
                "run_date": date,
                "misfire_grace_time": misfire_grace_time,
            }
            not_none_params = {k: v for k, v in params.items() if v is not None}
            self.outer.add_job(id=id, func=func, trigger=trigger.value, **not_none_params)

        def add_listener(self, func, job):
            self.outer.add_listener(func, job)

        def jobs(self):
            return self.outer.get_jobs()

        def job(self, _id: str):
            return self.outer.get_job(id=_id)

        def has_job(self, _id: str) -> bool:
            return self.outer.get_job(id=_id) is not None

        def remove_job(self, _id: str):
            if self.has_job(_id):
                return self.outer.remove_job(id=_id)


background_scheduler = create_background_scheduler()
scheduler = create_scheduler()
