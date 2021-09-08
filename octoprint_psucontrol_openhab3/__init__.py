# coding=utf-8
from __future__ import absolute_import

__author__ = "Philipp Große <philipp.grosse@protonmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2021 Philipp Große - Released under terms of the AGPLv3 License"

import octoprint.plugin
import base64
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class psucontrol_openhab3(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.RestartNeedingPlugin,
                         octoprint.plugin.TemplatePlugin,
                         octoprint.plugin.SettingsPlugin):

    def __init__(self):
        self.config = dict()

    def get_settings_defaults(self):
        return dict(
            address = '',
            authorizationMethod = '',
            api_key = '',
            basic_username = '',
            basic_password = '',
            item_name = '',
            verify_certificate = True,
        )

    def on_settings_initialized(self):
        self.reload_settings()

    def reload_settings(self):
        for k, v in self.get_settings_defaults().items():
            if type(v) == str:
                v = self._settings.get([k])
            elif type(v) == int:
                v = self._settings.get_int([k])
            elif type(v) == float:
                v = self._settings.get_float([k])
            elif type(v) == bool:
                v = self._settings.get_boolean([k])

            self.config[k] = v
            self._logger.debug("{}: {}".format(k, v))

    def on_startup(self, host, port):
        psucontrol_helpers = self._plugin_manager.get_helpers("psucontrol")
        if not psucontrol_helpers or 'register_plugin' not in psucontrol_helpers.keys():
            self._logger.warning("The version of PSUControl that is installed does not support plugin registration.")
            return

        self._logger.debug("Registering plugin with PSUControl")
        psucontrol_helpers['register_plugin'](self)

    def send(self, cmd, data=None):
        url = self.config['address'] + '/rest/items/' + cmd

        if ( self.config['authorizationMethod'] == 'BASIC' ):
            credentials = self.config['basic_username'] + ':' + self.config['basic_password']
            # Standard Base64 Encoding
            encodedBytes = base64.b64encode(credentials.encode("utf-8"))
            basicAuth = str(encodedBytes, "utf-8")
            headers = dict(Authorization='Basic ' + basicAuth)
        else:
            headers = dict(Authorization='X-OPENHAB-TOKEN: ' + self.config['api_key'])    

        response = None
        verify_certificate = self.config['verify_certificate']
        try:
            if data:
                response = requests.post(url, headers=headers, data=data, verify=verify_certificate)
            else:
                response = requests.get(url, headers=headers, verify=verify_certificate)
        except (
                requests.exceptions.InvalidURL,
                requests.exceptions.ConnectionError
        ):
            self._logger.error("Unable to communicate with server. Check settings.")
        except Exception:
            self._logger.exception("Exception while making API call")
        else:
            if data:
                self._logger.debug("cmd={}, headers{}, data={}, status_code={}, text={}".format(cmd, headers, data, response.status_code, response.text))
            else:
                self._logger.debug("cmd={}, headers{}, status_code={}, text={}".format(cmd, headers, response.status_code, response.text))

            if response.status_code == 401:
                self._logger.warning("Server returned 401 Unauthorized. Check API key or Username/Password.")
                response = None
            elif response.status_code == 404:
                self._logger.warning("Server returned 404 Not Found. Check Item Name.")
                response = None

        return response

    def change_psu_state(self, state):
        _item_name = self.config['item_name']
        # _domainsplit = _item_name.find('.')
        # if _domainsplit < 0:
        #     _domain = 'switch'
        #     _item_name = _domain + '.' + _item_name
        # else:
        #     _domain = _item_name[:_domainsplit]

        # if state:
        #    cmd = _item_name + '/state'
        # else:
        cmd = _item_name
        data = state
        self.send(cmd, data)

    def turn_psu_on(self):
        self._logger.debug("Switching PSU On")
        self.change_psu_state('ON')

    def turn_psu_off(self):
        self._logger.debug("Switching PSU Off")
        self.change_psu_state('OFF')

    def get_psu_state(self):
        _item_name = self.config['item_name']
        # _domainsplit = _item_name.find('.')
        # if _domainsplit < 0:
        #     _item_name = 'switch.' + _item_name

        cmd = _item_name + '/state'

        response = self.send(cmd)
        if not response:
            return False
        data = response.text()

        status = None
        try:
            status = (data == 'ON')
        except KeyError:
            pass

        if status == None:
            self._logger.error("Unable to determine status. Check settings.")
            status = False

        return status

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.reload_settings()

    def get_settings_version(self):
        return 1

    def on_settings_migrate(self, target, current=None):
        pass

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_update_information(self):
        return dict(
            psucontrol_openhab3=dict(
                displayName="PSU Control - openHAB3",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="Tomatenjoghurt",
                repo="OctoPrint-PSUControl-openHAB3",
                current=self._plugin_version,

                # update method: pip w/ dependency links
                pip="https://github.com/Tomatenjoghurt/OctoPrint-PSUControl-openHAB3/archive/{target_version}.zip"
            )
        )

__plugin_name__ = "PSU Control - openHAB3"
__plugin_pythoncompat__ = ">=3,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = psucontrol_openhab3()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }