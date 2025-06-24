# HYPER2000 NoCloud
This little tool is able to disconnect / connect your HYPER2000 from ZENDURE cloud. All states and the full controll will be available through a local MQTT-broker.



> [!NOTE]
>
> Please note that this is work in progress. Completely use at you own risk.
## Table of Contents

1. [Supported Devices](#what)
1. [Features](#features)
1. [Why disconnect your SF Hub from the cloud?](#why)
1. [How to use](#howto)
  - [Getting Basic Information](#getting-basic-information)
  - [Disconnecting the HYPER2000 from the cloud](#disconnecting-the-hyper2000-from-the-cloud)
  - [Authorize HYPER2000 to connect to your local MQTT-broker](#authorize-hyper2000-to-connect-to-your-local-mqtt-broker)
    - [Get HYPER2000 user_name and password](#get-hyper2000-user_name-and-password)
    - [Add user to mosquitto](#add-user-to-mosquitto)
    - [Get all properties](#get-all-properties)
  - [Basic MQTT communication](#basic-mqtt-communication)
    - [READ](#read)
    - [WRITE](#write)
    - [Updates on change](#updates-on-change)
  - [Reconnecting HYPER2000 to the cloud](#reconnecting-hyper2000-to-the-cloud)

## Supported Devices <a name="what"></a>
- Hyper2000 (SF_PRODUCT_ID=ja72U0ha _default_)
- Hyper2000 (new product id) (SF_PRODUCT_ID=gDa3tb )


## Features <a name="features"></a>
Currently you can:
- connect to the HYPER2000 by using a BTLE (Bluetooth Low Energy) connection
- retrieve system information (Device ID, Serial No., Battery Pack information, general settings, ...)
- disconnect the HYPER2000 from Zendure's cloud broker and connect it to a local one (offline mode)
- reconnect to Zendure's cloud broker (GLOBAL and EU)

## Why disconnect your SF Hub from the cloud? <a name="why"></a>

- Operate your HYPER2000 completely independant from a cloud connection
- Get fast update rates of state changes
- Get full control over all writable parameters
- Implement your own SMART Mode and adapt it to your needs.
- Integrate your HYPER2000 completely into HOME ASSISTANT

## How to use <a name="howto"></a>
You will need a Bluetooth LE capable system with Python 3. Linux and OSX works. Windows should do the same, but not tested.
The script is searching for a HYPER2000 with a Bluetooth name that starts with "zene". 

### Getting Basic Information
To get basic information about the HYPER2000 (without performing any changes) run the script with the `-i` option only:

```
$ python3 solarflow-bt-manager.py -i
```

After a successful connection you should see some output like this. You will also start seeing lots of JSON output with other device details. Also the divice will start reporting telemetry data. After a few seconds the script will terminate.

```
2023-09-05 13:52:27,534:INFO: Found device: 94:C9:60:3E:C8:E7: ZenP1_38
2023-09-05 13:52:28,393:INFO: Services:
2023-09-05 13:52:28,397:INFO: 00112233-4455-6677-8899-aabbccddeeff (Handle: 18): Unknown
2023-09-05 13:52:28,402:INFO: 0000a002-0000-1000-8000-00805f9b34fb (Handle: 12): Vendor specific
2023-09-05 13:52:28,409:INFO: 00001801-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Attribute Profile
...
2023-09-05 13:52:28,682:INFO: The SF device ID is: 5ak8yGU7
2023-09-05 13:52:28,684:INFO: The SF device SN is: PO1HLC9LDR01938
```

Take a note of the device hardware address, the device ID, and the serial number, you might need that later.

### Disconnecting the HYPER2000 from the cloud
You can completely disconnect the HYPER2000 from the Zendure cloud and connect it to a local MQTT broker. It wont send any data to the cloud but you will also not be able to change any settings with the app. From that point on you can only control the hub via your local MQTT broker. This gives you full control but is for advanced usage (e.g. setting the output limit to any arbitrary value)

> [!NOTE]
> I've tested this setup and I'm currently using it for some time. Use at your own risk! Longterm experience (firmware upgrades etc.) will show how this works over time.

Disconnecting works by reinitializing the HYPER2000 network connection (WiFi) and telling the hub to connect to a different MQTT broker. the AIO to your local broker.  
```
$ pip3 install -r requirements.txt
$ export WIFI_PWD="your_wifi_password"
$ export SF_DEVICE_ID="your_sf_deviceid"
# your_sf_productid is 73bkTV for Hub1200 or A8yh63 for Hub2000 and yWF7hV for AIO2400.
$ export SF_PRODUCT_ID="your_sf_productid"
$ export MQTT_USER="your mqtt user"
$ export MQTT_PWD="mqtt password"
$ python3 solarflow-bt-manager.py -d -w <WiFi SSID> -b <local MQTT broker>
```

example:
```
$ pip3 install -r requirements.txt
$ export WIFI_PWD="Sup3rS3cret!"
$ export SF_DEVICE_ID="5ak8yGU7"
$ export SF_PRODUCT_ID="73bkTV"
$ export MQTT_USER="mqtt"
$ export MQTT_PWD="mqtt_password"
$ python3 solarflow-bt-manager.py -d -w SuperWiFi -b 192.168.1.245
```

This will - if successful - tell the HYPER2000 to disconnect and reconnect the WiFi and then start sendin data to your local MQTT broker. 

### Authorize HYPER2000 to connect to your local MQTT-broker
As all ZENDURE devices, it will connect using a auto generated user_name and password. Thanksfully it was not that hard to get the used user_name and password.

I'm currently using the latest mosquitto docker image:
```
mosquitto version 2.0.20 starting
```
mosquitto has support for anonymous logins, but not any user_name and password. If the client is sending a user_name and password, it must be part of the password file. You can't ignore it. The error will look like this:

```
1739126399: Sending CONNACK to <SF_DEVICE_ID> (0, 5)
1739126399: Client <SF_DEVICE_ID> disconnected, not authorised.
```

#### Get HYPER2000 user_name and password
One way to get the necessary credentials is running tcpdump on the machine where you're running your MQTT-broker:

```
sudo tcpdump -i eth0 src host <IP_ADDRESS_HYPER2K> -w capture.pcap
```

Maybe the easiest way is to generate the used password out of your DEVICE_ID, the password is a part of the md5-hash only with upper letters:

```
echo -n <SF_DEVICE_ID> | md5sum | awk '{print toupper($1)}' | cut -c9-24
```
#### Add user to mosquitto
No add those credentials to mosquitto
```
sudo mosquitto_passwd <path_to_password_file> <SF_DEVICE_ID>
```

You should see now some time-sync topics:

```
Topic: /gDa3tb/<deviceId>/time-sync QoS: 0
{
  "messageId": 7297,
  "deviceId": "<deviceId>",
  "timestamp": 1739183690
}
```
#### Get all properties
Now publish the following MQTT message. Afterwards the HYPER2000 will start updating the topics:

```
iot/gDa3tb/<deviceId>/properties/read
{
"properties": ["getAll"]
}
```

## Basic MQTT communication
To send MQTT commands, use the following topics:

### READ:
```
iot/gDa3tb/<deviceId>/properties/read
```
response:
```
/gDa3tb/<deviceId>/properties/read/reply
```

### WRITE:
```
iot/gDa3tb/<deviceId>/properties/write
```
response:
```
/gDa3tb/<deviceId>/properties/write/reply
```

### Updates on change
Automatic updates will come over a different topics:
```
/gDa3tb/<deviceId>/properties/report
```

To update all properties, publish the following message:
```
iot/gDa3tb/<deviceId>/properties/read
{
"properties": ["getAll"]
}
```



### Reconnecting HYPER2000 to the cloud
Yoy can reconnect to Zendure's cloud again. This might be necessary to get firmware updates. The process is similar to the disconnect steps:

```
$ export WIFI_PWD="your_wifi_password"
$ export SF_DEVICE_ID="your_sf_deviceid"
$ export SF_PRODUCT_ID="73bkTV"
$ python3 solarflow-bt-manager.py -c -w <WiFi SSID>
```

# List of available MQTT entities
| Attribute           | Writable | Description                       |
|---------------------|----------|-----------------------------------|
| OldMode             | Yes/No   | Legacy mode?                      |
| acMode              | Yes      | AC mode (1=Input, 2=Output)       |
| ambientLightColor   | Yes/No   | Ambient light color? (d:65280)    |
| ambientLightMode    | Yes/No   | Ambient light mode?               |
| ambientLightNess    | Yes/No   | Ambient light brightness? (d:20)  |
| ambientSwitch       | Yes/No   | Ambient light switch?             |
| autoHeat            | Yes/No   | Automatic heating enabled?        |
| autoModel           | Yes/No   | Automatic model selection?        |
| batVolt             | No       | Battery voltage?                  |
| blueOta             | Yes/No   | Over the air?                     |
| buzzerSwitch        | Yes/No   | Buzzer switch?                    |
| chargingMode        | Yes/No   | Charging mode?                    |
| chargingTime        | No       | Charging time                     |
| chargingType        | Yes/No   | Charging type?                     |
| circuitCheckMode    | Yes/No   | Circuit check mode?                |
| clusterSw           | Yes/No   | Cluster switch?                   |
| ctOff               | Yes/No   | CT Mode off?                      |
| electricLevel       | No       | Battery level in % (0-100)        |
| energyPower         | No       | Energy power?                     |
| getAll              | Yes      | Get all properties                |
| gridInputPower      | No       | Input power from grid in W        |
| gridInputPowerCycle | Yes/No   | Grid input power cycle?           |
| gridOffMode         | Yes/No   | Grid-off mode?                    |
| gridReverse         | Yes      | Grid reverse mode (0=Auto, 1=On, 2=Off) |
| gridStandard        | Yes/No   | Grid standard?                     |
| heatState           | Yes/No   | Current heating state?            |
| hubState            | No       | Hub state?                        |
| hyperTmp            | No       | Device temperature (t - 2731) / 10|
| inputLimit          | Yes      | Input power limit from the grid   |
| inputMode           | Yes/No   | Input Mode?                       |
| invOutputPower      | Yes      | Inverter output power?            |
| inverseMaxPower     | Yes      | Maximum inverter power (0-1200)   |
| lampSwitch          | Yes      | Lamp switch (0=Off, 1=On)         |
| localState          | No       | Local state?                      |
| lowTemperature      | Yes/No   | Low temperature (0/1)             |
| masterSoftVersion   | No       | Master software version           |
| masterSwitch        | Yes/No   | Master switch (0=Off, 1=On)       |
| masterhaerVersion   | No       | Master hardware version           |
| minSoc              | Yes      | Minimum state of charge (%)       |
| outputHomePower     | No       | Output power to home in W         |
| outputHomePowerCycle| No       | Output home power cycle?          |
| outputLimit         | Yes      | Output power limit to the grid    |
| outputPackPower     | No       | Battery power in in W             |
| outputPackPowerCycle| Yes/No   | Battery output power cycle?       |
| packInputPower      | No       | Battery power out in W            |
| packInputPowerCycle | Yes/No   | Batter input power cycle?         |
| packNum             | No       | Number of battery packs (0-4)     |
| packState           | No       | Battery pack state (0=Standby, 1=Input, 2=Output) |
| pass                | No       | Bypass mode (0=Auto, 1=On, 2=Off) |
| phaseCheck          | Yes/No   | Phase check?                      |
| phaseSwitch         | Yes/No   | Phase switch?                     |
| plugState           | Yes/No   | Plug connection state?            |
| pvBrand             | Yes/No   | PV brand/model?                   |
| remainInputTime     | No       | Remaining current charging time   |
| remainOutTime       | No       | Remaining current discharing time |
| reverseState        | No       | Reverse state, bypass to grid allow (0=Yes, 1=No) |
| socSet              | Yes/No   | Set Maximum SOC (0-1000=100%)     |
| socStatus           | No       | State of charge status?           |
| solarInputPower     | No       | Solar input power in W            |
| solarPower1         | No       | Solar power channel 1 in W        |
| solarPower1Cycle    | No       | Solar power 1 cycle?              |
| solarPower2         | No       | Solar power channel 2 in W        |
| solarPower2Cycle    | No       | Solar power 2 cycle?              |
| strength            | No       | Wifi Signal strength  (0-3)       |
| voltWakeup          | Yes/No   | Voltage threshold for wakeup?     |
| wifiState           | No       | WiFi connection state (0=Disconnected, 1=Connected) |

> **Note:**  
> The "Writable" column indicates if the attribute can be set via MQTT. Please refer to the device documentation or test with caution, as not all attributes may be writable.
