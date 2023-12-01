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

import inspect
import pkgutil
import sqlalchemy as sa

from aurori.workspaces.page import Page
from aurori.workspaces.permission import Permission
from aurori.jobs.job import Job
from aurori.jobs import jobManager
from aurori.logs import logManager
from fastapi import APIRouter


class Workspace(object):
    """Base class that each workspaceinherit from. 
       The class define methods that all workspaces have to implement
    """

    disabled = False

    def __init__(self, app, db, name=None, uri=None):
        self.description = 'UNKNOWN'
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name
        if uri is None:
            self.uri = self.name
        else:
            self.uri = uri
        self.permissions = {}
        self.dataViews = {}
        self.sections = {}
        self.pages = {}
        self.actions = []
        self.app = app
        self.db = db

    def addSinglePageSection(self, name, page, caption=None, permission=None):
        key = self.name + "_" + name
        if caption is None:
            caption = name
        self.sections[key] = {
            "caption": caption,
            "page": page,
            "permission": permission
        }

    def addPage(self, name, callback, caption=None, permission=None):
        key = self.name + "_" + name
        if caption is None:
            caption = name
        self.pages[key] = {
            "caption": caption,
            "callback": callback,
            "permission": permission
        }

    def get_page(self, name):
        key = self.name + "_" + name
        return self.pages[key]

    def discover_jobs(self, workspace_source_path):
        jobSource = workspace_source_path + '.' + self.name + '.jobs'
        imported_source = __import__(jobSource, fromlist=['blah'])

        for _, jobname, ispkg in pkgutil.iter_modules(
                imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                job_module = __import__(jobname, fromlist=['blah'])
                clsmembers = inspect.getmembers(job_module, inspect.isclass)
                for (_, c) in clsmembers:
                    if issubclass(c, Job) & (c is not Job):
                        if c.disable is False:
                            logManager.info(
                                f'    Job registered from "{c.__module__}"')
                            jobManager.register_job(self, c, True)

    def discover_apis(self, workspace_source_path):
        api_workspace_path = workspace_source_path + '.' + self.name + '.api'
        api_source = __import__(api_workspace_path, fromlist=['blah'])
        for _, modulename, ispkg in pkgutil.iter_modules(
                api_source.__path__, api_source.__name__ + '.'):
            if not ispkg:
                api_module = __import__(modulename,
                                               fromlist=['blah'])
                clsmembers = inspect.getmembers(api_module)
                for (api_name, c) in clsmembers:
                    if isinstance(c, APIRouter):
                        logManager.info(
                            f'    API "{api_name}" loaded from "{modulename}"'
                        )
                        if c.prefix != "":
                            self.app.include_router(c, tags=["App." + self.name])
                        else:
                            self.app.include_router(c,prefix= "/" + self.uri, tags=["App." + self.name])


    def discover_permissions(self, workspace_source):
        permissionsSource = workspace_source + '.' + self.name
        imported_source = __import__(permissionsSource, fromlist=['blah'])

        for _, permissionname, ispkg in pkgutil.iter_modules(
                imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                permission_module = __import__(permissionname,
                                               fromlist=['blah'])
                clsmembers = inspect.getmembers(permission_module,
                                                inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for Permission classes
                    if issubclass(c, Permission) & (c is not Permission):
                        permissionInstance = c()
                        logManager.info(
                            f'    Permission "{permissionInstance.name}" loaded from "{c.__module__}"'
                        )
                        self.add_permission(str(permissionInstance.name),
                                           permissionInstance)

    def discoverSections(self, workspace_source_path):
        '''
        sectionsSource = workspace_source_path + '.' + self.name
        imported_source = __import__(sectionsSource, fromlist=['blah'])

        for _, sectionname, ispkg in pkgutil.iter_modules(imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                section_module = __import__(sectionname, fromlist=['blah'])
                clsmembers = inspect.getmembers(section_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for Section classes
                    if issubclass(c, Section) & (c is not Section):
                        sectionInstance = c()
                        logManager.info(f'Section: "{c.__module__}" created for workspace: "{self.name}"')
                        #self.dataViews[str(dataViewInstance.uri)] = (dataViewInstance)
        '''

    def discoverNodeClasses(self, workspace_source_path):
        # for _, node_class, ispkg in pkgutil.iter_modules(imported_source.__path__, imported_source.__name__ + '.'):
        #    if ispkg:
        #        print(node_class)

        node_sources = workspace_source_path + '.' + self.name + '.' + 'nodes'
        imported_source = __import__(node_sources, fromlist=['blah'])

        for _, nodename, ispkg in pkgutil.iter_modules(
                imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                node_module = __import__(nodename, fromlist=['blah'])
                clsmembers = inspect.getmembers(node_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for DataView classes
                    if issubclass(c, NodeClass) & (c is not NodeClass):
                        if c.disable is False:
                            logManager.info(
                                f'NodeClass: "{c.__module__}" loaded from "{node_sources}"'
                            )
                            nodeManager.register_node_class(self, c)
                        else:
                            logManager.info(
                                f'NodeClass: "{c.__module__}" is disabled and wont show up"'
                            )
        '''
        for i in os.listdir(node_sources):
            module_path = os.path.join(node_sources,i)
            if os.path.isdir(module_path):
                module_path_list = module_path.split('/')
                module_path_list.append('node')
                node_module_source = '.'.join(module_path_list)
                node_module = __import__(node_module_source, fromlist=['blah'])
                clsmembers = inspect.getmembers(node_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for DataView classes
                    if issubclass(c, NodeClass) & (c is not NodeClass):
                        if c.disable is False:
                            logManager.info(f'NodeClass: "{c.__module__}" loaded from "{node_sources}"')
                            nodeManager.register_node_class(self, c)
                        else:
                            logManager.info(f'NodeClass: "{c.__module__}" is disabled and wont show up"')
        '''

    def discover_pages(self, workspace_source_path):
        pagesSource = workspace_source_path + '.' + self.name + '.' + 'pages'
        imported_source = __import__(pagesSource, fromlist=['blah'])

        for _, pagename, ispkg in pkgutil.iter_modules(
                imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                page_module = __import__(pagename, fromlist=['blah'])
                clsmembers = inspect.getmembers(page_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for DataView classes
                    if issubclass(c, Page) & (c is not Page):
                        pageInstance = c()
                        logManager.info(
                            f'    Page: "{pageInstance.name}" loaded from "{c.__module__}"'
                        )
                        if pageInstance.disable is True:
                            logManager.info(
                                f'    Page: "{pageInstance.name}" is disabled and wont show up'
                            )
                        else:
                            self.pages[str(pageInstance.name)] = pageInstance

    def discoverDataViews(self, workspace_source_path):
        actionsSource = workspace_source_path + '.' + self.name + '.' + 'views'
        imported_source = __import__(actionsSource, fromlist=['blah'])

        for _, actionname, ispkg in pkgutil.iter_modules(
                imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                action_module = __import__(actionname, fromlist=['blah'])
                clsmembers = inspect.getmembers(action_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for DataView classes
                    if issubclass(c, DataView) & (c is not DataView):
                        if hasattr(c, 'name'):
                            dataViewInstance = c(c.name, c.uri)
                            logManager.info(
                                f'DataView "{c.name}" loaded from "{c.__module__}"'
                            )
                        else:
                            dataViewInstance = c(c.__name__, c.uri)
                            logManager.info(
                                f'DataView "{c.__name__}" loaded from "{c.__module__}"'
                            )

                        dataViewInstance.defineProperties()
                        dataViewInstance.defineMetadata()

                        if dataViewInstance.disable is True:
                            logManager.info(
                                f'DataView: "{dataViewInstance.name}" is disabled and wont show up'
                            )
                        else:
                            self.dataViews[str(
                                dataViewInstance.uri)] = (dataViewInstance)

                        if dataViewInstance.entrykey is None:
                            raise LookupError(
                                "DataView {} dont define a key".format(
                                    dataViewInstance.name))

    def discoverActions(self, workspace_source_path):

        # create manager wide generic handlers for the view
        self.getViewActionHandler = viewHandler.GetViewActionHandler(
            self.app, self.db)
        self.createViewEntryActionHandler = viewHandler.CreateViewEntryActionHandler(
            self.app, self.db)
        self.removeViewEntryActionHandler = viewHandler.RemoveViewEntryActionHandler(
            self.app, self.db)
        self.updateViewEntryActionHandler = viewHandler.UpdateViewEntryActionHandler(
            self.app, self.db)
        self.executeViewActionsActionHandler = viewHandler.ExecuteViewActionsActionHandler(
            self.app, self.db)

        # add handlers for view actions
        # the view handlers are generic and added to every workspace
        self.actions.append(self.getViewActionHandler)
        self.actions.append(self.createViewEntryActionHandler)
        self.actions.append(self.removeViewEntryActionHandler)
        self.actions.append(self.updateViewEntryActionHandler)
        self.actions.append(self.executeViewActionsActionHandler)

        logManager.info(
            f'Actions for handling DataViews created for workspace "{self.name}"'
        )

        actionsSource = workspace_source_path + '.' + self.name + '.' + 'actions'
        # print("Discover actions for", self.uri, "from", actionsSource)
        imported_source = __import__(actionsSource, fromlist=['blah'])

        # print(imported_source)

        for _, actionname, ispkg in pkgutil.iter_modules(
                imported_source.__path__, imported_source.__name__ + '.'):
            if not ispkg:
                action_module = __import__(actionname, fromlist=['blah'])
                clsmembers = inspect.getmembers(action_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Check for Action classes
                    if issubclass(c, Action) & (c is not Action):
                        actionInstance = c(self.app)
                        logManager.info(
                            f'Action "{c.__module__}" created for workspace "{self.name}"'
                        )
                        if actionInstance.disable is True:
                            logManager.info(
                                f'Action: "{actionInstance.name}" is disabled and wont show up'
                            )
                        else:
                            self.actions.append(actionInstance)

    def discoverCommands(self, workspace_source_path):
        commandSource = workspace_source_path + '.' + self.name + '.' + 'commands'
        try:
            imported_source = __import__(commandSource, fromlist=['blah'])
            for _, commandname, ispkg in pkgutil.iter_modules(
                    imported_source.__path__, imported_source.__name__ + '.'):
                if not ispkg:
                    try:
                        command_module = __import__(commandname,
                                                    fromlist=['blah'])
                        command_module.register(imported_source.user_cli)
                        logManager.info(
                            'Custom command "{} > {}" registered.'.format(
                                imported_source.user_cli.name,
                                list(imported_source.user_cli.commands)[-1],
                            ))
                    except Exception as e:
                        logManager.error(
                            'Unable to import: {}, exception: {}'.format(
                                commandname, e))

            self.app.cli.add_command(imported_source.user_cli)
        except Exception:
            pass

    def discoverWidgets(self, workspace_source_path):
        widgetSource = workspace_source_path + '.' + self.name + '.' + 'widgets'
        try:
            imported_source = __import__(widgetSource, fromlist=['blah'])
            for _, widgetname, ispkg in pkgutil.iter_modules(
                    imported_source.__path__, imported_source.__name__ + '.'):
                if not ispkg:
                    widget_module = __import__(widgetname, fromlist=['blah'])
                    clsmembers = inspect.getmembers(widget_module,
                                                    inspect.isclass)
                    for (_, c) in clsmembers:
                        if issubclass(c, Widget) & (c is not Widget):
                            if c.disable is False:
                                logManager.info(
                                    f'Widget registered from "{c.__module__}"')
                                widgetInstance = widgetManager.register_widget(
                                    self, c)
                                self.actions.append(widgetInstance)
                                logManager.info(
                                    f'Widget uri registered from "{c.__module__}"'
                                )
                            else:
                                logManager.info(
                                    f'Widget disabled and not registered from "{c.__module__}"'
                                )

        except Exception:
            pass

    def add_permission(self, name, permission):
        from .models import Permission
        from aurori import db
        key = self.name + "." + name
        description = "No description available"

        if hasattr(permission, 'description'):
            description = permission.description

        engine = db.engine
        table_exists = sa.inspect(engine).has_table(Permission.__tablename__)
        if table_exists:
            with db.get_session() as db_session:
                p = db_session.query(Permission).filter_by(name=key).first()
                if p is None:
                    p = Permission(name=key, description=description)
                    db_session.add(p)
                    db_session.commit()
                    p = db_session.query(Permission).filter_by(name=key).first()
                else:
                    p.caption = description
                    db_session.commit()
                self.permissions[key] = p
        else:
            logManager.error(
                'Unable to create permission "{}" for workspace {}'.format(
                    name, self.name))

    def getPermission(self, name):
        key = self.name + "." + name
        return self.permissions[key]

    def createUserHook(self, user):
        pass

    def removeUserHook(self, user):
        pass
