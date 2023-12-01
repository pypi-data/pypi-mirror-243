"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3+"

import logging
from datetime import datetime
from apscheduler.schedulers.asyncio  import AsyncIOScheduler
from cron_descriptor import ExpressionDescriptor, Options, CasingTypeEnum

from aurori.logs import logManager
from aurori.types.objDict import ObjDict
from aurori.database import db
from pytz import utc

class JobManager(object):
    """ The JobManager ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.config = None
        self.workspaceManager = None
        self.job_counter = 0
        self.jobs = {}
        self.scheduler = AsyncIOScheduler()
        logging.getLogger('apscheduler.scheduler').setLevel(logging.ERROR)
        logging.getLogger('apscheduler.scheduler').name = "SCHEDULER"
        logging.getLogger('apscheduler.executors.default').setLevel(logging.ERROR)
        logging.getLogger('apscheduler.executors.default').name = "EXECUTOR"
        logging.getLogger('EXECUTOR').setLevel(logging.ERROR)

    def init_manager(self, config):
        self.config = config

        from aurori.jobs.models import JobExecute
        self.job = JobExecute

    def get_jobs(self):
        return self.jobs

    def register_job(self, workspace, job_class, log_in_db=False):
        jobkey = job_class.__module__

        jobInstance = job_class()

        jobInstance.job_key = jobkey
        if workspace is not None:
            jobInstance.workspace = workspace.name
        job = {
            'job_class': job_class,
            'name': jobInstance.name,
            'workspace': workspace.name,
            'description': jobInstance.description,
            'parameters': jobInstance.parameters,
            'trigger': 'Internal',
            'log_in_db': log_in_db,
            'cron': jobInstance.cron,
            'day': jobInstance.day,
            'week': jobInstance.week,
            'day_of_week': jobInstance.day_of_week,
            'hour': jobInstance.hour,
            'minute': jobInstance.minute,
            'second': jobInstance.second,
        }

        if jobInstance.cron is True:
            cron_list = []

            if job_class.minute is None:
                cron_list.append("*")
            else:
                cron_list.append(job_class.minute)

            if job_class.hour is None:
                cron_list.append("*")
            else:
                cron_list.append(job_class.hour)

            if job_class.day is None:
                cron_list.append("*")
            else:
                cron_list.append(job_class.day)

            cron_list.append("*")

            if job_class.day_of_week is None:
                cron_list.append("*")
            else:
                cron_list.append(job_class.day_of_week)

            cron_string = " ".join(cron_list)
            options = Options()
            options.throw_exception_on_parse_error = False
            options.day_of_week_start_index_zero = True
            options.use_24hour_time_format = True
            options.casing_type = CasingTypeEnum.LowerCase
            descripter = ExpressionDescriptor(cron_string, options)
            logManager.info("Register repetitive job '{}' triggered {}".format(
                jobkey, descripter.get_description()))
            self.scheduler.add_job(
                jobInstance.start_job,
                kwargs=({
                    "job_id": str(jobkey)
                }),
                id=(str(jobkey)),
                trigger='cron',
                replace_existing=True,
                day=job_class.day,
                day_of_week=job_class.day_of_week,
                week=job_class.week,
                hour=job_class.hour,
                minute=job_class.minute,
                second=job_class.second,
            )
            job['trigger'] = descripter.get_description()

        self.jobs[str(jobkey)] = ObjDict(job.copy())

    def run_job(self,
                user,
                job_class,
                args,
                date,
                max_instances=10,
                log_trigger=False):
        job_key = job_class.__module__
        if job_key in self.jobs:
            with db.get_session() as db_session:
           
                je = None
                if log_trigger is True:
                    from aurori.jobs.models import JobExecute
                    je = JobExecute()
                    je.triggered_on = datetime.now()
                    if user is None:
                        je.triggered_by = ""
                    else:
                        je.triggered_by = user.email
                    je.name = job_key
                    je.workspace = self.jobs[job_key].workspace
                    je.state = "TRIGGERED"

                    db_session.add(je)
                    db_session.commit()

                # if self.jobs[jobkey]['cron']:
                #     # handle a cron job
                #     job = self.scheduler.get_job(jobkey)
                #     job.modify(next_run_time=datetime.now())
                #     return None
                # else:

                # handle a single trigger job
                jobInstance = self.jobs[job_key]['job_class']()
                self.job_counter += 1
                job_ececution_id = None

                if je is not None:
                    job_ececution_id = je.id

                kwargs = {
                    "job_id": str(job_key) + str(self.job_counter),
                    "job_execution_id": job_ececution_id
                }
                kwargs = {**kwargs, **args}
                self.scheduler.add_job(
                    jobInstance.start_job,
                    id=(str(job_key) + str(self.job_counter)),
                    trigger='date',
                    next_run_time=date.astimezone(utc),
                    kwargs=kwargs,
                    max_instances=max_instances,
                )
                if je is not None:
                    return je.id
                else:
                    return None
        else:
            logManager.error("Unknown type of job in add_dated_job")
            return None
