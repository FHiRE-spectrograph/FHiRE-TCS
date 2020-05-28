# Temperature control system for FHiRE -- Updated 10/24/19  

*Scripts posted to GITHUB  

--------------------------------------------------------------------------------  
## Scripts on RPi #1:  

 *low-p-temp-boards.py : communicates with low precision temperature boards using SPI communications. 3 boards and uses heater relays 21-26?  
 Test2.py : testing UART communication between the two raspberry pis.  
 relay.py : example of basic relay commincation.  
 temp_sensor.py : communicates with and querries temperature. Writes temperaure to other raspberry pi using serial communication. Paired with temp_feed.py. [replaced temp2.py]  
 tcs.py : temperature control front end for characterization (derived from tcs.ui)  
 PID_final.py : empty  

### Copies:  
 PID.py  
 TEMP.py : Current working version  
 PID_single.py : Current working version  
 PID_multiple.py  

--------------------------------------------------------------------------------
## Scripts on RPi #2:  

 PID_loop_ref.py : reference for writing a PID loop.  
 PID_multiple.py : PID loop for multiple hp sensors.  
 PID_separate.py : PID loop that accesses hp sensors from another rpi.  
 PID_single.py : PID loop for a single hp sensor.  
 temp_feed.py : sets up serial communication between raspberry pis.   
 TEMP.py : basic function for measuring temperature of a single high precision sensor.  
 *PID.py : Downloaded python PID controller. Functions used in other scripts.  

--------------------------------------------------------------------------------
## Need to:  
[]Be able to turn on/off each of the 26 relays from one RPi.  
[]Set up communication with low precision boards -- how do you read temperature?  
[]  



