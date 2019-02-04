import appdaemon.plugins.hass.hassapi as hass
import aiohttp

#
# testing the hass api
#

class test_cal(hass.Hass):

    def initialize(self):
        self.log_cal()
        
    def load_cal(self):
        conn = aiohttp.TCPConnector()
        self.session = aiohttp.ClientSession(connector=conn)
        ha_url = "http://hassio/homeassistant"
        token = self.args["token"]
        headers = {'Authorization': "Bearer {}".format(token)}
        self.log("Try to load calendars")
        apiurl = "{}/api/config".format(ha_url)
        self.log("ha_config: url is {}".format(apiurl))
        r = self.session.get(apiurl, headers=headers, verify_ssl=False)
        r.raise_for_status()
        return r.json()
        
    def log_cal(self):
        resp = self.load_cal()
        self.log(resp)
