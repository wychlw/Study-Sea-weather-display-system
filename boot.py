# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import network
import os
import time
webrepl.start()
gc.collect()

machine.freq(160000000)
print("boot from memory...")

SSID=[put your own wifi ssid here]
PASSWD=[put maches passwd here]

wlan=network.WLAN(network.STA_IF)
wlan.active(True)
print(wlan.scan())
which=0
while not wlan.isconnected():
    if which>=len(SSID):
        which=0
    t=0
    while t<5 and not wlan.isconnected():
        print("connecting",SSID[which])
        wlan.connect(SSID[which],PASSWD[which])
        if wlan.isconnected():
            break
        t=t+1
        time.sleep(5)
        if not wlan.isconnected():
            print("conn fail,SSID:",SSID[which],wlan.isconnected())
        else:
            break
        time.sleep(5)
    which=which+1

print("network config:\n",wlan.ifconfig())

from main import main

main(wlan,SSID,PASSWD)