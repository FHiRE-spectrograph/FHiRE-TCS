import low_p_temp_boards as lowp
from time import sleep
import numpy as np

class LN2_Temp:
	
	def __init__(self):
		self.lp = lowp.LP()
		
	def Run(self):
		temp = self.lp.getTemp(27)
		temp = float(temp)
		self.save_dat(temp)
	
	def save_dat(self,temp):
		temp = np.array(temp).reshape(1, )
		header = "Temperature at LN2 Feedthrough"
		np.savetxt('LN2Temp.dat',temp,header=header)
			
if __name__ == '__main__':
	ln2t = LN2_Temp()
	
	try:
		while True:
			ln2t.Run()
			sleep(10)
	except KeyboardInterrupt:
		pass
