import appdaemon.plugins.hass.hassapi as hass
#
# App does:
#  - Send notification on status change of aqara cube (testing)
#

class test_cube(hass.Hass):

    def initialize(self):
        self.listen_state(self.action, "sensor.aqara_cube_1_action")
        self.listen_state(self.side, "sensor.cube_1_side")
        
    def action(self, entity, attribute, old, new, kwargs):
        if new != "":
            side = self.get_state("sensor.cube_1_side")
            self.fire_event("custom_notify", message="Cube Action changed: {} / Side zu dem Zeitpunkt: {}".format(new.replace("_"," "),side), target="telegram_jo")

    def side(self, entity, attribute, old, new, kwargs):
        self.fire_event("custom_notify", message="Cube Side changed: {}".format(new), target="telegram_jo")
