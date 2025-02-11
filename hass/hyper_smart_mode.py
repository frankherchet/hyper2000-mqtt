# To get the logs:
# tail -f home-assistant.log | grep pyscript 
# This script is currently provided 'as it is'. You have to manually add some helpers:
# - input_boolean.hyper2000_smart_ct (to enable/disable the smart mode)
# - input_number.hyper2k_charging_offset (to set the offset for charging, -100 to 100)
# - input_number.hyper2k_discharging_offset (to set the offset for discharging, -100 to 100)
# 
# Additionally, you need the following entities:
# - sensor.solarflow_ac_mode (0=off, 1=charging, 2=discharging)
# - sensor.solarflow_output_home_power (current power output of the battery)
# - sensor.solarflow_grid_input_power (current power input of the battery)
# - sensor.shellypro3em_08f9e0e6cb74_total_active_power (current power consumption of the house)
#
# You need HACS and pyscript installed
# copy the following file to the pyscript folder
#

@state_trigger("sensor.shellypro3em_08f9e0e6cb74_total_active_power")
@service
def update_hyper_smart_mode():
    # Smart-CT-Modus aktiv?
    hyper2000_smart_ct = state.get("input_boolean.hyper2000_smart_ct") == "on"
    log.info(f"hyper2000_smart_ct: {hyper2000_smart_ct}")
    
    # Konstante AC-Modi
    BAT_DISCHARGING, BAT_CHARGING = 2, 1
    
    # Offset-Werte abrufen
    charging_offset = int(float(state.get("input_number.hyper2k_charging_offset")))
    discharging_offset = int(float(state.get("input_number.hyper2k_discharging_offset")))
    log.info(f"Charging Offset: {charging_offset}, Discharging Offset: {discharging_offset}")

    # Sensordaten einlesen & umwandeln
    total_power_to_grid = float(state.get("sensor.shellypro3em_08f9e0e6cb74_total_active_power"))
    bat_ac_mode = int(state.get("sensor.solarflow_ac_mode"))
    bat_discharging = int(state.get("sensor.solarflow_output_home_power"))
    bat_charging = int(state.get("sensor.solarflow_grid_input_power"))
    
    # Debug-Logging
    log.info(f"total_power_to_grid: {total_power_to_grid} W | "
             f"bat_discharging: {bat_discharging} W | "
             f"bat_charging: {bat_charging} W")
    
    # Berechnung neuer Werte
    new_bat_discharging = new_bat_charging = 0
    new_ac_mode = bat_ac_mode
    
    household_power_demand = total_power_to_grid + bat_discharging - bat_charging
    
    if household_power_demand > discharging_offset:
        new_bat_discharging = int(household_power_demand - discharging_offset)
        new_ac_mode = BAT_DISCHARGING
    else: 
        new_bat_discharging = 0
    
    if household_power_demand < charging_offset:
        new_bat_charging = int(household_power_demand + charging_offset)
        new_ac_mode = BAT_CHARGING
    else:
        new_bat_charging = 0
  
    # Do not send out values higher than 1200
    new_bat_discharging = min(new_bat_discharging, 1200)
    new_bat_charging = min(new_bat_charging, 1200)
    
    log.info(f"household_power_demand: {household_power_demand}W | new_bat_discharging: {new_bat_discharging} | new_bat_charging: {new_bat_charging}")

    if hyper2000_smart_ct:
        # Werte für die Batterie setzen
        service.call("number", "set_value", entity_id="number.solarflow_set_output_limit", value=new_bat_discharging)
        service.call("number", "set_value", entity_id="number.solarflow_set_input_limit_2", value=new_bat_charging)

        # AC-Modus schalten
        if new_ac_mode == BAT_CHARGING and bat_ac_mode == BAT_DISCHARGING:
            log.info("Switching to Charging Mode")
            service.call("switch", "turn_on", entity_id="switch.solarflow_ac_mode")
        elif new_ac_mode == BAT_DISCHARGING and bat_ac_mode == BAT_CHARGING:
            log.info("Switching to Discharging Mode")
            service.call("switch", "turn_off", entity_id="switch.solarflow_ac_mode")
        else:
            log.info(f"Keeping AC Mode {bat_ac_mode}")
            
    else:
        log.info("Smart CT mode not active")

    log.info(f"AC Mode: {bat_ac_mode} → {new_ac_mode} | "
             f"Charging: {bat_charging} → {new_bat_charging} | "
             f"Discharging: {bat_discharging} → {new_bat_discharging}")
    log.info(f"### DONE ###")
