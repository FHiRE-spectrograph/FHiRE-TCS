#===================================================================
# Function to measure temperature of a single HP temperature sensor.
#===================================================================

import smbus, subprocess
import time
import numpy as np

class TEMP:
	def __init__(self):
		#
		# Addresses of HP boards. Check which boards are
		# connected using $i2cdetect -y 1
		# Boards 2,7 and 10 haven't worked. Board 4 (0x43) suddenly
		# won't work now though. :(
		#
		#self.ADD = [0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x4c]
		self.ADD = [0x40, 0x42, 0x43, 0x44, 0x45, 0x47, 0x48]

		l = [0x02, 0x42, 0x06, 0xA0]
		self.bus = smbus.SMBus(1)

		for i in range(0,7):
			# Skip connecting to board 4.
			if i == 2:
				continue

			#
			# I2C communications are nested in these try loops as
			# a quick fix to IOErrors with I2C on the Pi. It's an
			# issue with clock stretching and could also be fixed
			# by slowing the I2C clock rate down. 
			#
			x = True
			attempt = 0
			while x == True:
				try:
					self.bus.write_i2c_block_data(
						self.ADD[i], 0x40, [l[0]])
					self.bus.write_i2c_block_data(
						self.ADD[i], 0x44, [l[1]])
					self.bus.write_i2c_block_data(
						self.ADD[i], 0x48, [l[2]])
					self.bus.write_i2c_block_data(
						self.ADD[i], 0x4C, [l[3]])
					x = False
				# Handle missed communications
				except:
					attempt += 1
					if attempt < 20:
						print("Timeout error: HP board "
						      "%s initialization" 
						      %hex(self.ADD[i]))
						x = False
					pass


	def getTemp(self,sensor):
		# Chebyshev coefficients for relating resistance to temperature.
		r = [31.3231717, 2.20213448, 1.66482204e-3, -3.98620116e-6,
		     4.74888650e-9, 7.27263261e-12, -2.80325700e-14, 
		     3.11300149e-17, -1.22123964e-20] 
		polyR = np.polynomial.Chebyshev(r)

		rdata = 0x10
		start = 0x08

		# 1bit = 2.3e-7volts (not 2.441e-7? I don't think it matters for dT.)
		LSB = 2.3e-7  
		IDAC = .001  # 1000 microA excitation current

		#
		# HP 1 was calibrated using an ice bath. All other HP sensors
		# were calibrated in relation to HP 1 while within the vacuum
		# enclosure. Below are the resistance of each sensor when
		# HP 1 = ~23.8C
		# **Wait, this doesn't make sense why the resistances = ~100ohms
		# **Are you sure you didn't calibrate all the sensors to 
		# **an ice bath? x.x
		#
		resistance = {
			0:100.32,   1:100.432,  2:100.439, 3:100.529, 
			4:100.4005, 5:100.3736, 6:101.8879}
 
		x = True
		attempt = 0
		while x == True:
			try:
				self.bus.write_byte(self.ADD[sensor], start)
				time.sleep(0.1)
				x = False
				attempt = 0
			except:
				attempt += 1
				if attempt < 20:
					print("Timeout error: HP board %s write" 
					      %hex(self.ADD[sensor]))
					x = False
				pass

		x = True
		while x == True:
			try:
				Data = self.bus.read_i2c_block_data(
							self.ADD[sensor],rdata)
				x = False
				attempt = 0
			except:
				attempt += 1
				if attempt < 20:
					print("Timeout error: HP board %s read" 
					      %hex(self.ADD[sensor]))
					x = False
					return 11111
				pass

		# Check if sensor is disconnected.
		if Data[0: 3] == [127, 255, 255]:
			print("Sensor %s: N/C" %sensor)
			return 11111

		dec10s = Data[0] << 16
		dec11s = Data[1] << 8
		code = dec10s | dec11s | Data[2]

		Vin = LSB * code / 2
		R = Vin / IDAC
		R = R * 109.28 / resistance[sensor]  # conversion when HP 1 = ~23.8C

		output = polyR(R) - 273.15

		return output

# Used for testing without running the full temperature interface
#hp = TEMP()
#while True:
#	for x in range(6):
#		temp = hp.getTemp(x)
#		print("Sensor %s: %.2f C" %(x,temp))
#		time.sleep(0.5)
#	print("----------------")
	

