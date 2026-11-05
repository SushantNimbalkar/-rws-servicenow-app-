/**
 * Script Include: RWSUtils
 *
 * Basic server-side utility class for the RWS ServiceNow app.
 *
 * Record settings (System Definition > Script Includes):
 *   Name:            RWSUtils
 *   API Name:        global.RWSUtils (or <your_scope>.RWSUtils)
 *   Client callable: false
 *   Accessible from: All application scopes
 *   Active:          true
 *
 * Usage (server-side script, business rule, background script):
 *   var utils = new RWSUtils();
 *   gs.info(utils.getUserFullName(gs.getUserID()));
 */
var RWSUtils = Class.create();
RWSUtils.prototype = {
    initialize: function() {
        this.LOG_SOURCE = 'RWSUtils';
    },

    /**
     * Returns the display name of a user.
     * @param {string} userSysId - sys_id of a sys_user record
     * @returns {string} the user's name, or '' if not found
     */
    getUserFullName: function(userSysId) {
        if (!userSysId) {
            return '';
        }
        var user = new GlideRecord('sys_user');
        if (user.get(userSysId)) {
            return user.getValue('name') || '';
        }
        this._log('User not found: ' + userSysId);
        return '';
    },

    /**
     * Checks whether a user belongs to a group.
     * @param {string} userSysId - sys_id of a sys_user record
     * @param {string} groupName - name of a sys_user_group record
     * @returns {boolean}
     */
    isUserInGroup: function(userSysId, groupName) {
        if (!userSysId || !groupName) {
            return false;
        }
        var member = new GlideRecord('sys_user_grmember');
        member.addQuery('user', userSysId);
        member.addQuery('group.name', groupName);
        member.setLimit(1);
        member.query();
        return member.hasNext();
    },

    /**
     * Counts records in a table matching an encoded query.
     * @param {string} tableName - e.g. 'incident'
     * @param {string} encodedQuery - e.g. 'active=true^priority=1'
     * @returns {number}
     */
    getRecordCount: function(tableName, encodedQuery) {
        if (!tableName) {
            return 0;
        }
        var ga = new GlideAggregate(tableName);
        if (encodedQuery) {
            ga.addEncodedQuery(encodedQuery);
        }
        ga.addAggregate('COUNT');
        ga.query();
        return ga.next() ? parseInt(ga.getAggregate('COUNT'), 10) : 0;
    },

    _log: function(message) {
        gs.info('[' + this.LOG_SOURCE + '] ' + message);
    },

    type: 'RWSUtils'
};
