from math import pi

p = 1e-12
u = 1e-6

capacitor = {
				100:10*p, 
				101:100*p, 
				102:0.001*u, 
				103:0.01*u, 
				104:0.1*u, 
				105:u, 
				106:10*u, 
				223:0.022*u, 
				333:0.033*u, 
				473:0.047*u, 
				474:0.47*u
			}

def filter(fc) :

	global capacitor

	t = 1.0 / (fc * 2*pi)

	for i in capacitor :
		r = str(round((t / capacitor[i]), 2))
		print("%s %s and %s" %(r, "\u03a9", i))
	

def freq(r, c) :
	global capacitor

	c = capacitor[c]

	fc = 1.0 / (2 * pi * r * c)
	return fc

if __name__ == "__main__" :
	print("A frequency which you want to cut using HPF or LPF")
	fc = int(input("Hz >>>"))

	filter(fc)

	print("Which resister do you use?")
	r = float(input("\u03a9 >>>"))

	print("Which capacitor do you use?")
	c = int(input("No. >>>"))

	print("\n%.3f Hz" %freq(r, c))

	exit()