from machine import Pin
import ubluetooth
import time


from machine import Pin, Timer
from time import sleep_ms
import ubluetooth
from esp32 import raw_temperature

class BLE():


		def __init__(self, name):

				self.name = name
				self.ble = ubluetooth.BLE()
				self.ble.active(True)

				self.led = Pin(2, Pin.OUT)
				self.timer1 = Timer(0)
				self.timer2 = Timer(1)

				self.disconnected()
				self.ble.irq(self.ble_irq)
				self.register()
				self.advertiser()


		def connected(self):

				self.timer1.deinit()
				self.timer2.deinit()


		def disconnected(self):

				self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
				sleep_ms(200)
				self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))


		def ble_irq(self, event, data):

				if event == 1:
						'''Central disconnected'''
						self.connected()
						self.led(1)

				elif event == 2:
						'''Central disconnected'''
						self.advertiser()
						self.disconnected()

				elif event == 4:
						'''New message received'''

						buffer = self.ble.gatts_read(self.rx)
						message = buffer.decode('UTF-8')[:-1]
						print(message)

						if received == 'blue_led':
								blue_led.value(not blue_led.value())


		def register(self):

				# Nordic UART Service (NUS)
				BLE_NUS = ubluetooth.UUID(0x1812)
				BLE_RX = (ubluetooth.UUID(0x2A37), ubluetooth.FLAG_WRITE)
				BLE_TX = (ubluetooth.UUID(0x2A38), ubluetooth.FLAG_NOTIFY)

				BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
				SERVICES = (BLE_UART, )
				((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)


		def send(self, data):
				self.ble.gatts_notify(0, self.tx, data + '\n')


		def advertiser(self):
				name = bytes(self.name, 'UTF-8')
				self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)



if __name__ == '__main__':
	ALERT = Pin(2, Pin.OUT)
	button = pin(25, Pin.IN, Pin.PULL_DOWN)
	ble = BLE("P.E.A 500A")
	while True:
		if button.value == 1:
			time.sleep(2)
			if button.value == 1:
				while True:
					ble.send('ALERT:500A:TRIGGER:USER')
					ALERT(1)
					time.sleep(1)
					ALERT(0)
					time.sleep(2)
					ble.send('ALERT:500A:UPTIME:DEVICE')
					time.sleep(0.1)
					if button.value == 1:
						time.sleep(3)
						if button.value == 1:
							ble.send('ALER:500A:CANCEL:USER')
							break
