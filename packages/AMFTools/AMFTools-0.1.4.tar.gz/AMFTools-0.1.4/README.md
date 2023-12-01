

# AMF TOOLS Python Library

## Description

AMF TOOLS Python Library is a python library to control AMF products (RVMFS, RVMLP, SPM and LSPOne) with a serial connection protocol.

## Installation

### Requirements

- Python 3.8 or higher
- pyserial 3.4 or higher
- ftd2xx 1.1.2 or higher

currently only tested on Windows 11 with Python 3.11 an update will be made for alternative OS

### Installation with pip

```bash
pip install AMFTools
```

### Installation from source

```bash
git clone
cd AMFTools
python setup.py install
```
## License

This Library is proprietary software of **Advanced Microfluidics S.A**. It is distributed under a proprietary license [[1](#license-text "the licence")].

This Library is free to use for Advanced Microfluidics SA customers. It is not free to use for non-customers of Advanced Microfluidics SA.

If you have any questions about the license, please contact Advanced Microfluidics SA: 
- Chem. de la Dent d'Oche 1A, 1024 Ecublens (Switzerland)
- +41 21 552 14 30
- info@amf.ch

## Usage

*This version of the data sheet is for the version 0.1.3 of the AMFTools library.*

### Import

```python
import amfTools
```


## Class AMF(): 

```python
AMF(product : Object, autoconect : bool = True, portnumber : int = None, syringeVolume : int = None, productAddress : int = 1, type : str = None, serialBaudrate : int = None) 

```
Initialize the AMF object. Either serialPort, serialNumber or a Device type object must be specified as product.

### General Methods: 

```python
connect(serialBaudrate : int = defaultSerialBaudrate, serialTimeout : float = defaultSerialTimeout) -> bool
```
Connect to the product. If the connection is successful, return True, otherwise return False.

```python
disconnect() 
```
Disconnect from the product

```python
send(command : str, integer : bool = False, force_aws : bool = False) 
```
Send a command to the product. If the command is successful, return the response of the product. If integer is True, the response will be converted to an integer. If force_aws is True, the product will be temporarily set to wait for an answer even if it is set to not wait for an answer.

```python
receive(integer = False, full : bool = False, isfloat : bool = False) -> str
```
Receive a line of response from the product. If integer is True, the response will be converted to an integer. If full is True, the response will be returned as is, without removing the first and last character. If float is True, the response will be converted to a float.

```python
prepareCommand(command : str, parameter : int = None) -> str
```
Prepare a command to be sent to the product. If the command needs a parameter, it must be specified. The parameter must be an integer.

```python
pullAndWait(homming_mode : bool = False) 
```
Wait until the valve and the pump are not busy.

### LIST OF SET FUNCTIONS


```python
setAddress(address : int) 
```
Set the Address of the product. The Address must be between 1 and 9. (1 by default)

```python
setSyringeSize(size : int) 
```
Set the syringe size of the product. The size must be between 0 and 5000 ( $\mu l$ ). 

```python
setAnswerMode(mode : int) 
```
Set the answer mode of the product. The mode must be between 0 and 2. 0: synchronous, 1:  Asynchronous, 2: same as asynchronous but add number of subcommand processed in its last answer

```python
setPortNumber(portnumber : int = portnumber) 
```
Set the port number of the product's valves.

```python
setSpeedVolume(speed : float, syringeVolume : int = syringeSize) -> int
```
Set the speed of the product. The speed must be positive. The syringe volume must be between 0 and 5000  ( $\mu l$ ).

```python
setSpeed(speed : int) 
```
Set the speed of the product. The speed must be between 0 and 6000 (pulse/sec).

```python
setSpeedCode(speed : int) 
```
Set the speed of the product with a code. The speed must be between 0 and 50.

```python
setAccelerationRate(rate : int) 
```
Set the acceleration rate of the product. The rate must be between 1 and 59590. 

```python
setDecelerationRate(rate : int) 
```
Set the deceleration rate of the product. The rate must be between 1 and 59590.

```python
setMicrostepResolution(argument : int) 
```
Set the microstep resolution of the product. ( 0: 0.01mm resolution/step, 1: 0.00125mm resolution/step )

```python
setSlowMode() 
```
Set the slow mode of the product.

```python
setFastMode() 
```
Set the fast mode of the product.

```python
setPumpStrengthAndHome(strength : int, block : bool = True) 
```
Set the pump strength and home the pump. The strength must be between 0 and 3. If block is True, the function will wait until the pump is not busy.

```python
setPlungerForce(force : int) 
```
Set the plunger force of the product. The force must be between 0 and 3.

```python
setNoAwser() 
```
Set the product to not wait for an answer. (If the product is set to not wait for an answer, it will not send any answer even if you force it with force_aws parameters)


### LIST OF GET FUNCTIONS

```python
getSerialPort(serialNumber : str = serialNumber) -> str
```
Find the serial port of the product with the specified serial number

```python
getSerialNumber(serialPort = serialPort) -> str
```
Get the serial number of the product

```python
getType() 
```
Autoset the type of the product (SPM, RVMFS or RVMLP)
 
```python
getPortNumber() -> int
```
Get the number of port of the product's valve

```python
getCurrentStatus() -> str
```
Get the current status of the product

```python
getValvePosition() -> int
```
Get the valve position of the product

```python
getRealPlungerPosition() -> int : 
```
Get the real plunger position of the product

```python
getPlungerPosition() -> int
```
Get the plunger position of the product

```python
getNumberValveMovements() -> int
```
Get the number of valve movements of the product

```python
getNumberValveMovementsSinceLastReport() -> int
```
Get the number of valve movements since last report of the product

```python
getSpeedMode() -> str
```
Get the speed mode of the product

```python
getFirmwareChecksum() -> str
```
Get the firmware checksum of the product

```python
getFirmwareVersion() -> str
```
Get the firmware version of the product

```python
getValveAddress() -> int
```
Get the valve address of the product

```python
getValveConfiguration() -> int
```
Get the valve configuration of the product

```python
getMicrostepResolution() -> int
```
Get the microstep resolution of the product

```python
getPlungerCurrent() -> int
```
Get the plunger current of the product

```python
getAnswerMode() -> str
```
Get the answer mode of the product

```python
getAcceleration() -> int
```
Get the acceleration of the product

```python
getDeceleration() -> int
```
Get the deceleration of the product

```python
getSupplyVoltage() -> float
```
Get the supply voltage of the product

```python
getUniqueID() -> str
```
Get the unique ID of the product

```python
getValveStatus() -> int
```
Get the valve status of the product

```python
getPumpStatus() -> int
```
Get the pump status of the product

```python
getHomeStatus() -> bool
```
Get the homing status of the product (False: not homed, True: homed)

```python
getDeviceInformation() -> object
```
Get all the information of the product

### GLOBAL ACTION FUNCTIONS

```python
checkValveStatus() 
```
Check the valve status of the product

```python
checkPumpStatus() 
```
Check the pump status of the product

```python
sendBrute(command : str, blocked : bool = True, force_aws : bool = False) 
```
Send a command to the product. If blocked is True, the function will wait until the product is not busy. If force_aws is True, the function will ask for an answer even if the product is set to not wait for an answer.

```python
internalReset() 
```
Reset the product

```python
executeLastCommand() 
```
Execute the last command of the product

```python
delay(delay : int) 
```
Delay the product. The delay must be positive.

```python
home(block = True) 
```
Home the product. If block is True, the function will wait until the product is not busy.

```python
valveShortestPath(target : int, enforced : bool = False, block : bool = True) 
```
Move the valve to the target port with the shortest path. The target must be between 1 and the number of ports of the product. If enforced is True, the valve will Move to the target port with the shortest path even if it is not the shortest path. If block is True, the function will wait until the product is not busy.

```python	
valveIncrementalMove(target : int, enforced : bool = False, block : bool = True) 
```
Move the valve to the target port with an incremental Move. The target must be between 1 and the number of ports of the product. If enforced is True, the valve will Move even if they are already on the target point (1 complete rotation). If block is True, the function will wait until the product is not busy.

```python
valveClockwiseMove(target : int, enforced : bool = False, block : bool = True) 
```
Move the valve to the target port with an incremental Move. The target must be between 1 and the number of ports of the product. If enforced is True, the valve will Move even if they are already on the target point (1 complete rotation). If block is True, the function will wait until the product is not busy.

```python
valveDecrementalMove(target : int, enforced : bool = False, block : bool = True) 
```
Move the valve to the target port with a decremental Move. The target must be between 1 and the number of ports of the product. If enforced is True, the valve will Move even if they are already on the target point (1 complete rotation). If block is True, the function will wait until the product is not busy.

```python
valveCounterClockwiseMove(target : int, enforced : bool = False, block : bool = True) 
```
Move the valve to the target port with a decremental Move. The target must be between 1 and the number of ports of the product. If enforced is True, the valve will Move even if they are already on the target point (1 complete rotation). If block is True, the function will wait until the product is not busy.

```python
valveMove(target : int, mode : int = 0, enforced = False, block : bool = True) 
```
Move the valve to the target port. The target must be between 1 and the number of ports of the product. The mode must be between 0 and 2. 0: ShortestPath, 1: IncrementalMove, 2: DecrementalMove. If enforced is True, the valve will Move even if they are already on the target point (1 complete rotation). If block is True, the function will wait until the product is not busy.

```python
hardStop() 
```
Stop the product (immediate stop of the valve and the pump)

```python
powerOff() 
```
Power off the product

### PUMP ACTION FUNCTIONS

```python
pumpAbsolutePosition(position : int, block : bool = True) 
```
Move the pump to the specified position. The position must be between 0 and 3000 (or 24000). If block is True, the function will wait until the product is not busy.

```python
pump(position : int, block : bool = True)
```
Move the pump to the specified position. The position must be between 0 and 3000 (or 24000). If block is True, the function will wait until the product is not busy.

```python
pumpVolume(volume : int, syringeVolume : int = syringeSize, block : bool = True) 
```
Move the pump to the specified volume. The volume must be between 0 and 5000 ( $\mu l$ ). If syringeVolume is specified, it will be used as the syringe volume. If block is True, the function will wait until the product is not busy.

```python
pumpRelativePickup(position : int, block : bool = True) 
```
Move the pump to the specified relative position. The position must be between 0 and 3000 (or 24000). If block is True, the function will wait until the product is not busy.

```python
pumpPickup(position : int, block : bool = True)
```
Move the pump to the specified relative position. The position must be between 0 and 3000 (or 24000). If block is True, the function will wait until the product is not busy.

```python
pumpPickupVolume(volume : int, syringeVolume : int = syringeSize, block : bool = True) 
```
Move the pump to the specified relative volume. The volume must be between 0 and 5000 ( $\mu l$ ). If syringeVolume is specified, it will be used as the syringe volume. If block is True, the function will wait until the product is not busy.

```python
pumpRelativeDispense(position : int, block : bool = True) 
```
Move the pump to the specified relative position. The position must be between 0 and 3000 (or 24000). If block is True, the function will wait until the product is not busy.

```python
pumpDispense(position : int, block : bool = True)
```
Move the pump to the specified relative position. The position must be between 0 and 3000 (or 24000). If block is True, the function will wait until the product is not busy.

```python
pumpDispenseVolume(volume : int, syringeVolume : int = syringeSize, block : bool = True) 
```
Move the pump to the specified relative volume. The volume must be between 0 and 5000 ( $\mu l$ ). If syringeVolume is specified, it will be used as the syringe volume. If block is True, the function will wait until the product is not busy.

## Class Device(): 

### Attributes: 
```python	
SerialNumber : str = None
ComPort : str = None
DeviceType : str = None
```

str method return example: 
"Device RVMFS on port com3 with serial number P201-O0000xxxx"

## Class util(): 
```python
getProductList(specified_type = None) -> list : 
```
Return a list of Device object. If specified_type is specified, only the Device object with the specified type will be returned (exemple of specifie type : "SPM", "RVMFS" or "RVMLP").



# license-text


``` richtext
AMF Tools Python Package by Advanced Microfluidics SA

Copyright (C) 2023 Advanced Microfluidics SA

This Python Package is distributed to all AMF customers and partners for the sole purpose of using it with AMF products.

The right to use this Python Package is included in the price of all AMF OEM products.

REDISTRIBUTION AND USE in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
- (i) Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
- (ii) Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
- (iii) Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
- (iv) The use of this Python Package is restricted to AMF products.

WARRANTY OF EVICTION. Advanced Microfluidics SA represents and warrants: 
- (i) that it holds all the Intellectual Property Rights required to enter into the Agreement; 
- (ii) that the Advanced Microfluidics SA Service, as well as the elements necessary for their operation provided in performance of the Agreement, do not infringe the rights of third parties and do not constitute an infringement of any pre-existing work or even infringement of any other software or other intellectual creation belonging to a third party;

RESPONSIBILITY LIMITATION: This package is provided by the copyright holder and contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall the copyright holder or contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

Advanced Microfluidics SA reserves the right to modify this Agreement at any time by publishing a new version on https://amf.ch . The applicable terms and conditions are those in force on the date of the order.

NUMBER OF COPIES: The Customer may make as many copies of the package as necessary for the use of the Package in accordance with the terms of this Agreement. The Customer may make a copy of the Package for backup purposes. The Customer may not make copies of the Package for any other purpose.

DURATION: This Agreement is effective from the date of delivery of the AMF Product to the Customer and shall remain in force until terminated by either party.

TERMINATION: This Agreement shall terminate automatically if the Customer fails to comply with any of the terms and conditions of this Agreement. In such event, the Customer must destroy all copies of the package.

GEOGRAPHICAL RESTRICTIONS: The Customer may not export or re-export the Package or any copy or adaptation thereof in violation of any applicable locals laws or regulations.

GOVERNING LAW: This Agreement shall be governed by and construed in accordance with the laws of Switzerland. The parties agree that the United Nations Convention on Contracts for the International Sale of Goods is specifically excluded from application to this Agreement.

JURISDICTION: Any dispute arising out of or in connection with this Agreement shall be submitted to the exclusive jurisdiction of the courts of the Canton of Vaud, Switzerland.
```

### [BACK TO THE TOP](#amf-tools-python-library)