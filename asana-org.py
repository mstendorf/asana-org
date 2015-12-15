from models import *
import asana as asana

org_file = "/home/effi/.emacs.d/org/Agenda/plan.org"
asana_token = ''
workspace_id = 1
interested_in = [1,2,3]

# gather tasks from asana - SLOW due to api design, or the python module i use.
# did not care to check.
ass = Asana_workspace(token=asana_token, workspace_id=workspace_id,
                      interested_in=interested_in)
# parse the org file.
org = Orgtopia(path=org_file)
org.process(ass)
org.write()

print(ass.me["name"])
