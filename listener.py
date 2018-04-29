import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
from time import gmtime, strftime

import gammu.smsd
smsd = gammu.smsd.SMSD('/etc/gammu-smsdrc')

def cleanAndExit():
	print "Cleaning..."
	GPIO.cleanup()
	print "Bye!"
	sys.exit()

hx = HX711(5, 6)
hx2 = HX711(13, 26)
hx3 = HX711(23, 24)

hx.set_reading_format("LSB", "MSB")
hx2.set_reading_format("LSB", "MSB")
hx3.set_reading_format("LSB", "MSB")

hx.set_reference_unit(21)
hx2.set_reference_unit(21)
hx3.set_reference_unit(21)

hx.reset()
hx.tare()
hx2.reset()
hx2.tare()
hx3.reset()
hx3.tare()
status = 0

while True:
    try:
		val1 = hx1.get_weight(5)
		val2 = hx2.get_weight(5)
		val3 = hx3.get_weight(5)
		messages = "Panel1: " + val1 + ", Panel2: " + val2 + ", Panel3: " + val3
		
		hours = strftime("%H", gmtime())
		minutes = strftime("%M", gmtime())
		times = ((int(hours) + int(8)) * int(60)) + int(minutes)
		print times

		if int(times)%5 == 0 :
			if(status == 0):
				message = { 'Text': messages , 'SMSC' : {'Location' : 1}, 'Number' : '09283164164' }
				smsd.InjectSMS([message])
				print ("Panel1: %s , Panel2: %s , Panel3: %s ," %(val1,val2,val3))				
				print "Message Sent"
				status = 1
		else:	
				status = 0

		hx.power_down()
		hx.power_up()
		hx2.power_down()
		hx2.power_up()
		hx3.power_down()
		hx3.power_up()
		time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
cleanAndExit()