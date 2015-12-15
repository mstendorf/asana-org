from models import *
import asana as asana

org_file = "/home/mas/.emacs.d/org/Agenda/plan.org"
asana_token = ''
workspace_id = 0
interested_in = [1,2,3]

# gather tasks from asana - SLOW due to api design, or the python module i use.
# did not care to check.
ass = Asana_workspace(token=asana_token, workspace_id=workspace_id,
                      interested_in=interested_in)
# parse the org file.
org = Orgtopia(path=org_file)


for project in ass.projects.values():
    print(project)
    for task in project.tasks.values():
        if not task.completed and len(task.name) > 0: # stupidity checks
            print("Gonna add %s to %s" % (task.name, project.name))
            org.add_task(project, task)

org.write()


print(ass.me["name"])
# sect = org.get_section("bnaa.dk")
# print(sect)
# print(len(sect.content))
# for tsk in sect.content:
#     print(tsk.heading)
#     for p in tsk.content:
#         if type(p) == PyOrgMode.OrgDrawer.Element:
#             print(p.name)
#             print(p.content[0].name)
#             print(p.content[0].value)
#         print(type(p))


# org_task = org.get_task(section, task)
# if org_task:
#     pass
# else:
#     org.add_task(section, task)
