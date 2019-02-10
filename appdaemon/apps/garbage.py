import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# App to handle garbage topics
#
# Args: no args required
# 

class garbage(hass.Hass):

    def initialize(self):
        # --- calendar and sensor names ---
        self.calendar_waste = "calendar.restmuelltonne"
        self.calendar_organic = "calendar.biotonne"
        self.calendar_paper = "calendar.papiertonne"
        self.calendar_plastic = "calendar.raweg"
        self.sensor_display_waste = "sensor.restmuelltonne_anzeige"
        self.sensor_display_organic = "sensor.biotonne_anzeige"
        self.sensor_display_paper = "sensor.papiertonne_anzeige"
        self.sensor_display_plastic = "sensor.raweg_anzeige"
        self.switch_reminder_waste = "switch.restmuelltonne_erinnerung"
        self.switch_reminder_organic = "switch.biotonne_erinnerung"
        self.switch_reminder_paper = "switch.papiertonne_erinnerung"
        self.switch_reminder_plastic = "switch.raweg_erinnerung"
        self.icon_waste = "/local/icons/garbage/tonne_schwarz.svg"
        self.icon_organic = "/local/icons/garbage/tonne_braun.svg"
        self.icon_paper = "/local/icons/garbage/tonne_blau.svg"
        self.icon_plastic = "/local/icons/garbage/tonne_gelb.svg"
        self.icon_waste_blink = "/local/icons/garbage/tonne_schwarz_blink.svg"
        self.icon_organic_blink = "/local/icons/garbage/tonne_braun_blink.svg"
        self.icon_paper_blink = "/local/icons/garbage/tonne_blau_blink.svg"
        self.icon_plastic_blink = "/local/icons/garbage/tonne_gelb_blink.svg"
        # --- reminder ---
        time_check_next_day = datetime.time(17, 00, 0)
        self.run_daily(self.check_next_day, time_check_next_day)
        # --- update text at midnight ---
        time_midnight = datetime.time(0, 00, 30)
        self.run_daily(self.midnight, time_midnight)
        # --- listen for calendar updates
        self.listen_state(self.end_waste, self.calendar_waste, attribute="end_time")
        self.listen_state(self.end_organic, self.calendar_organic, attribute="end_time")
        self.listen_state(self.end_paper, self.calendar_paper, attribute="end_time")
        self.listen_state(self.end_plastic, self.calendar_plastic, attribute="end_time")
        # --- restarts ---
        self.listen_event(self.startup, "plugin_started")
        self.listen_event(self.startup, "appd_started")
        # --- initialize sensors and switches
        self.create_display_sensors(None)
        self.create_reminder_switches(None)
        self.update_all_displays(None)
        # --- listen for events of self created switches (they are not handeled by HA)
        self.listen_event(self.toggle_switches, event = "call_service")
        
    def check_next_day(self, kwargs):
        self.log("Checking if tomorrow is some garbage collection")
        # check waste
        if self.calc_days(self.calendar_waste) == 1:
            self.log("Tomorrow is waste collection")
            self.set_state(self.switch_reminder_waste, state = "on")
            self.notify("Morgen ist Restmülltonne", name = "telegram_jo")
        # check organic
        if self.calc_days(self.calendar_organic) == 1:
            self.log("Tomorrow is organic waste collection")
            self.set_state(self.switch_reminder_organic, state = "on")
            self.notify("Morgen ist Biotonne", name = "telegram_jo")
        # check paper
        if self.calc_days(self.calendar_paper) == 1:
            self.log("Tomorrow is paper collection")
            self.set_state(self.switch_reminder_paper, state = "on")
            self.notify("Morgen ist Papiertonne", name = "telegram_jo")
        # check plastic
        if self.calc_days(self.calendar_plastic) == 1:
            self.log("Tomorrow is plastic collection")
            self.set_state(self.switch_reminder_plastic, state = "on")
            self.notify("Morgen ist RaWeg", name = "telegram_jo")

    def end_waste(self, entity, attribute, old, new, kwargs):
        self.update_waste_display(None)
        self.log("Reseting waste reminder")
        self.set_state(self.switch_reminder_waste, state = "off")

    def end_organic(self, entity, attribute, old, new, kwargs):
        self.update_organic_display(None)
        self.log("Reseting organic waste reminder")
        self.set_state(self.switch_reminder_organic, state = "off")

    def end_paper(self, entity, attribute, old, new, kwargs):
        self.update_paper_display(None)
        self.log("Reseting paper reminder")
        self.set_state(self.switch_reminder_paper, state = "off")

    def end_plastic(self, entity, attribute, old, new, kwargs):
        self.update_plastic_display(None)
        self.log("Reseting plastic reminder")
        self.set_state(self.switch_reminder_plastic, state = "off")
    
    def update_waste_display(self, kwargs):
        self.log("Updating Waste Display Sensor")
        self.create_text(self.calendar_waste, self.sensor_display_waste)

    def update_organic_display(self, kwargs):
        self.log("Updating Organic Waste Display Sensor")
        self.create_text(self.calendar_organic, self.sensor_display_organic)

    def update_paper_display(self, kwargs):
        self.log("Updating Paper Display Sensor")
        self.create_text(self.calendar_paper, self.sensor_display_paper)

    def update_plastic_display(self, kwargs):
        self.log("Updating Plastic Display Sensor")
        self.create_text(self.calendar_plastic, self.sensor_display_plastic)

    def midnight(self, kwargs):
        self.log("Midnight - Updating All Waste Display Sensors")
        self.update_all_displays(None)

    def startup(self, event_name, data, kwargs):
        self.log("Garbage: Startup detected. Updating all the stuff now")
        self.create_display_sensors(None)
        self.create_reminder_switches(None)
        self.update_all_displays(None)

    def update_all_displays(self, kwargs):
        self.update_waste_display(None)
        self.update_organic_display(None)
        self.update_paper_display(None)
        self.update_plastic_display(None)

    def toggle_switches(self,event_name,data, kwargs):
        # waste
        if(data["service"] == "turn_off" and data["service_data"]["entity_id"] == self.switch_reminder_waste):
            self.log(self.switch_reminder_waste + " switched off")
            self.set_state(self.switch_reminder_waste, state = "off")
        if(data["service"] == "turn_on" and data["service_data"]["entity_id"] == self.switch_reminder_waste):
            self.log(self.switch_reminder_waste + " switched on")
            self.set_state(self.switch_reminder_waste, state = "on")
        # organic
        if(data["service"] == "turn_off" and data["service_data"]["entity_id"] == self.switch_reminder_organic):
            self.log(self.switch_reminder_organic + " switched off")
            self.set_state(self.switch_reminder_organic, state = "off")
        if(data["service"] == "turn_on" and data["service_data"]["entity_id"] == self.switch_reminder_organic):
            self.log(self.switch_reminder_organic + " switched on")
            self.set_state(self.switch_reminder_organic, state = "on")
        # paper
        if(data["service"] == "turn_off" and data["service_data"]["entity_id"] == self.switch_reminder_paper):
            self.log(self.switch_reminder_paper + " switched off")
            self.set_state(self.switch_reminder_paper, state = "off")
        if(data["service"] == "turn_on" and data["service_data"]["entity_id"] == self.switch_reminder_paper):
            self.log(self.switch_reminder_paper + " switched on")
            self.set_state(self.switch_reminder_paper, state = "on")
        # plastic
        if(data["service"] == "turn_off" and data["service_data"]["entity_id"] == self.switch_reminder_plastic):
            self.log(self.switch_reminder_plastic + " switched off")
            self.set_state(self.switch_reminder_plastic, state = "off")
        if(data["service"] == "turn_on" and data["service_data"]["entity_id"] == self.switch_reminder_plastic):
            self.log(self.switch_reminder_plastic + " switched on")
            self.set_state(self.switch_reminder_plastic, state = "on")

    def create_reminder_switches(self, kwargs):
        if self.entity_exists(self.switch_reminder_waste):
            curr_state = self.get_state(self.switch_reminder_waste)
            self.set_state(self.switch_reminder_waste, state = curr_state, attributes={"entity_picture":self.icon_waste_blink})
        else:
            self.set_state(self.switch_reminder_waste, state = "off", attributes={"entity_picture":self.icon_waste_blink})
        if self.entity_exists(self.switch_reminder_organic):
            curr_state = self.get_state(self.switch_reminder_organic)
            self.set_state(self.switch_reminder_organic, state = curr_state, attributes={"entity_picture":self.icon_organic_blink})
        else:
            self.set_state(self.switch_reminder_organic, state = "off", attributes={"entity_picture":self.icon_organic_blink})
        if self.entity_exists(self.switch_reminder_paper):
            curr_state = self.get_state(self.switch_reminder_paper)
            self.set_state(self.switch_reminder_paper, state = curr_state, attributes={"entity_picture":self.icon_paper_blink})
        else:
            self.set_state(self.switch_reminder_paper, state = "off", attributes={"entity_picture":self.icon_paper_blink})
        if self.entity_exists(self.switch_reminder_plastic):
            curr_state = self.get_state(self.switch_reminder_plastic)
            self.set_state(self.switch_reminder_plastic, state = curr_state, attributes={"entity_picture":self.icon_plastic_blink})
        else:
            self.set_state(self.switch_reminder_plastic, state = "off", attributes={"entity_picture":self.icon_plastic_blink})

    def create_display_sensors(self, kwargs):
        if self.entity_exists(self.sensor_display_waste):
            curr_state = self.get_state(self.sensor_display_waste)
            self.set_state(self.sensor_display_waste, state = curr_state, attributes={"entity_picture":self.icon_waste})
        else:
            self.set_state(self.sensor_display_waste, state = "warte...", attributes={"entity_picture":self.icon_waste})
        if self.entity_exists(self.sensor_display_organic):
            curr_state = self.get_state(self.sensor_display_organic)
            self.set_state(self.sensor_display_organic, state = curr_state, attributes={"entity_picture":self.icon_organic})
        else:
            self.set_state(self.sensor_display_organic, state = "warte...", attributes={"entity_picture":self.icon_organic})
        if self.entity_exists(self.sensor_display_paper):
            curr_state = self.get_state(self.sensor_display_paper)
            self.set_state(self.sensor_display_paper, state = curr_state, attributes={"entity_picture":self.icon_paper})
        else:
            self.set_state(self.sensor_display_paper, state = "warte...", attributes={"entity_picture":self.icon_paper})
        if self.entity_exists(self.sensor_display_plastic):
            curr_state = self.get_state(self.sensor_display_plastic)
            self.set_state(self.sensor_display_plastic, state = curr_state, attributes={"entity_picture":self.icon_plastic})
        else:
            self.set_state(self.sensor_display_plastic, state = "warte...", attributes={"entity_picture":self.icon_plastic})

    def create_text(self, calendar_name, display_sensor_name):
        weekdays = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        days = self.calc_days(calendar_name)
        if days == 0:
            printtext = "heute"
        elif days == 1:
            printtext = "morgen"
        else:
            end_time_datetime = self.get_end_time(calendar_name)
            printtext = end_time_datetime.strftime('{}, %d.%m. ({} T.)').format(weekdays[end_time_datetime.weekday()], days)
        self.set_state(display_sensor_name, state=printtext)
        self.log(printtext)
        
    def calc_days(self, calendar_name):
        end_time_datetime = self.get_end_time(calendar_name)
        days = (end_time_datetime.date() - self.datetime().date()).days
        return days

    def get_end_time(self, calendar_name):
        end_time_str = self.get_state(calendar_name, attribute="end_time")
        end_time_datetime = datetime.datetime.strptime(end_time_str,"%Y-%m-%d %H:%M:%S")
        return end_time_datetime
