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

import os
import pathlib
import pkgutil
import inspect
from aurori.workspaces.workspace import Workspace
from aurori.logs import logManager
import sys
import traceback
import sqlalchemy as sa


class WorkspaceManager(object):
    """ The WorkspaceManager holds all available workspaces and load them while creation.
    """
    def __init__(self, workspace_source_path):
        self.workspace_source_path = workspace_source_path
        self.app = None
        self.db = None
        self.config = None
        self.workspaces = None
        self.user_class = None
        self.api_prefix = None

    def init_app(self, app, config, minimal = False, api_prefix="api/v1"):
        self.app = app
        self.config = config
        self.workspaces = []
        self.seen_paths = []
        self.api_prefix = api_prefix
        logManager.info("")
        logManager.info(
            f'Discover workspaces in path : {self.workspace_source_path}')
        self.discover_workspaces(self.workspace_source_path)
        self.discover_models()
        if minimal is False:
            self.discover_permissions()
            self.create_permissions()
            self.discover_jobs()
            self.discover_pages()
            self.discover_apis()

        #    self.registerWorkspacePermissions()
        #    self.registerWorkspaceAPIs()

        logManager.info("")
        logManager.info("Workspaces and their components initialized")

    def get_workspace(self, name):
        for w in self.workspaces:
            if w.name is name:
                return w
        return None

    def reload_workspaces(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.workspaces = []
        self.seen_paths = []
        logManager.info("")
        logManager.info(
            f'Discover workspaces in path : {self.workspace_source_path}')
        self.discover_workspaces(self.workspace_source_path)

    def discover_permissions(self):

        logManager.info("")
        logManager.info("Discover permissions:")

        for w in self.workspaces:
            logManager.info(f'  For workspace: "{w.name}"')

            # try to register permissions
            try:
                w.discover_permissions(self.workspace_source_path)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(
                    f'  Workspace "{w.uri}" unable to discover permissions  ({str(type(e).__name__)}:{e})'
                )

    def discover_pages(self):
        logManager.info("")
        logManager.info("Discover pages:")

        for w in self.workspaces:
            logManager.info(f'  For workspace: "{w.name}"')
            workspace_config_section_name = pathlib.Path(
                w.path).resolve().name.upper()
            # try to register permissions

            try:
                w.discover_pages(self.workspace_source_path)
            except Exception as exception:
                traceback.print_exc(file=sys.stdout)
                logManager.error(
                    f'  Workspace "{w.name}" unable to discover pages  ({str(type(exception).__name__)}:{exception})'
                )

    def discover_jobs(self):
        logManager.info("")
        logManager.info("Discover jobs:")

        for w in self.workspaces:
            logManager.info(f'  For workspace: "{w.name}"')
            workspace_config_section_name = pathlib.Path(
                w.path).resolve().name.upper()

            if workspace_config_section_name in self.config and "disable_jobs" in self.config[
                    workspace_config_section_name] and self.config[
                        workspace_config_section_name]["disable_jobs"]:
                logManager.info(f'    Jobs for "{w.name}" are disabled by config')
            else:
                # try to register jobs
                try:
                    w.discover_jobs(self.workspace_source_path)
                except Exception as e:
                    traceback.print_exc(file=sys.stdout)
                    logManager.error(
                        f'    Workspace "{w.name}" unable to discover jobs  ({str(type(e).__name__)}:{e})'
                    )

    def discover_apis(self):
        logManager.info("")
        logManager.info("Discover apis:")

        for w in self.workspaces:
            logManager.info(f'  For workspace: "{w.name}"')
            workspace_config_section_name = pathlib.Path(
                w.path).resolve().name.upper()
            
            try:
                w.discover_apis(self.workspace_source_path)
            except Exception as exception:
                traceback.print_exc(file=sys.stdout)
                logManager.error(
                    f'  Workspace "{w.name}" unable to apis pages  ({str(type(exception).__name__)}:{exception})'
                )
                
    def discover_models(self):
        source = self.workspace_source_path
        try:
            imported_source = __import__(source, fromlist=['blah'])
        except Exception as exception:
            logManager.error(f"Unable to locate workspaces {str(exception)}")
            return
        all_current_paths = []

        # all_current_paths.append(imported_source.__path__._path)

        if isinstance(imported_source.__path__, str):
            all_current_paths.append(imported_source.__path__)
        else:
            all_current_paths.extend([x for x in imported_source.__path__])

        from aurori.users.basemodels import UserBase
        
        # remove duplicates
        all_current_paths = list(set(all_current_paths))

        for pkg_path in all_current_paths:
            # Walk through all sub directories
            child_pkgs = [
                p for p in os.listdir(pkg_path)
                if os.path.isdir(os.path.join(pkg_path, p))
            ]

            for child_pkg in child_pkgs:
                try:
                    # fixme: this was assigned to a later unused variable?
                    # imported_package = __import__(source + '.' + child_pkg + '.models', fromlist=['blah'])
                    imported_package = __import__(source + '.' + child_pkg + '.models',
                               fromlist=['blah'])
                    for _, modelpackagename, ispkg in pkgutil.iter_modules(
                            imported_package.__path__,
                            imported_package.__name__ + '.'):
                        workspace_module = __import__(modelpackagename,
                                                      fromlist=['blah'])
                        clsmembers = inspect.getmembers(
                            workspace_module, inspect.isclass)

                        for (_, c) in clsmembers:     
                            if issubclass(c, UserBase) & (c is not UserBase):
                                if self.user_class is not None and self.user_class != c:
                                    raise Exception("Multiple User models found. For a aurori app only one is allowed.")
                                self.user_class = c
                except ModuleNotFoundError:
                    modelmodule = source + '.' + child_pkg + '.models'
                    logManager.info(f'No model found for {modelmodule}')
        
        if self.user_class is None:
            logManager.warning(f'No User model derived from aurori.users.basemodels.UserBase found.')
            logManager.warning(f'A aurori app needs a user model to work properly.')
            logManager.warning(f'Please define a derived model named "User" in your workspaces, if needed.')
            logManager.warning(f'The default model will be used, please reference: aurori.users.defaultmodels.User ')
            from aurori.users.defaultmodels import User

    def discover_workspaces(self, source):
        """Recursively walk the supplied package to retrieve all plugins (workspaces)
        """

        try:
            imported_source = __import__(source, fromlist=['blah'])
        except Exception as e:
            logManager.error(f"Unable to locate workspaces {str(e)}")
            return

        all_current_paths = []

        # all_current_paths.append(imported_source.__path__._path)

        if isinstance(imported_source.__path__, str):
            all_current_paths.append(imported_source.__path__)
        else:
            all_current_paths.extend([x for x in imported_source.__path__])

        # remove duplicates
        all_current_paths = list(set(all_current_paths))

        for pkg_path in all_current_paths:
            # Walk through all sub directories
            child_pkgs = [
                p for p in os.listdir(pkg_path)
                if os.path.isdir(os.path.join(pkg_path, p))
            ]

            # Every sub directory contains one workspace
            for child_pkg in child_pkgs:
                imported_package = __import__(source + '.' + child_pkg,
                                              fromlist=['blah'])
                
                clsmembers = inspect.getmembers(imported_package)
              
                uri = ""
                if hasattr(imported_package,"uri"):
                    uri = imported_package.uri
                else:
                    uri = str(child_pkg).lower()

                logger = None
                if hasattr(imported_package,"logger"):
                    logger = imported_package.logger


                workspaceInstance = Workspace(self.app, self.db, str(child_pkg), uri)

                if hasattr(imported_package,"description"):
                    workspaceInstance.description = imported_package.description

                if hasattr(imported_package,"disabled"):
                    workspaceInstance.disabled = imported_package.disabled

                workspaceInstance.path = os.path.dirname(
                    imported_package.__file__)
                workspace_config_section_name = pathlib.Path(
                    imported_package.__file__).parent.resolve(
                    ).name.upper()
                logManager.info(
                    f'  Discovered workspace "{workspaceInstance.name}" as "{workspaceInstance.uri}" from "{source + "." + child_pkg}"')

                if (workspace_config_section_name
                        in self.config) and (
                            "disabled" in self.config[
                                workspace_config_section_name]
                        ) and (self.config[
                            workspace_config_section_name]
                                ["disabled"]):
                    logManager.info(
                        '  The workspace is disabled by config and wont show up'
                    )
                else:
                    if workspaceInstance.disabled is True:
                        logManager.info(
                            '  The workspace is disabled by module definition and wont show up'
                        )
                    else:
                        logManager.register_logger(logger, workspaceInstance.name)
                        self.workspaces.append(
                            workspaceInstance)

    def create_permissions(self):
        """ Run createPermissions for all workspaces and store permissions
        """
        all_permissions = {}
        for ws in self.workspaces:

            workspace_permissions = ws.permissions
            if workspace_permissions is not None:
                all_permissions = {**all_permissions, **workspace_permissions}

        # delete orphaned permissions for security reasons
        from .models import Permission
        from aurori import db
        engine = db.engine
        table_exists = sa.inspect(engine).has_table(Permission.__tablename__)
        if table_exists:
            with db.get_session() as db_session:
                db_permissions = db_session.query(Permission).all()
                for permission in db_permissions:
                    if permission.name not in all_permissions:
                        logManager.warning(f'  Delete orphaned {permission}')
                        db_session.delete(permission)
                        db_session.commit()