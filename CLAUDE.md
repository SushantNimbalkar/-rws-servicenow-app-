# ServiceNow development rules

## How to talk to the instance
- Install deps first: `pip install -r requirements.txt`
- Use only `python sn.py get|create|update <table> ...`
  - get: `python sn.py get sys_script_include "name=MyUtil" "sys_id,name,script"`
  - newest first: `python sn.py get sys_script_include "ORDERBYDESCsys_updated_on" "sys_id,name,sys_updated_on" 5`
  - create: `python sn.py create sys_script_include '{"name":"MyUtil","script":"..."}'`
  - update: `python sn.py update sys_script_include <sys_id> '{"script":"..."}'`
- For multi-line scripts, build the JSON with a small Python snippet that reads
  the file from `src/` (json.dumps) instead of hand-escaping it in the shell.
- Credentials come from environment variables (SN_INSTANCE, SN_USER, SN_PASS).
  Never print or commit them.

## Update sets
- Before any change, make sure the current update set for user claude.dev
  is the one in $SN_UPDATE_SET:
  1. Get the user's sys_id: `python sn.py get sys_user "user_name=claude.dev" "sys_id"`
  2. Check `sys_user_preference` with query `name=sys_update_set^user=<user sys_id>`.
  3. If it exists, update its `value` to $SN_UPDATE_SET; otherwise create it with
     `{"name":"sys_update_set","user":"<user sys_id>","value":"$SN_UPDATE_SET"}`.
- After a change, confirm it was captured: `sys_update_xml` with query
  `update_set=$SN_UPDATE_SET^ORDERBYDESCsys_updated_on`.

## Rules
- Always read existing records before changing them.
- Never delete records. Never touch sys_user, sys_user_role or sys_properties
  unless asked (reading sys_user to look up claude.dev's sys_id is fine).
- Keep a copy of every script you push in `src/<table>/<name>.js` and commit it.
- After each change, report the table, sys_id and a link:
  $SN_INSTANCE/nav_to.do?uri=<table>.do?sys_id=<sys_id>

## Key tables
sys_script_include, sys_script (business rules), sys_script_client,
sys_ui_policy, sys_security_acl, sc_cat_item, item_option_new,
sp_widget, sys_ui_action
