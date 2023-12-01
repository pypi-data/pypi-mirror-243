from datetime import datetime
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

from aurori.types.jsonDict import JsonDict

from sqlalchemy import Boolean, Column, DateTime, Integer, String, LargeBinary
from aurori.database import SQLModelBase

class JobExecute(SQLModelBase):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), default="")
    workspace = Column(String(120), default="")
    job = Column(String(120), default="")
    state = Column(String(120), default="")
    triggered_on = Column(DateTime, default=datetime.utcnow)
    triggered_by = Column(String(120), default="")
    lifetime = Column(Integer, default=0)
    args = Column(JsonDict)
    results = Column(JsonDict)

    def __repr__(self):
        return '<Job {} for {}/{} >'.format(self.name, self.workspace,
                                            self.job)
