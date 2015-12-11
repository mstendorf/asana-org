from models import *
import asana as asana

org_file = ""
asana_token = ''
workspace_id = -1


# gather tasks from asana - SLOW due to api design, or the python module i use.
# did not care to check.
ass = Asana_workspace(token=asana_token, workspace_id=workspace_id)
# parse the org file.
org = Orgtopia(path=org_file)


for project in ass.projects.values():
    print(type(project))
    print(project)
    # create or fetch section.
    sect = org.get_section(project.name)
    for task in project.tasks.values():
        print("Gonna add %s to %s", (task.name, project.name))
        org.add_task(project.name, task)

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
