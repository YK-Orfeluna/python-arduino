import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt



TEST = True
TEST = False

CNT = 1000

if __name__ == "__main__" :
	if TEST :
		from arduino import*

		port = "/dev/cu.usbmodem1421"
		pin = 0

		app = Arduino(port)
	
		arr = []
		for i in range(CNT) :
			arr.append(app.analogRead(pin))
			delay(50)

		arr = np.array(arr, dtype=np.int64)

	else :
		arr = np.random.rand(CNT)

	f, pxx = signal.welch(arr, fs=20000, nperseg=CNT)
	print(f, pxx)

	plt.semilogy(f, pxx)
	plt.show()

	exit()