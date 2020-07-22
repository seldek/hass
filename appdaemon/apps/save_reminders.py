import appdaemon.plugins.hass.hassapi as hass
import time

#
# make custom reminders survive a restart
#
# Args: 
# 

class save_reminders(hass.Hass):

    def initialize(self):
        self.set_textvalue("input_text.saved_reminder_01", "wiederhergestellteerinnerung::Test: Tu was::/local/icons/reminders/exclamation_mark_blink.svg")
        
        time.sleep(1)
        text = self.get_state("input_text.saved_reminder_01")
        if len(text.split("::")) == 3:
            switch_name = "switch.reminder_" + text.split("::")[0]
            friendly_name = text.split("::")[1]
            icon = text.split("::")[2]
#            self.set_state(switch_name, state = "on", attributes={"entity_picture":icon, "friendly_name": friendly_name})
        else:
            self.log("input_text sollte 2 mal :: enthalten")
        
        for switch in self.get_state("switch"):
            self.log(switch)
            if switch.startswith("switch.reminder_"):
                self.log("reminder!")
                if self.get_state(switch) == "on":
                    self.log("der ist aktiv!")

                
        #self.listen_state(self.illuminance_changed, self.args["illuminance_sensor"])

    def illuminance_changed(self, entity, attributes, old, new, kwargs):
        pass
