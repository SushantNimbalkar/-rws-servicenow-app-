# RWS ServiceNow App

ServiceNow application repository.

## Script Includes

| Name | File | Description |
| --- | --- | --- |
| `RWSUtils` | [`src/sys_script_include/RWSUtils.js`](src/sys_script_include/RWSUtils.js) | Basic server-side helpers: user name lookup, group membership check, record count. |

### Install

1. In ServiceNow, open **System Definition > Script Includes** and click **New**.
2. Set **Name** to `RWSUtils`, leave **Client callable** unchecked, and make sure **Active** is checked.
3. Paste the contents of `src/sys_script_include/RWSUtils.js` into **Script** and save.

### Try it (Scripts - Background)

```javascript
var utils = new RWSUtils();
gs.info(utils.getUserFullName(gs.getUserID()));
gs.info(utils.isUserInGroup(gs.getUserID(), 'Service Desk'));
gs.info(utils.getRecordCount('incident', 'active=true'));
```
