import sys
import numpy as np
import pandas as pd
import scipy.signal as signal

v = sys.version_info[0]
if v == 2 :
	import Tkinter
	import tkMessageBox
	import tkFileDialog
elif v == 3 :
	import tkinter as Tkinter
	from tkinter import messagebox as tkMessageBox
	from tkinter import filedialog as tkFileDialog
else :
	exit("*This script only supports Python2.x or 3.x.\nSorry, we can not support your Python.")

FS = 10000			# PSDの周波数上限

if __name__ == "__main__" :
	### GUI用のおまじない
	root = Tkinter.Tk()
	root.option_add('*font', ('FixedSys', 14))
	fTyp=[('csvファイル','*.csv')]
	iDir='.'


	### ファイル選択
	lb=Tkinter.Label(root, text="Chose answer-file",width=20)
	lb.pack()

	filename = tkFileDialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
	if filename == "" :
		exit("*You did not chose your csv files")
	else :
		print("*A file you selected: %s" %filename)


	### ファイル読み込み
	df = pd.read_csv(filename, index_col=0)		# headerあり，indexあり
	data = df.values

	### PSD計算
	if data.shape[0] < 256 :
		segment = cnt
	else :
		segment = 256

	f, pxx = signal.welch(data, fs=FS*2, nperseg=segment)
	
	import matplotlib.pyplot as plt
	plt.subplot(211)						# 測定したセンサ値（もしくは生成した乱数）をグラフ化
	x = [i+1 for i in range(data.shape[0])]
	plt.plot(x, data)

	plt.xlim(-10, np.amax(x)*1.05)
	plt.ylim(np.amin(data)*0.95, np.amax(data)*1.05)

	plt.ylabel("Sensor-value")
	plt.title("Sensor-values")

	plt.subplot(212)						# 計算したPSDをグラフ化

	plt.plot(f, pxx, color="r")
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
