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
import sys
from fastapi import APIRouter, FastAPI
from os import environ

from sqlalchemy_utils import database_exists

from aurori.config import configure_app, config_manager
from aurori.version import version
from aurori.logs import logManager
from aurori.workspaces import workspaceManager
from aurori.users import userManager
from aurori.workspaces.permission import Permission
from aurori.jobs import jobManager
from aurori.database import db, SQLModelBase
from aurori.utils import unicode_string_to_bytes
from aurori.pages import menu_builder

__version__ = version


def create_app(config, fastapi_config=None, minimal=False, api_prefix="", title="Aurori App", version="0.1.0"):
    config_manager.init_manager(config, fastapi_config)
    app = FastAPI(title=title, version=version)

    db.init_app(config)

    from aurori import app_router
    app.include_router(app_router, tags=["Core"])

    from aurori.jobs import jobs_router
    app.include_router(jobs_router,prefix=api_prefix, tags=["Jobs"])

    from aurori.users import user_router, core_router, basemodels  # noqa: F401, F811
    app.include_router(core_router, tags=["Core"])
    app.include_router(user_router, prefix=api_prefix + "/user", tags=["App.User"])

    if not minimal:
        jobManager.init_manager(config_manager.config)
        menu_builder.init_builder(app, db, userManager, workspaceManager)

    workspaceManager.init_app(app, config_manager.config, minimal=minimal,api_prefix=api_prefix)
    if not minimal:
        userManager.init_manager(app, db, workspaceManager, config_manager.config)        


    database_is_new = not database_exists(db.url)
    if database_is_new == True:
        logManager.warning("No database found at", db.url)
        logManager.warning("Creating new empty database")
        SQLModelBase.metadata.create_all(bind=db.engine)

    return app


# declare app routes
app_router = APIRouter()
from aurori import routes
