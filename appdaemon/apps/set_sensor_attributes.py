import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# App does:
#  - Some KNX sensors don't get a "unit_of_measurement" or an icon at startup. This app shall update them after some delay
#
# Args:
# none

class set_sensor_attributes(hass.Hass):

    def initialize(self):
        # listen for new values
        self.run_in(self.set_attributes, 60)
  
    def set_attributes(self, kwargs):
        for sensor in self.get_state("sensor"):
            if sensor.startswith("sensor.el_leistung"):
                self.set_state(sensor, attributes={"icon":"mdi:speedometer", "unit_of_measurement": "W"})
            if sensor.startswith("sensor.stromzahler"):
                self.set_state(sensor, attributes={"icon":"mdi:counter", "unit_of_measurement": "kWh"})
            if sensor.startswith("sensor.helligkeit"):
                self.set_state(sensor, attributes={"icon":"mdi:weather-sunny", "unit_of_measurement": "lx"})
            if sensor.startswith("sensor.windgeschwindigkeit"):
                self.set_state(sensor, attributes={"icon":"mdi:weather-windy", "unit_of_measurement": "km/h"})