from PyOrgMode import PyOrgMode
import asana as asana

class Asana_workspace:

    def __init__(self, token, workspace_id, interested_in):
        self.client = asana.Client.access_token(token)
        self.me = self.client.users.me()
        for workspace in self.me["workspaces"]:
            if workspace["id"] == workspace_id:
                self.ws = workspace
                break
        if self.ws:
            print("Workspace found")
            self.projects = {}
            projects = self.client.projects.find_all({"workspace":
                                                      workspace['id']})
            for project in projects:
                if project["id"] in interested_in:
                    self.projects[project["name"]] = self.Project(self.client, project)

        else:
            exit("Workspace not found!")

    class Project:
        def __init__(self, client, project):
            print("Init project %s" % project["name"])
            self.id = project["id"]
            self.name = project["name"]
            self.tasks = {}
            tasks = client.tasks.find_all({"project": project['id'],
                                                "opt_fields": ["notes", "name",
                                                               "completed_at",
                                                               "due_on",
                                                               "tags",
                                                               "assignee",
                                                               "assignee.name",
                                                               "completed"]})
            for task in tasks:
                self.tasks[task["id"]] = self.Task(client, task, 1)

        class Task:
            def __init__(self, client, tsk, level):
                print((level * "\t") + "Init Task %s" % tsk["name"])
                self.id = tsk["id"]
                self.name = tsk["name"]
                self.description = tsk["notes"]
                self.completed = tsk["completed"]
                self.completed_at = tsk["completed_at"]
                self.level = level
                self.subtasks = {}
                self.due_date = tsk["due_on"]
                self.assignee = tsk["assignee"]
                tasks = client.tasks.subtasks(tsk["id"],
                                              {"opt_fields": ["notes", "name",
                                                              "completed_at",
                                                              "due_on",
                                                              "tags",
                                                              "assignee",
                                                              "assignee.name",
                                                              "completed"]})
                # recursive nesting of elements.
                for subtask in tasks:
                    self.subtasks[subtask["id"]] = self.__class__(client, subtask, level+1)


class Orgtopia:

    def __init__(self, path):
        self.path = path
        self.base = PyOrgMode.OrgDataStructure()
        self.base.load_from_file(path)

    def write(self):
        """
        Write the orgfile to disk!
        """
        self.base.save_to_file(self.path)

    def task_to_org(self, task):
        import datetime
        todo = PyOrgMode.OrgNode.Element()
        todo.heading = task.name
        todo.level = task.level
        todo.todo = "DONE" if task.completed else "TODO"
        if task.due_date:
            _sched = PyOrgMode.OrgSchedule()
            print(task.due_date)
            _sched._append(todo, _sched.Element(deadline=datetime.datetime.strptime(task.due_date, "%Y-%m-%d").strftime("<%Y-%m-%d %a>")))
        # add task id as a property for later retrieval
        _props = PyOrgMode.OrgDrawer.Element("PROPERTIES")
        _props.append(PyOrgMode.OrgDrawer.Property("TASK_ID", str(task.id)))
        if task.assignee is not None:
            print(task.assignee)
            _props.append(PyOrgMode.OrgDrawer.Property("ASSIGNEE",
                                                       task.assignee["name"]))
        todo.append_clean(_props)
        for l in task.description.split("\n"):
            todo.content.append(l + "\n")

        # loop this code to add subtasks nested.
        for tsk in task.subtasks.values():
            todo.content.append(self.task_to_org(tsk))
        return todo

    def get_task(self, section, task):
        """
        Gets an asana task from an orgmode section
        """
        try:
            sect = self.sections[section]
            for tsk in sect.content:
                print(tsk.heading)
                for p in tsk.content:
                    if type(p) == PyOrgMode.OrgDrawer.Element:
                        if p.content[0].value == task.id:
                            return tsk

        except:
            return None

    def get_section(self, name):
        """
        Gets or creates a section or root org node.
        """

        return sect

    def process(self, asana):
        """
        Start processing the asana api.
        """
        for project in asana.projects.values():
            print(project)
            sect = PyOrgMode.OrgNode.Element()
            sect.heading = project.name
            sect.level = 0
            for task in project.tasks.values():
                if not task.completed and len(task.name) > 0:
                    print("Gonna add %s to %s" % (task.name, sect.heading))
                    sect.content.append(self.task_to_org(task))
            # now append the section to root
            self.base.root.append_clean(sect)
