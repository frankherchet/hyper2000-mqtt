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
    # Constants AC-Modi
    AC_OUT, AC_IN = 2, 1
    BYPASS_MODE_ON, BYPASS_MODE_OFF, BYPASS_MODE_AUTO = 2, 1, 0
    
    # Smart-CT-Modus aktiv?
    hyper2k_smart_mode = state.get("input_boolean.hyper2000_smart_ct") == "on"
    hyper2k_smart_bypass_mode = state.get("input_boolean.hyper2k_smart_bypass_mode") == "on"
    log.info(f"SMART MODE: {hyper2k_smart_mode} | BYPASS MODE: {hyper2k_smart_bypass_mode}")
    hyper2k_soc = float(state.get("sensor.solarflow_electric_level"))
    hyper2k_soc_max = float(state.get("sensor.hyper2k_soc_max"))
    
    # Sensordaten einlesen & umwandeln
    total_power_to_grid = float(state.get("sensor.shellypro3em_08f9e0e6cb74_total_active_power"))
    bat_ac_mode = int(state.get("sensor.hyper2k_ac_mode"))
    ac_power_out = int(state.get("sensor.solarflow_output_home_power"))
    ac_power_in = int(state.get("sensor.solarflow_grid_input_power"))
    solar_input_power = int(state.get("sensor.solarflow_solar_input_power"))
    bypass_mode = state.get("sensor.solarflow_pass_mode")
    
    old_ac_mode = "AC_MODE_IN" if bat_ac_mode == AC_IN else "AC_MODE_OUT"
    if bypass_mode == BYPASS_MODE_ON:
        old_ac_mode = "AC_MODE_BYPASS"
        
    log.info(f"old_ac_mode: {old_ac_mode} | bypass_mode: {bypass_mode}")
    
    # Offset-Werte abrufen
    charging_offset = int(float(state.get("input_number.hyper2k_charging_offset")))
    discharging_offset = int(float(state.get("input_number.hyper2k_discharging_offset")))
    log.info(f"Charging Offset: {charging_offset}, Discharging Offset: {discharging_offset}")
    
    # Debug-Logging
    log.info(f"total_power_to_grid: {total_power_to_grid} W | "
             f"ac_power_out: {ac_power_out} W | "
             f"ac_power_in: {ac_power_in} W")
    
    # calculate new values
    new_ac_output_limit = new_ac_input_limit = 0
    new_ac_mode = bat_ac_mode
    
    household_power_demand = total_power_to_grid + ac_power_out - ac_power_in
    
    if household_power_demand > discharging_offset:
        new_ac_output_limit = int(household_power_demand - discharging_offset)
        new_ac_mode = AC_OUT
    else: 
        new_ac_output_limit = 0
    
    if household_power_demand < charging_offset:
        new_ac_input_limit = int(abs(household_power_demand) + charging_offset)
        new_ac_mode = AC_IN
    else:
        new_ac_input_limit = 0
        
    # If smart bypass mode is active - no discharging above solar_input_power allowed
    if hyper2k_smart_bypass_mode and solar_input_power > discharging_offset:
        log.info(f"new_bat_discharging will be limited to {solar_input_power} and AC Mode in CHARGING")
        new_ac_output_limit = min(new_ac_output_limit, solar_input_power)
        new_ac_mode = AC_IN
    
    log.info(f"household_power_demand: {household_power_demand:.2f}W | new_ac_output_limit: {new_ac_output_limit:.2f} | new_ac_input_limit: {new_ac_input_limit:.2f}")

    if hyper2k_soc >= hyper2k_soc_max-2 and solar_input_power > discharging_offset:
        log.info(f"Hyper2k SOC is at {hyper2k_soc}%, trying to enforce BYPASS_MODE")
        new_ac_mode = AC_OUT
        new_ac_input_limit = 0
        new_ac_output_limit = discharging_offset
        
    # Do not send out values higher than 1200
    new_ac_output_limit = min(new_ac_output_limit, 1200)
    new_ac_input_limit = min(new_ac_input_limit, 1200)

    if hyper2k_smart_mode:
        # Send new limits to Hyper2k              
        service.call("number", "set_value", entity_id="number.solarflow_set_output_limit", value=new_ac_output_limit)
        service.call("number", "set_value", entity_id="number.solarflow_set_input_limit_2", value=new_ac_input_limit)

        # Set AC-Mode
        if new_ac_mode == AC_IN and bat_ac_mode == AC_OUT:
            if bypass_mode != 2:
                log.info("Switching to Charging Mode")
                service.call("switch", "turn_on", entity_id="switch.solarflow_ac_mode")
                input_text.smart_mode_debug = "-> CHARGING"
            else:
                log.info(f"Switching to Charging Mode not possible due to bypass mode")
        elif new_ac_mode == AC_OUT and bat_ac_mode == AC_IN:
            log.info("Switching to Discharging Mode")
            service.call("switch", "turn_off", entity_id="switch.solarflow_ac_mode")
            input_text.smart_mode_debug = "-> DISCHARGING"
        else:
            log.info(f"Keeping AC Mode {bat_ac_mode}")
            if bat_ac_mode == AC_IN:
                input_text.smart_mode_debug = "CHARGING"
            else:
                input_text.smart_mode_debug = "DISCHARGING"
            
    else:
        log.info("Smart CT mode not active")

    log.info(f"AC Mode: {bat_ac_mode} → {new_ac_mode} | "
             f"Charging: {ac_power_in} → {new_ac_input_limit} | "
             f"Discharging: {ac_power_out} → {new_ac_output_limit}")
    log.info(f"### DONE ###")
    log.info(f"")
