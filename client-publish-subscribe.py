#! c:\python34\python.exe
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
# slight mods to Steve's code to include AWS IOT security and
# a wait for ack after the subscribe
"""
Simple publish and sbscribe. See the callback script for code to get the message from the
on_message callback into the main script. Notice I use a wildcard to subscribe so I receive message
sent on multiple topics
"""
# broker="test.mosquitto.org"
# broker="192.168.1.41"
#broker="localhost"
import paho.mqtt.client as mqtt  #import the client1
import time, sys
import ssl
awshost = "a2r1ri0ddc3zuq-ats.iot.us-east-1.amazonaws.com"
awsport = 8883
suback = False
clientId = "myThingName"
thingName = "myThingName"
caPath = r"C:\Users\felix\OneDrive\Desktop\AWS_Certs\aws-iot\rasppi\AmazonRootCA1.pem"
certPath = r"C:\Users\felix\OneDrive\Desktop\AWS_Certs\aws-iot\rasppi\RaspPi.cert.pem"
keyPath = r"C:\Users\felix\OneDrive\Desktop\AWS_Certs\aws-iot\rasppi\RaspPi.private.key"

def on_subscribe(client, userdata, mid, granted_qos): 
       global suback
       suback = True

def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))

def on_message(client,userdata,msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message received",m_decode)

client = mqtt.Client("python1")#create new instance
client.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_subscribe = on_subscribe
#client.on_log=on_log
client.on_message=on_message
print("Connecting to broker ",awshost)

client.connect(awshost, awsport, keepalive=60)      #connect to broker
client.loop_start()  #Start loop
client.subscribe("house/#")
sleep_count = 0
while not suback:
        time.sleep(.25)
        if sleep_count >40: #give up
                print("Subscribe failure quitting")
                client.loop_stop()
                sys.exit()
        sleep_count += 1

# time.sleep(2)

client.publish("house/sensor1","my first message")
time.sleep(3)
client.publish("house/sensors/s1","my second message")
time.sleep(4)
client.loop_stop()    #Stop loop 
client.disconnect() # disconnect



