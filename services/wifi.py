import network
import uasyncio


class ConnectionStatus:
    NOT_CONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


async def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    connected = False
    while not connected:
        nets = sta_if.scan()
        for net in nets:
            net_ssid = net[0].decode()
            if net_ssid == ssid:
                print(f'Network found! Connecting to {ssid}...')
                sta_if.connect(net_ssid, password)
                while not sta_if.isconnected():
                    await uasyncio.sleep_ms(500)
                print('WLAN connection succeeded!')
                connected = True
                break
        await uasyncio.sleep_ms(500)

    return sta_if
