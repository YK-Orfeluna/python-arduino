# -*- coding: utf-8 -*

import time
import numpy as np
import serial, pyfirmata

HIGH = 1
LOW = 0

D1 = np.arange(0, 181)
D2 = np.arange(180, -1, -1)

def delay(ms) :
	time.sleep(ms / 1000.0)

class Arduino :
	def __init__(self, port) :
		self.board = pyfirmata.Arduino(port)		# Arduinoと接続

		it = pyfirmata.util.Iterator(self.board)	# analogRead()の準備
		it.start()

		print("*Connected Arduino to %s" %port)

	def servo_attach(self, pin, angle=90) :
		self.board.digital[pin].mode = pyfirmata.SERVO
		self.board.digital[pin].write(angle)

		print("*Connected %s pin to servo motor" %pin)

	def servo_read(self, pin, output=int) :
		value = self.board.digital[pin].read()
		if output == int :
			value = int(round(value, 0))
		return value

	def servo_write(self, pin, angle, limit=[0, 180], ms=30) :
		now_angle = self.servo_read(pin)
		angle_f = 0

		if limit[0] <= angle <= limit[1] and angle != now_angle:
			print("*Rotated servo from %s to %s in %s pin" %(now_angle, angle, pin))

			if type(angle) == float :
				angle_f = angle
				angle = int(round(angle, 0))

			if angle > now_angle :
				d_list = D1[now_angle : angle+1]
			else :
				d_list = D2[180-now_angle : 180-degrees+1]

			for i in d_list :
				self.board.digital[pin].write(i)
				delay(ms)

			if angle_f != 0 :
				self.board.digital[pin].write(angle_f)

		elif angle < limit[0] or limit[1] < angle :
			print("*Worning!!: angle is out of limits")
	
	def analogRead(self, pin) :
		value = self.board.get_pin('a:%s:i' %pin)
		value = int(round((value * 1023), 0))		# board.get_pin()は0~1のfloat値なので，1023倍のint値で出力
		return value

	def digitalWrite(self, pin, value) :
		if value == "HIGH" or HIGH :
			self.board.digital[pin].write[HIGH]
		elif value =="LOW" or LOW :
			self.board.digital[pin].write[LOW]
		else :
			print("*value is missing: 'HIGH', 1, 'LOW', 0")

	def digitalRead(self, pin) :
		value = self.board.digital[pin].read()
		return value

	def finish(self) :
		self.board.exit()













