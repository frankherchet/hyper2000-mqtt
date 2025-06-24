## List of Available MQTT Entities

### From HYPER2000

| Attribute             | Writable | Description                                                        |
|-----------------------|----------|--------------------------------------------------------------------|
| OldMode               | Yes/No   | Legacy mode?                                                       |
| acMode                | Yes      | AC mode (1=Input, 2=Output)                                        |
| ambientLightColor     | Yes/No   | Ambient light color? (default: 65280)                              |
| ambientLightMode      | Yes/No   | Ambient light mode?                                                |
| ambientLightNess      | Yes/No   | Ambient light brightness? (default: 20)                            |
| ambientSwitch         | Yes/No   | Ambient light switch?                                              |
| autoHeat              | Yes/No   | Automatic heating enabled?                                         |
| autoModel             | Yes/No   | Automatic model selection?                                         |
| batVolt               | No       | Battery voltage                                                    |
| blueOta               | Yes/No   | Over the air?                                                      |
| buzzerSwitch          | Yes/No   | Buzzer switch?                                                     |
| chargingMode          | Yes/No   | Charging mode?                                                     |
| chargingTime          | No       | Charging time                                                      |
| chargingType          | Yes/No   | Charging type?                                                     |
| circuitCheckMode      | Yes/No   | Circuit check mode?                                                |
| clusterSw             | Yes/No   | Cluster switch?                                                    |
| ctOff                 | Yes/No   | CT Mode off?                                                       |
| electricLevel         | No       | Battery level in % (0-100)                                         |
| energyPower           | No       | Energy power                                                       |
| getAll                | Yes      | Get all properties                                                 |
| gridInputPower        | No       | Input power from grid in W                                         |
| gridInputPowerCycle   | Yes/No   | Grid input power cycle?                                            |
| gridOffMode           | Yes/No   | Grid-off mode?                                                     |
| gridReverse           | Yes      | Grid reverse mode (0=Auto, 1=On, 2=Off)                            |
| gridStandard          | Yes/No   | Grid standard?                                                     |
| heatState             | Yes/No   | Current heating state?                                             |
| hubState              | No       | Hub state                                                          |
| hyperTmp              | No       | Device temperature ((t - 2731) / 10)                               |
| inputLimit            | Yes      | Input power limit from the grid                                    |
| inputMode             | Yes/No   | Input Mode?                                                        |
| invOutputPower        | Yes      | Inverter output power?                                             |
| inverseMaxPower       | Yes      | Maximum inverter power (0-1200)                                    |
| lampSwitch            | Yes      | Lamp switch (0=Off, 1=On)                                          |
| localState            | No       | Local state                                                        |
| lowTemperature        | Yes/No   | Low temperature (0/1)                                              |
| masterSoftVersion     | No       | Master software version                                            |
| masterSwitch          | Yes/No   | Master switch (0=Off, 1=On)                                        |
| masterhaerVersion     | No       | Master hardware version                                            |
| minSoc                | Yes      | Minimum state of charge (%)                                        |
| outputHomePower       | No       | Output power to home in W                                          |
| outputHomePowerCycle  | No       | Output home power cycle?                                           |
| outputLimit           | Yes      | Output power limit to the grid                                     |
| outputPackPower       | No       | Battery power in in W                                              |
| outputPackPowerCycle  | Yes/No   | Battery output power cycle?                                        |
| packInputPower        | No       | Battery power out in W                                             |
| packInputPowerCycle   | Yes/No   | Battery input power cycle?                                         |
| packNum               | No       | Number of battery packs (0-4)                                      |
| packState             | No       | Battery pack state (0=Standby, 1=Input, 2=Output)                  |
| pass                  | No       | Bypass mode (0=Auto, 1=On, 2=Off)                                  |
| phaseCheck            | Yes/No   | Phase check?                                                       |
| phaseSwitch           | Yes/No   | Phase switch?                                                      |
| plugState             | Yes/No   | Plug connection state?                                             |
| pvBrand               | Yes/No   | PV brand/model?                                                    |
| remainInputTime       | No       | Remaining current charging time                                    |
| remainOutTime         | No       | Remaining current discharging time                                 |
| reverseState          | No       | Reverse state, bypass to grid allow (0=Yes, 1=No)                  |
| socSet                | Yes/No   | Set Maximum SOC (0-1000=100%)                                      |
| socStatus             | No       | State of charge status?                                            |
| solarInputPower       | No       | Solar input power in W                                             |
| solarPower1           | No       | Solar power channel 1 in W                                         |
| solarPower1Cycle      | No       | Solar power 1 cycle?                                               |
| solarPower2           | No       | Solar power channel 2 in W                                         |
| solarPower2Cycle      | No       | Solar power 2 cycle?                                               |
| strength              | No       | WiFi Signal strength (0-3)                                         |
| voltWakeup            | Yes/No   | Voltage threshold for wakeup?                                      |
| wifiState             | No       | WiFi connection state (0=Disconnected, 1=Connected)                |

> **Note:**  
> The "Writable" column indicates if the attribute can be set via MQTT. Please refer to the device documentation or test with caution, as not all attributes may be writable.

### From Each Battery Pack

| Attribute   | Writable | Description                                  |
|-------------|----------|----------------------------------------------|
| sn          | No       | Serial number                                |
| power       | No       | Battery pack power in W                      |
| socLevel    | No       | State of charge level (%)                    |
| state       | No       | Battery pack state (0=Standby, 1=Input, 2=Output) |
| maxTemp     | No       | Maximum temperature (raw value)              |
| totalVol    | No       | Total voltage (raw value)                    |
| maxVol      | No       | Maximum cell voltage (raw value)             |
| minVol      | No       | Minimum cell voltage (raw value)             |
| softVersion | No       | Battery pack software version                |
| batcur      | No       | Battery current (raw value)                  |
