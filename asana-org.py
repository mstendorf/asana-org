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

print(ass.me["name"])

# org_task = org.get_task(section, task)
# if org_task:
#     pass
# else:
#     org.add_task(section, task)
