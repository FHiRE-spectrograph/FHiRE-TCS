# Temperature control system for FHiRE -- Updated 09/16/2020  

*Scripts posted to GITHUB  
__bold__ Important (Core) scripts.  

--------------------------------------------------------------------------------  
## Scripts on RPi #1:  

 *low-p-temp-boards.py : communicates with low precision temperature boards using SPI communications. 3 boards and uses heater relays 21-26.  
__*low_p_temp_boards.py__: a more up to date version of low-p-temp-boards.py. Sets up LP board communication within a class to be accessed by TCS_GUI.py. Includes relay (21-26) and LP sensor communication methods.   
 Test2.py : testing UART communication between the two raspberry pis.  
 *relay.py : example of basic relay communication. Updated to be able to toggle relays on RPi1 and RPi2 from RPi1   
 temp_sensor.py : communicates with and querries temperature. Writes temperaure to other raspberry pi using serial communication. Paired with temp_feed.py. [replaced temp2.py]  
__*tcs.py__ : layout of temperature control front end (GUI). GUI version used for characterization (derived from tcs.ui)  
 PID_final.py : empty  
__*TCS_GUI.py__ : Temperature control system interface script using PyQt5. Monitors HP and LP sensors by deriving methods from TEMP.py and low_p_temp_boards.py scripts respectively. Continuously collects sensor readings into an array which is averaged after a set time span. The averaged reading (and stdev) is displayed within the GUI and LP diode readings are used to calculate the duty cycle of their respective heating pads via individual PID loops (might need to be changed to LP resistors running the duty cycles). Target temperature and PID coefficients for individual PID loops can be updated via pid.conf without restarting the GUI script. Each heating pad (AKA relay) operates off of individual PWM controls. Graphic widget is not yet implemented.  
__*PID.py__ : Downloaded python PID controller. Functions used in other scripts.   
__*TEMP.py__ : basic function for measuring temperature of a single high precision sensor.  
pid.conf : example PID configuration file which can be used to update the target temp and PID coefficients of individual PID loops without restarting TCS_GUI.py.  

### Copies:  
 PID_single.py : Current working version  
 PID_multiple.py  

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
[?]Double check chebyshev coefficients (LP resistors show high fluctuations over time.)  
[x]Add averaging sequence for sensor readings.  
[x]Integrate PWM and PID loop methods to GUI.  
[]Add option to view temperatures of toggled sensors (not a priority).  



