from machine import Pin
import uasyncio
import urequests

from env.env import Environment
from services.wifi import *

led = Pin("LED", Pin.OUT)


async def main():
    connection_status = ConnectionStatus.NOT_CONNECTED

    async def monitor_connection_status(station):
        nonlocal connection_status
        while True:
            if station.isconnected():
                connection_status = ConnectionStatus.CONNECTED
            else:
                connection_status = ConnectionStatus.NOT_CONNECTED
            await uasyncio.sleep_ms(500)

    async def setup_wifi():
        try:
            nonlocal connection_status
            connection_status = ConnectionStatus.CONNECTING
            print(f"Searching for {Environment.SSID}...")
            station = await connect_wifi(Environment.SSID, Environment.SSID_PASSWORD)
            intra_ipaddress, _, _, _ = station.ifconfig()
            uasyncio.create_task(monitor_connection_status(station))
            response = urequests.get("https://icanhazip.com/").text()
            print("----\nIP Info:\n----")
            print(f"Internal IP Address: {intra_ipaddress}")
            print(f"External IP Address: {response}")
        except Exception as e:
            print(e)

    async def display_connection_status():
        while True:
            if connection_status == ConnectionStatus.CONNECTED:
                led.value(1)
            elif connection_status == ConnectionStatus.CONNECTING:
                led.value(1)
                await uasyncio.sleep_ms(500)
                led.value(0)
            else:
                led.value(0)
            await uasyncio.sleep_ms(500)

    uasyncio.create_task(display_connection_status())
    uasyncio.create_task(setup_wifi())
    print("Welcome!")

    while True:
        # Loop forever, just letting other processes run
        # This allows us to group our code above and keep it organized
        await uasyncio.sleep_ms(1000)


uasyncio.run(main())
