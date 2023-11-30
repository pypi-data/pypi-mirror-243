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

from datetime import datetime
from fastapi import APIRouter
from aurori.jobs.job import Job

from aurori.jobs.jobManager import JobManager
from aurori.logs import logManager
from inspect import isclass

jobManager = JobManager()

jobs_router = APIRouter()

def trigger_job(job_class, args, user):
    if user is None:
        logManager.info("Internal job {} triggered".format(job_class))
    else:
        logManager.info("User {} triggered job {}".format(user.email, job_class))

    job_id = jobManager.run_job(user,
                                job_class,
                                args,
                                datetime.now(),
                                log_trigger=True)
    return job_id


def add_dated_job(user,
                  job,
                  args,
                  date=None,
                  workspace=None,
                  max_instances=10):
    if date is None:
        date = datetime.now()
    key = ""
    if workspace is not None:
        if type(workspace) == str:
            key += workspace + '/'
        elif isclass(workspace):
            logManager.error(
                "Class parameters are not allowed for add_dated_job")
            return
        else:
            key += workspace.name + '/'

    if type(job) == str:
        key += job
    elif isclass(workspace):
        logManager.error("Class parameters are not allowed for add_dated_job")
        return
    elif issubclass(type(job), Job):
        key += job.name
    else:
        logManager.error("Unknown type of job in add_dated_job")
        return
    jobManager.run_job(user, key, args, date, max_instances)


def print_job_list():
    print("jobs.print_job_list not implemented yet")


from aurori.jobs import routes
