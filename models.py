from PyOrgMode import PyOrgMode
import asana as asana

class Asana_workspace:

    def __init__(self, token, workspace_id):
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
                                                              "completed"]})
                # recursive nesting of elements.
                for subtask in tasks:
                    self.subtasks[subtask["id"]] = self.__class__(client, subtask, level+1)


class Orgtopia:

    def __init__(self, path):
        self.path = path
        self.base = PyOrgMode.OrgDataStructure()
        self.base.load_from_file(path)
        self.sections = {}
        for section in self.base.root.content:
            self.sections[section.heading] = section

    def write(self):
        """
        Write the orgfile to disk!
        """
        self.base.save_to_file(self.path)

    def get_task(self, section, task):
        """
        Gets an asana task from an orgmode section
        """
        try:
            return self.sections[section][task.id]
        except:
            return None

    def add_task(self, section, task):
        """
        Adds an asana task from an orgmode section
        """
        todo = PyOrgMode.OrgNode.Element()
        todo.heading = task.name
        todo.level = task.level
        todo.todo = "DONE" if task.completed else "TODO"
        if task.due_date:
            _sched = PyOrgMode.OrgSchedule()
            _sched._append(todo, _sched.Element(deadline=task.due_on))
        # add task id as a property for later retrieval
        _props = PyOrgMode.OrgDrawer.Element("PROPERTIES")
        _props.append(PyOrgMode.OrgDrawer.Property("TASK_ID", task.id))
        if task.assignee:
            _props.append(PyOrgMode.OrgDrawer.Property("ASSIGNEE",
                                                       task.assignee["name"]))
        todo.append_clean(_props)
        self.sections.append_clean(todo)
