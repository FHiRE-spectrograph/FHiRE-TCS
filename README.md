# Temperature control system for FHiRE -- Updated 05/13/2021  

*Scripts posted to GITHUB  
__bold__ Important (Core) scripts.  

--------------------------------------------------------------------------------  
## Scripts on RPi #1:  

 *low-p-temp-boards.py : communicates with low precision temperature boards using SPI communications. 3 boards and uses heater relays 21-26.  
__*low_p_temp_boards.py__: a more up to date version of low-p-temp-boards.py. Sets up communication with the AD7124-8 boards. Implemented by TCS_GUI.py to read low precision sensors and toggle heater relays 21-26.   
 Test2.py : testing UART communication between the two raspberry pis.  
 relay.py : example of basic relay communication. Updated to be able to toggle relays on RPi1 and RPi2 from RPi1   
 temp_sensor.py : communicates with and querries temperature. Writes temperaure to other raspberry pi using serial communication. Paired with temp_feed.py. [replaced temp2.py]  
__*tcs.py__ : layout of temperature control front end (GUI). GUI version used for characterization (derived from tcs.ui)  
 PID_final.py : empty  
__*TCS_GUI.py__ : Temperature control system interface script using PyQt5. Monitors high precision and low precision sensors by deriving methods from TEMP.py and low_p_temp_boards.py scripts respectively. Continuously collects sensor readings into an array which is averaged after a set time span. *Currently, it takes slightly less than 50sec to read through all LP sensors once. LP sensors are read within the ~55sec period when LP relays are off. With the current setup, LP sensors are only being read through once. They can be read out more than once by either improving the readout time or increasing the frequency of the LP relay PWM.* The averaged readings are saved to individual dat files for HP and LP sensors (where LP sensors are paired to specific PID loops).   
	The duty cycle of each heating pads' PWM is calculated via individual PID loops. Each PID loop provides an updated duty cycle based on the most recent average temperature readings of the LP sensors which surround each heating pad. *The default is that each heating pad's PWM is based on its respective 2N2222 sensor (or control sensor). This may be replaced by the averaged PT100s (monitoring sensors) around each heating pad. There's a question here about whether the averaged PT100s can effectively monitor and act as a replacement for a control sensor. PT100s have a much higher RMS and are not absolutely calibrated.*   
	Target temperature and PID coefficients for individual PID loops can be updated via pid.conf without restarting the GUI script. The GUI also includes a graphing option to track the temperature readings and RMS of HP sensors, LP sensors, and PID averages.  
__*PID.py__ : Downloaded python PID controller. Functions used in TCS_GUI.py.   
__*TEMP.py__ : basic function for measuring temperature of a single high precision sensor.  
*pid.conf : example PID configuration file which can be used to update the target temp and PID coefficients of individual PID loops without restarting TCS_GUI.py.  

### Copies:  
 PID_single.py : Current working version - trash  
 PID_multiple.py : trash   

--------------------------------------------------------------------------------
## Scripts on RPi #2:  

 PID_loop_ref.py : reference for writing a PID loop.  
 PID_multiple.py : PID loop for multiple hp sensors.  
 PID_separate.py : PID loop that accesses hp sensors from another rpi.  
 PID_single.py : PID loop for a single hp sensor.  
 temp_feed.py : sets up serial communication between raspberry pis.   
 TEMP.py : copy  
 PID.py : copy  
__*relay_feed.py__ : UART script to toggle relays on RPi2 from RPi1 via relay.py. Run via pxssh in TCS_GUI.py.  

--------------------------------------------------------------------------------
## Need to:  
[x]Be able to turn on/off each of the 26 relays from one RPi.  
[x]Set up communication with low precision boards -- how do you read temperature?  
[x]Use accurate formulas to convert LP sensor voltages to temperature (resistors and diodes)  
[-]Double check chebyshev coefficients (LP resistors show high fluctuations over time.)  
[x]Add averaging sequence for sensor readings.  
[x]Integrate PWM and PID loop methods to GUI.  
[x]Add option to view temperatures of toggled sensors (not a priority).  
[]Fix disconnected HP sensors
[]Fix disconnected heating pads
[]Improve readout speed of LP sensors to take advantage of averaging
[]Improve calibration of LP sensors (especially the external 2N2222 sensors)
[]Opt: Add an external voltage reference source with a better precision for AD7124-8 boards. Currently, using the boards' internal voltage reference (5ppm/C?).
[]Opt: Determine why LP resistors have such high RMS - possibly due to the uncertainty and possibly low precision of the AD7124-8 board excitation current?



