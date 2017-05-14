import sys
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

TEST = True			# TESTがTrueだと，乱数生成によるコードの動作確認を行う
#TEST = False		# Falseだと，Arduinoからセンサ値を取得して，センサ値のノイズを測定する

CNT = 1000			# データ数
if CNT <= 256 :
	segment = CNT
else :
	segment = 256


FS = 10000			# PSDの周波数上限

if __name__ == "__main__" :
	if TEST == False:
		from arduino import*

		port = "/dev/cu.usbmodem1421"
		pin = 0
		STR_LI = ["*Collecting sensor-values.    ", "*Collecting sensor-values. .  ", "*Collecting sensor-values. . ."]

		app = Arduino(port)
	
		arr = []
		for i in range(CNT) :
			arr.append(app.analogRead(pin))
			sys.stdout.write("\r%d" % STR_LI[i%len(STR_LI)])
			sys.stdout.flush()
			delay(10)

		arr = np.array(arr, dtype=np.int64)

	else :
		arr = np.random.rand(CNT)

	f, pxx = signal.welch(arr, fs=FS*2, nperseg=segment)
	
	plt.subplot(211)						# 測定したセンサ値（もしくは生成した乱数）をグラフ化
	x = [i*10 for i in range(CNT)]
	plt.plot(x, arr)

	plt.xlim(-10, np.amax(x)*1.05)
	plt.ylim(np.amin(arr)*0.95, np.amax(arr)*1.05)

	plt.xlabel("Time(mill sec.)")
	plt.ylabel("Sensor-value")
	plt.title("Sensor-values")

	plt.subplot(212)						# 計算したPSDをグラフ化

	plt.plot(f, pxx)
	plt.xlim(-100, FS*1.05)

	if np.amin(pxx) < 0 :
		ymin = np.amin(pxx) * 0.95
	else :
		ymin = 0

	plt.ylim(ymin, np.amax(pxx)*1.05)

	plt.xlabel("Frequency (Hz)")
	plt.ylabel("PSD")
	plt.title("PSD of Sensor-values")

	plt.show()

	exit()