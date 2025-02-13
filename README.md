# HYPER2000 Cloud unchained
This little tool is able to disconnect / connect your HYPER2000 from ZENDURE cloud. All states and the full controll will be available through a local MQTT-broker.



> [!NOTE]
>
> Please note that this is work in progress. Completely use at you own risk.

1. [Features](#features)
1. [Why disconnect your Solarflow Hub](#why)
1. [How to use](#howto)
1. [Use Cases](#usecase)

## Supported Devices <a name="what"></a>
- Hyper2000 (SF_PRODUCT_ID=ja72U0ha _default_)

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

As all ZENDURE device, it will connect using a auto generated user_name and password. Thanksfully it was not that hard to get the used user_name and password.

I'm currently using the latest mosquitto docker image:
```
mosquitto version 2.0.20 starting
```
mosquitto has support for anonymous logins, but not any user_name and password. If the client is sending a user_name and password, it must be part of the password file. You can't ignore it.

#### Get HYPER2000 user_name and password

One way to get the necessary credentials is tcpdump:

```
sudo tcpdump -i eth0 src host <IP_ADDRESS_HYPER2K> -w capture.pcap
```

Maybe the easiest way is to generate the used password out of your DEVICE_ID, the password is a part of the md5-hash only with upper letters:

```
echo -n <SF_DEVICE_ID> | md5sum | awk '{print toupper($1)}' | cut -c9-24
```
#### Add user to mosquitto

```
sudo mosquitto_passwd <path_to_password_file> <SF_DEVICE_ID>
```

### Reconnecting HYPER2000 to the cloud
Yoy can reconnect to Zendure's cloud again. This might be necessary to get firmware updates. The process is similar to the disconnect steps:

```
$ export WIFI_PWD="your_wifi_password"
$ export SF_DEVICE_ID="your_sf_deviceid"
$ export SF_PRODUCT_ID="73bkTV"
$ python3 solarflow-bt-manager.py -c -w <WiFi SSID>
```

