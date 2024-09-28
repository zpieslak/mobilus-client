## Mobilus Cosmo GTW Client

![test workflow](https://github.com/zpieslak/mobilus-client/actions/workflows/test.yml/badge.svg)

This code provides a native Python client for the Mobilus Cosmo GTW. It connects directly to the gateway's MQTT broker and sends message commands to control the associated devices. The connection is established locally, so the client must be run on the same network as the gateway. Currently, the only tested and supported devices are radio shutters (Mobilus COSMO 2WAY).

In order to use the client, configuration and setup need to be done on the Mobilus Cosmo GTW side. This includes creating a user and pairing the devices with the gateway.

More information can be found on [blog post](https://codegyver.com/2024/09/22/mobilus-cosmo-gtw-reverse-engineering-a-radio-shutter-device/).

## Installation

Install the module with pip:

    pip install mobilus-client

## Usage

For convenience, the client can be run as a module:

    python -m mobilus_client --host=GATEWAY_HOST --login=USER_LOGIN --password=USER_PASSWORD COMMANDS

Where:

* `GATEWAY_HOST` is the IP address of the gateway.
* `USER_LOGIN` and `USER_PASSWORD` are the user credentials to access the gateway.
* `COMMANDS` is a list of commands to be sent to the gateway.

Currently, the following commands are supported:

* `current_state` - Get the current state of the devices. Please note that in the case of shutters, this doesn't return any meaningful data.

* `devices_list` - List all devices that are paired with the gateway.

* `call_events:device_id=DEVICE_ID,value=VALUE` - Send a command to the device. This can be used for actual control of the device (shutter).

    * `DEVICE_ID` - The ID of the device as returned from devices_list.
    * `VALUE` - The value to be sent to the device, currently one of "UP", "DOWN", "STOP", or a percentage value like "85%".

Multiple commands can be sent at once, separated by spaces:

    python -m mobilus_client --host=192.168.2.1 --login=admin --password=my_password devices_list call_events:device_id=0,value=100% call_events:device_id=1,value=80%

Output is printed to the console in JSON format, and therefore the client command can be easily chained with `jq` for prettier output. For example:

    python -m mobilus_client --host=192.168.2.1 --login=admin --password=my_password current_state | jq

Verbose mode can be enabled with the `--verbose` flag:

    python -m mobilus_client --host=192.168.2.1 --login=admin --password=my_password --verbose current_state

## Caveats

The client is tested with Mobilus Cosmo GTW with shutter devices only (COSMO 2WAY). It is possible that it will work with other devices, but it is not guaranteed. The purpose of the client is to provide a simple way to control the devices without the need to use the official Mobilus Cosmo GTW web interface or app, and to integrate it with open-source systems like Home Assistant. I am not affiliated with Mobilus, and the client is provided as is.

## Development

Clone the repository and navigate to the project directory.
Install the package in editable mode with the following command:

    pip install -e .[test]

Check mypy and flake8 with the following commands:

    mypy .
    flake8 .

The tests can be run with the following command:

    python -m unittest -v

To generate a coverage report:

    coverage run -m unittest discover
    coverage report
