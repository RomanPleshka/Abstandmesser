# Stellt die Verbindung zum WLAN her
import network, utime
def wifiConnect(ssid, password):
   
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Wait for connection')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print(".", end="")
            utime.sleep_ms(500)
            
    print()
    print("Connected to", ssid)
    print('IP address:', sta_if.ifconfig()[0])
