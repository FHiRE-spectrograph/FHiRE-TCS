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
		C0=-245.19
		C1=5.5293
		C2=-0.066046
		C3=4.0422e-3
		C4=-2.0697e-6
		C5=-0.025422
		C6=1.6883e-3
		C7=-1.3601e-6

		rdata=0x10
		start=0x08
		LSB = 2.3e-7
		IDAC = .001  # 1000 micro amp excitation current

		#Raw=[]
		self.bus.write_byte(self.ADD[sensor],start)
		time.sleep(0.1)
		Data=self.bus.read_i2c_block_data(self.ADD[sensor],rdata)

		dec10s=Data[0]<<16
		dec11s=Data[1]<<8
		code=dec10s|dec11s|Data[2]

		Vin = LSB*code
		R = (Vin/IDAC)/2

		output=C0+(R*(C1+R*(C2+R*(C3+C4*R))))/(1+R*(C5+R*(C6+C7*R)))
		return output

#temp = TEMP()
#print temp.getTemp(0)

