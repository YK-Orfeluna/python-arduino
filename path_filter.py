from math import pi

capacitor = [100, 101, 102, 103, 104, 105, 106, 223, 333, 473, 474]
p = 1e-12
u = 1e-6
farad = [10*p, 100*p, 0.001*u, 0.01*u, 0.1*u, 1*u, 10*u, 0.022*u, 0.033*u, 0.047*u, 0.47*u]

def filter(fc) :
	global capacitor, farad

	t = 1.0 / (fc * 2*pi)

	r = []
	for i in farad :
		r.append(str(round(t/i, 3))+"\u03a9")

	for x, i in enumerate(r) :
		print("%s and %s" %(i, capacitor[x]))

def freq(r, c) :
	global capacitor, farad

	index = capacitor.index(c)
	c = farad[index]

	fc = 1.0 / (2 * pi * r * c)
	return fc

if __name__ == "__main__" :
	print("A frequency(Hz) which you want to cut using HPF or LPF")
	fc = int(input(">>>"))

	filter(fc)

	print("Which resister(\u03a9) do you use?")
	r = float(input(">>>"))

	print("Which capacitor do you use?")
	c = int(input(">>>"))

	print("\n%.3f Hz" %freq(r, c))