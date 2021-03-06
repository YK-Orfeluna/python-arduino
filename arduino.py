# -*- coding: utf-8 -*

import time
import numpy as np
import pyfirmata

HIGH = 1
LOW = 0

INPUT = "INPUT"
OUTPUT = "OUTPUT"
ANALOG = "ANALOG"
PWM = "PWM"
SERVO = "SERVO"

D1 = np.arange(0, 181)
D2 = np.arange(180, -1, -1)

UNO = "UNO"
MEGA = "MEGA"
SAINSMART = "SAINSMART"

"""
SAINSMART = {
	'digital': tuple(x for x in range(14)),
	'analog': tuple(x for x in range(8)),
	'pwm': (3, 5, 6, 9, 10, 11),
	'use_ports': True,
	'disabled': (0, 1)  # Rx, Tx, Crystal
}
"""

def delay(ms) :
	time.sleep(ms / 1000.0)

def exchangeV(value, V=5.0) :
	x = 1023 / V
	out = value / x
	return out

class Arduino :
	def __init__(self, port, board=UNO) :
		if board == UNO:
			self.board = pyfirmata.Arduino(port)		# Arduinoと接続
		elif board == MEGA :
			self.board = pyfirmata.ArduinoMega(port)
		"""
		elif board == SAINSMART :
			self.board = pyfirmata.Board(port, layout=SAINSMART)
		"""

		it = pyfirmata.util.Iterator(self.board)	# analogRead()の準備
		it.start()

		A0 = self.board.get_pin('a:0:i')
		A1 = self.board.get_pin('a:1:i')
		A2 = self.board.get_pin('a:2:i')
		A3 = self.board.get_pin('a:3:i')
		A4 = self.board.get_pin('a:4:i')
		A5 = self.board.get_pin('a:5:i')
		self.ANALOG = [A0, A1, A2, A3, A4, A5]

		if board == MEGA :
			A6 = self.board.get_pin('a:6:i')
			A7 = self.board.get_pin('a:7:i')
			A8 = self.board.get_pin('a:8:i')
			A9 = self.board.get_pin('a:9:i')
			A10 = self.board.get_pin('a:10:i')
			A11 = self.board.get_pin('a:11:i')
			A12 = self.board.get_pin('a:12:i')
			A13 = self.board.get_pin('a:13:i')
			A14 = self.board.get_pin('a:14:i')
			A15 = self.board.get_pin('a:15:i')
			A16 = self.board.get_pin('a:16:i')
			self.ANALOG = [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16]
		"""
		elif board == "SAINSMART" :
			A6 = self.board.get_pin('a:6:i')
			A7 = self.board.get_pin('a:7:i')
			self.ANALOG = [A0, A1, A2, A3, A4, A5, A6, A7]
		"""

		time.sleep(3)

		print("*Connected Arduino %s to %s" %(board, port))

	def pinMode(self, pin, mode) :
		if mode == INPUT :
			self.board.digital[pin].mode = pyfirmata.INPUT			# as defined in wiring.h
		elif mode == OUTPUT :
			self.board.digital[pin].mode = pyfirmata.OUTPUT			# as defined in wiring.h
		elif mode == ANALOG :
			self.board.analog[pin].mode = pyfirmata.ANALOG			# analog pin in analogInput mode
		elif mode == PWM :
			self.board.digital[pin].mode = pyfirmata.PWM			# digital pin in PWM output mode
		elif mode == SERVO :
			self.board.digital[pin].mode = pyfirmata.SERVO			# digital pin in SERVO mode
		else :
			print("*mode is missing: %s, %s, %s, %s or %s" %(INPUT, OUTPUT, ANALOG, PWM, SERVO))

		time.sleep(1)

	def digitalRead(self, pin) :
		value = self.board.digital[pin].read()
		return value

	def digitalWrite(self, pin, value, ccc=False) :
		if ccc :
			self.board.digital[pin].write[value]
		elif value == "HIGH" or value == HIGH :
			self.board.digital[pin].write(HIGH)
		elif value == "LOW" or value == LOW :
			self.board.digital[pin].write(LOW)
		else :
			print("*value is missing: 'HIGH', 1, 'LOW', 0")

	def analogRead(self, pin) :
		value = self.ANALOG[pin].read()
		value = int(round((value * 1023), 0))		# board.get_pin()は0~1のfloat値なので，1023倍のint値で出力
		return value

	def analogWrite(self, pin, pwm) :
		if pwm != 0 :
			pwm /= 255.0
		self.digitalWrite(pin, pwm, ccc=True)

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
				self.digitalWrite(pin, i, ccc=True)
				delay(ms)

			if angle_f != 0 :
				self.digitalWrite(pin, angle_f, ccc=True)

		elif angle < limit[0] or limit[1] < angle :
			print("*Worning!!: angle is out of limits")

	def servo_attach(self, pin, angle=90) :
		self.pinMode(pin, SERVO)
		time.sleep(1)
		self.servo_write(pin, angle)

		print("*Connected %s pin to servo motor" %pin)

	def servo_read(self, pin, output=int) :
		value = self.digitalRead(pin)
		if output == int :
			value = int(round(value, 0))
		return value

	def disconnection(self) :
		self.board.exit()
		print("*disconnected to Arduino")

if __name__ == "__main__" :
	port = "/dev/cu.usbmodem1421"
	a = Arduino(port)

	for i in range(6) :
		print("A%s = %s" %(i, a.analogRead(i)))
		delay(100)

	a.pinMode(2, "INPUT")
	print(a.digitalRead(2))

	a.pinMode(9, "OUTPUT")
	a.digitalWrite(9, "HIGH")
	delay(100)
	a.digitalWrite(9, "LOW")
	a.digitalWrite(13, "LOW")

	a.disconnection()

	exit()
