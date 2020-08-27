#===================================================================
# Function to measure temperature of a single HP temperature sensor.
#===================================================================

import smbus, subprocess
import time
import numpy as np

class TEMP:
	def __init__(self):
		#self.ADD=[0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x4c]
		self.ADD=[0x40,0x42,0x43,0x44,0x45,0x47,0x48]

		l=[0x02,0x42,0x06,0xA0]
		self.bus=smbus.SMBus(1)
	
		i=0
		while i in range(0,7):
			self.bus.write_i2c_block_data(self.ADD[i],0x40,[l[0]])
			self.bus.write_i2c_block_data(self.ADD[i],0x44,[l[1]])
			self.bus.write_i2c_block_data(self.ADD[i],0x48,[l[2]])
			self.bus.write_i2c_block_data(self.ADD[i],0x4C,[l[3]])
			i+=1

	def getTemp(self,sensor):
		r = [31.3231717,2.20213448,1.66482204e-3,-3.98620116e-6,4.74888650e-9,
			7.27263261e-12,-2.80325700e-14,3.11300149e-17,-1.22123964e-20] 
		polyR = np.polynomial.Chebyshev(r)

		rdata=0x10
		start=0x08
		LSB = 2.3e-7 #1bit = 2.3e-7volts (not 2.441e-7? I don't think it matters for dT)
		IDAC = .001  # 1000 micro amp excitation current
		resistance = {0:1,1:1,2:100.447,3:100.490,4:100.353,5:100.355,6:100.497}

		self.bus.write_byte(self.ADD[sensor],start)
		time.sleep(0.1)
		Data=self.bus.read_i2c_block_data(self.ADD[sensor],rdata)

		dec10s=Data[0]<<16
		dec11s=Data[1]<<8
		code=dec10s|dec11s|Data[2]

		Vin = LSB*code/2
		R = Vin/IDAC
		R = R*109.28/resistance[sensor] #conversion at ~23.8C

		output = polyR(R)-273.15
		return output

