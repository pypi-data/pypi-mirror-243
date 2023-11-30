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
from aurori.logs import logManager
from aurori.config import config_manager
from aurori.database import db
import logging
import traceback


class Job(object):
    """Base class that each job inherit from.
       The class define methods that all jobs have to implement
    """
    description = "Not available"  # description of the job
    disable = False  # disable the job
    local = True  # only runnable by the same workspace
    strict = True  # strict argument parsing
    requireAdmin = False  # admin is required to view the page
    requirePermission = None  # a permission is required in the meaning of one of the following

    # Repetetive members
    cron = False 
    day = None
    week = None
    day_of_week = None
    hour = None
    minute = None
    second = None

    def __init__(self, name=None, uri=None):
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name
        self.job_key = self.name
        self.workspace = ""
        self.parameters = None
        self.defineArguments()

    def start_job(self, **kwargs):
        from aurori.jobs.models import JobExecute

        self.debug_info = {}
        triggered = datetime.now()
        current_time = triggered.strftime("%H:%M:%S")

        logManager.info("Run " + self.name + " " + current_time)

        je = None

        with db.get_session() as db_session:
            if 'job_execution_id' in kwargs:
                je = db_session.query(JobExecute).filter_by(
                    id=kwargs['job_execution_id']).first()

            if je is None:
                je = JobExecute()
                je.workspace = self.workspace
                je.triggered_by = "Cron"
                je.triggered_on = triggered
                je.name = self.job_key
                db_session.add(je)
                db_session.commit()

            try:
                self.run(**kwargs)
                je.state = "SUCCEED"
                # je.results = {"hjsadhj": "jklsajdklas"}
            except Exception as e:
                je.state = "FAILED"
                je.results = {
                    "error": str(type(e)),
                    "traceback": str(traceback.format_exc()),
                    "debug": self.debug_info
                }
                print(je.results)

            after = datetime.now()
            delta = after - triggered
            je.lifetime = delta.total_seconds()
            db_session.commit()


    def addArgument(self,
                    name,
                    typestring,
                    label="",
                    description="",
                    optional=False,
                    group=None):
        p = {
            'name': name,
            'type': typestring,
            'label': label,
            'optional': optional,
            'group': group
        }
        if self.parameters is None:
            self.parameters = [p]
        else:
            self.parameters.append(p)

    def addDictArgument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        logManager.info("Add dict type argument to job {}".format(self.name))
        self.addArgument(name, 'dict', label, description, optional, group)

    def addListArgument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        logManager.info("Add list type argument to job {}".format(self.name))
        self.addArgument(name, 'list', label, description, optional, group)

    def addStringArgument(self,
                          name,
                          label="",
                          description="",
                          optional=False,
                          group=None):
        logManager.info("Add string type argument to job {}: {} - {}".format(
            self.name, name, label))
        self.addArgument(name, 'string', label, description, optional, group)

    def addDoubleArgument(self,
                          name,
                          label="",
                          description="",
                          optional=False,
                          group=None):
        logManager.info("Add double type argument to job {}".format(self.name))
        self.addArgument(name, 'double', label, description, optional, group)

    def addIntegerArgument(self,
                           name,
                           label="",
                           description="",
                           optional=False,
                           group=None):
        logManager.info("Add integer type argument for job {}".format(
            self.name))
        self.addArgument(name, 'integer', label, description, optional, group)

    def addDatetimeArgument(self,
                            name,
                            label="",
                            description="",
                            optional=False,
                            group=None):
        logManager.info("Add datetime type argument for job {}".format(
            self.name))
        self.addArgument(name, 'datetime', label, description, optional, group)

    def addTimeArgument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        logManager.info("Add time type argument for job {}".format(self.name))
        self.addArgument(name, 'time', label, description, optional, group)

    def addDateArgument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        logManager.info("Add date tyme argument for job {}".format(self.name))
        self.addArgument(name, 'date', label, description, optional, group)

    def addBooleanArgument(self,
                           name,
                           label="",
                           description="",
                           optional=False,
                           group=None):
        logManager.info("Add boolean type argument for job {}".format(
            self.name))
        self.addArgument(name, 'boolean', label, description, optional, group)

    def defineArguments(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError
