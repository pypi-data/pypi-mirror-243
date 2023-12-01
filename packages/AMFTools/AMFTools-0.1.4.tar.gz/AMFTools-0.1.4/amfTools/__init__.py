# !/usr/bin/env python3
# -*- coding: utf-8 -*-

#*******************************************************************************
# File : __init__.py
# Package : AMFTools
# Description : This module is used to control the AMF products
# Author : Paul Giroux AMF (paul.giroux@amf.ch)
# Date Created : august 21, 2023
# Date Modified : november 30, 2023
# Version : 0.1.4
# Python Version : 3.11.4
# Dependencies : pyserial, ftd2xx
# License : all Right reserved : Proprietary license (Advanced Microfluidics S.A.)
# Contact : info [at] amf.ch
#*******************************************************************************

__version__ = "0.1.4"
__author__ = 'Paul Giroux AMF'
__credits__ = 'Advanced Microfluidics S.A.'

import serial
import time
import os

#si windows :
if os.name == 'nt':
    import ftd2xx
#si linux :
elif os.name == 'posix':
    import serial.tools.list_ports
#si mac :
else : 
    import serial.tools.list_ports

class Device:
    serialnumber : str = None
    comPort : str = None
    deviceType : str = None

    def __str__(self) -> str:
        return f"Device {self.deviceType} on port {self.comPort} with serial number {self.serialnumber}"


class AMF:
    TIME_BETWEEN_COMMAND = 0.0
    serialNumber : str = None
    firmwareVersion : str = None
    serialPort : str = None
    serialBaudrate : int = 9600
    serialTimeout : float = 0.1
    productAddress : int = 1
    productserial : serial.Serial = None
    connected : bool = False
    portnumber : int = 6
    typeProduct : str = None
    syringeSize : int = None
    pumpPosition : int = None
    responseTimeout : float = 1
    speed : int = None
    answerMode : int = 0
    valveSpeed : str = None
    acelerationRate : int = None
    decelerationRate : int = None
    microstepResolution : int = None
    valvePosition : int = None
    no_aws : bool = False


    FIRST_CHAR = '/'
    LAST_CHAR = '\r'

    fonction = {
        'setAddress' : "@ADDR=#", #Define the Address of the product
        'setAnswerMode' : "!50#", #Define the answer mode of the product
        'setPortNumber' : "!80#", #Set the port number of the product
        'setPlungerForce' : "!30#", #Set the plunger force (only for SPM et LSPOne)
        'getPortNumber' : "?801", #Get the port number of the product
        'slowMode' : "-", #Set the slow mode (only for the RVMFS)
        'fastMode' : "+", #Set the fast mode (only for the RVMFS)
        'getCurrentStatus' : "Q", #Get the current status of the product
        'getRealPlungerPosition' : "?4", #Get the real plunger position (only for SPM et LSPOne)
        'getPlungerPosition' : "?0", #Get the plunger position (only for SPM et LSPOne)
        'getValvePosition' : "?6", #Get the valve position
        'getNumberValveMovements' : "?17", #Get the number of valve movements
        'getNumberValveMovementsSinceLastReport' : "?18", #Get the number of valve movements since last get
        'getSpeedMode' : "?19", #Get the speed mode
        'getFirmwareChecksum' : "?20", #Get the firmware checksum
        'getFirmwareVersion' : "?23", #Get the firmware version
        'getAcceleration' : "?25", #Get the acceleration slope setting (only for SPM et LSPOne)
        'getValveAddress' : "?26", #Get the valve or pump Address
        'getDeceleration' : "?27", #Get the deceleration slope setting (only for SPM et LSPOne)
        'getMicrostepResolution' : "?28", #Get the microstep mode (only for SPM et LSPOne)
        'getPlungerCurrent' : "?300", #Get the plunger current (only for SPM et LSPOne)
        'getAnswerMode' : "?500", #Get the answer mode
        'getValveConfiguration' : "?76", #Get the valve configuration
        'internalReset' : "$", #Reset the product
        'getSuplyVoltage' : "*", #Get the supply voltage
        'getUniqueID' : "?9000", #Get the unique ID
        'gethomedSPM' : "?9010", #Get the homed status (only for SPM et LSPOne)
        'gethomedRVM' : "?6", #Get the homed status (only for RVMLP et RVMFS)
        'getValveStatus' : "?9200", #Get the valve status
        'getPumpStatus' : "?9100", #Get the pump status (only for SPM et LSPOne)
        'executeLastCommand' : "XR", #Execute the last command
        'delay' : "M#R", #Delay in ms
        'home' : "ZR", #Move to the home position
        'enforcedShortestPath' : "B#R", #Move to the shortest path make 360° if target port is the current position
        'shortestPath' : "b#R", #Move to the shortest path no Move if target port is the current position
        'enforcedIncrementalMove' : "I#R", #Move to the clockwise path make 360° if target port is the current position
        'incrementalMove' : "i#R", #Move to the clockwise path no Move if target port is the current position
        'enforcedDecementalMove' : "O#R", #Move to the counter clockwise path make 360° if target port is the current position
        'decrementalMove' : "o#R", #Move to the counter clockwise path no Move if target port is the current position
        'hardStop' : "T", #Stop the pump (only for SPM et LSPOne)
        'powerOff' : "@POWEROFF", #Power off the product (only for SPM et LSPOne)
        'forceAndHome' : "Y#R", #set force and go to home position (only for SPM et LSPOne)
        'AbsolutePumpPosition' : "A#R", #Set the pump absolute position (only for SPM et LSPOne)
        'RelativePumpPickup' : "P#R", #pump relative pickup (only for SPM et LSPOne)
        'RelativePumpDispense' : "D#R", #pump relative dispense (only for SPM et LSPOne)
        'setSpeed' : "V#R", #Set the pump speed (only for SPM et LSPOne)
        'setSpeedCode' : "S#R", #Set the pump speed with code set on the operationg manuel 6.2 table (only for SPM et LSPOne)
        'acelerationRate' : "L#R", #Set the pump aceleration rate pulse/Sec² (only for SPM et LSPOne) 
        'decelerationRate' : "l#R", #Set the pump deceleration rate pulse/sec² (only for SPM et LSPOne)
        'scalingArgument' : "N#R", #Set the pump scaling argument (only for SPM et LSPOne)
    }

    ERROR_CODES = {'@': [0, 'No Error'],
                'M': [0, 'No Error'],
                "`": [0, 'No Error'],
                'A': [1, 'Initialization'],
                'B': [2, 'Invalid command'],
                'C': [3, 'Invalid operand'],
                'D': [4, 'Missing trailing [R]'],
                'G': [7, 'Device not initialized'],
                'H': [8, 'Internal failure (valve)'],
                'I': [9, 'Plunger overload'],
                'J': [10, 'Valve overload'],
                'N': [14, 'A/D converter failure'],
                'O': [15, 'Command overflow'], }

    VALVE_ERROR = {
        '255': [255, 'Busy', 'Valve currently executing an instruction.'],
        '0': [0, 'Done', 'Valve available for next instruction.'],
        '128': [128, 'Unknown command', 'Check that the command is written properly'],
        '144': [144, 'Not homed', 'You forgot the homing! Otherwise, check that you have the right port configuration and try again.'],
        '145': [145, 'Move out of range', 'You\'re probably trying to do a relative positioning and are too close to the limits.'],
        '146': [146, 'Speed out of range', 'Check the speed that you\'re trying to go at.'],
        '224': [224, 'Blocked', 'Something prevented the valve to move.'],
        '225': [225, 'Sensor error', 'Unable to read position sensor. This probably means that the cable is disconnected.'],
        '226': [226, 'Missing main reference', ('Unable to find the valve\'s main reference magnet '
                                                'during homing. This can mean that a reference magnet '
                                                'of the valve is bad/missing or that the motor is '
                                                'blocked during homing. Please also check motor '
                                                'cables and crimp.')],
        '227': [227, 'Missing reference', ('Unable to find a valve\'s reference magnet during '
                                            'homing. Please check that you have the correct valve '
                                            'number configuration with command "/1?801". If '
                                            'not, change it according to the valve you are working '
                                            'with. This can also mean that a reference magnet of '
                                            'the valve is bad/missing or that the motor is blocked '
                                            'during homing.')],
        '228': [228, 'Bad reference polarity', ('One of the magnets of the reference valve has a bad '
                                                'polarity. Please check that you have the correct valve '
                                                'number configuration with command "/1?801". If '
                                                'not, change it according to the valve you are working '
                                                'with. This can also mean that a reference magnet has '
                                                'been assembled in the wrong orientation in the valve.')],
    }

    PUMP_ERROR = {
        '255': [255, 'Busy', 'Pump currently executing an instruction.'],
        '0': [0, 'Done', 'Pump available for next instruction.'],
        '128': [128, 'Unknown command', 'Check that the command is written properly'],
        '144': [144, 'Not homed', 'You forgot the homing! Otherwise, check that you have the right port configuration and try again.'],
        '145': [145, 'Move out of range', 'You\'re probably trying to do a relative positioning and are too close to the limits.'],
        '146': [146, 'Speed out of range', 'Check the speed that you\'re trying to go at.'],
        '224': [224, 'Blocked', 'Something prevented the pump to move.'],
        '225': [225, 'Sensor error', 'Unable to read position sensor. This probably means that the cable is disconnected.'],
    }


    def __init__(self, product, autoconect = True, portnumber: int = None, syringeVolume : int = None, productAddress : int = 1, type : str = None, serialBaudrate : int = None) -> None:
        """
        INPUTS:
            product: # product to connect to. Can be a serial port, a serial number or a Device objectZ
            portnumber: int # Number of ports on the product. Default: 6
            syringeVolume: int # Volume of the syringe in µL.
            serialBaudrate: int # Baudrate to use for the serial connection. Default: 9600
            productAddress: int # Address of the product to connect to. Default: 1

        OUTPUTS:
            None

        Initialize the AMF object. Either serialPort or serialNumber must be specified. 
        If serialPort is specified, serialNumber will be automatically found
        If serialNumber is specified, serialPort will be automatically found
        """
        if isinstance(product, Device):
            device = product
            serialPort = None
            serialNumber = None
        elif isinstance(product, str):
            if product.replace(" ", "")[0] == 'P':
                serialNumber = product
                serialPort = None
                device = None
            else:
                serialPort = product
                serialNumber = None
                device = None

        fct = self.fonction.copy()
        for key, value in fct.items():
            self.fonction[key.lower()] = value

        if portnumber is not None: self.portnumber = portnumber
        if syringeVolume is not None: self.syringeSize = syringeVolume

        if device is not None:
            self.serialPort = device.comPort
            self.serialNumber = device.serialnumber
            self.typeProduct = device.deviceType
        else:
            if serialPort is not None:
                self.serialPort = serialPort
                self.serialNumber = self.getSerialNumber()
            elif serialNumber is not None:
                self.serialNumber = serialNumber
                self.serialPort = self.getSerialPort()
            else:
                raise ConnectionError("No serial port, serial number or device specified")
            
        if serialBaudrate is not None:
            self.serialBaudrate = serialBaudrate
        if productAddress != 1:
            self.productAddress = productAddress
        if type is not None:
            self.typeProduct = type
        
        if autoconect:
            self.connect()

    def connect(self, serialBaudrate : int = serialBaudrate, serialTimeout : float = serialTimeout) -> bool:
        """
        INPUTS:
            serialBaudrate: int # Baudrate to use for the serial connection. Default: 9600
            serialTimeout: float # Timeout to use for the serial connection. Default: 0.1
        OUTPUTS:
            bool # True if the connection was successful, False otherwise
        """
        try : self.disconnect() 
        except: pass
        if serialBaudrate is not None: self.serialBaudrate = serialBaudrate
        if serialTimeout is not None: self.serialTimeout = serialTimeout

        if self.serialPort is None and self.serialNumber is not None: self.serialPort = self.getSerialPort()
        elif self.serialPort is None: raise ConnectionError("No serial port or serial number specified")
        try :
            self.productserial = serial.Serial(self.serialPort, self.serialBaudrate, timeout=self.serialTimeout)
            self.connected = True
            if self.typeProduct is None:
                self.getType()
            if self.portnumber is None:
                self.portnumber = self.getPortNumber(integer = True)
            return True
        except serial.SerialException as e:
            self.connected = False
            raise ConnectionError("Could not connect to product on port " + self.serialPort)
            return False
        
    def disconnect(self) -> None:
        """ Disconnect from the product """
        if self.connected:
            self.productserial.close()
        else:
            raise ConnectionError("product is not connected")
    
    def send(self, command : str, integer : bool = False, force_aws : bool = False) -> None:
        """
        INPUTS:
            command: str # Command to send to the product. Example: "/1ZR"
        OUTPUTS:
            None

        if the product is connected, send the command to the product
        """
        if self.connected:
            self.productserial.write(command.encode())
        else:
            raise ConnectionError("product is not connected")
        time.sleep(self.TIME_BETWEEN_COMMAND)
        if self.no_aws and not force_aws:
            return
        return self.receive(integer=integer)
        
    def receive(self, integer=False, full=False, float = False) -> str:
        """
        INPUTS:
            integer: bool # If True, the response will be converted to an integer
            full: bool # If True, the response will be returned as is, without removing the first and last character
        OUTPUTS:
            str # Response from the product
        
        receive a line of response from the product
        """
        if self.connected:
            response = self.productserial.readline().decode()
            timeout = time.time() + self.responseTimeout
            while response == "" and time.time() < timeout:
                response = self.productserial.readline().decode()
                time.sleep(0.01)
                if response != "":
                    break
            if response != "":
                if full:
                    return response
                response = response.replace("\r", "").replace("\n", "").replace(" ", "").replace("/0", "").replace("`", "").replace("@", "")
                response = response[0:len(response)-1]
                if integer:
                    try :
                        response = int(response)
                        return response
                    except ValueError as e:
                        #print(response , " is not an integer")
                        return self.receive(integer = True)
                if float:
                    try :
                        response = float(response)
                        return response
                    except ValueError as e:
                        print(response , " is not a float")
                        return self.receive(float = True)
                if response.upper() in self.ERROR_CODES.keys():
                    raise Exception("error " + response.upper() + " : " + self.ERROR_CODES[response.upper()][1])
                return response
        else:
            raise ConnectionError("product is not connected")
    
    def prepareCommand(self, command : str, parameter = None) -> str:
        """
        INPUTS:
            command: str
        OUTPUTS:
            str
        """
        preparedComande : str = self.FIRST_CHAR + str(self.productAddress) + self.fonction[command.lower()] + self.LAST_CHAR
        if '#' in  preparedComande and parameter is not None:
             preparedComande =  preparedComande.replace('#', str(parameter))
        elif '#' in  preparedComande and parameter is None:
            raise ValueError("Commande "+command+ "need a parameter")
        return preparedComande
    
    def pullAndWait(self, homming_mode = False)->None:
        valvebusy = True
        pumpbusy = True
        #print("type produit : ---"+self.typeProduct+"---")
        while valvebusy or pumpbusy:
            time.sleep(self.TIME_BETWEEN_COMMAND)
            response = self.checkValveStatus()
            if response[0] != 255 and response[0] == 0:
                valvebusy = False
            elif homming_mode and response[0] == 144:
                valvebusy = True
            elif response[0] != 255:
                raise Exception("Valve error : "+str(response[1]+" : "+response[2]))
            else:
                valvebusy = True
            if self.typeProduct == "SPM" or self.typeProduct == "LSPOne":
                response = self.checkPumpStatus()
                if response[0] != 255 and response[0] == 0:
                    pumpbusy = False
                elif homming_mode and response[0] == 144:
                    valvebusy = True
                elif response[0] != 255:
                    raise Exception("Pump error : "+str(response[1]+" : "+response[2]))
                else:
                    pumpbusy = True
            else:
                pumpbusy = False

############################################################################################################
#                                                                                                          #
#                                           LIST OF SET FUNCTION                                           #
#                                                                                                          #
############################################################################################################
    def setAddress(self, address : int) -> None:
        """
        INPUTS:
            Address: int # Address of the  [[1; 9]]
        OUTPUTS:
            None
        """
        if address < 1 or address > 9:
            raise ValueError("Address must be between 1 and 9")
        self.productAddress = address
        self.send(self.prepareCommand('setAddress', address))

    def setSyringeSize(self, size : int) -> None:
        """
        INPUTS:
            size: int # Size of the syringe in µL [[0; 5000]]
        OUTPUTS:
            None
        """
        if size < 0 or size > 5000:
            raise ValueError("Size must be between 0 and 5000")
        self.syringeSize = size

    def setAnswerMode(self, mode : int) -> None:
        """
        INPUTS:
            mode: int # mode de reponse [[0; 2]] 0: synchronous, 1: Asynchronous, 2: same as asynchronous but add number of subcommand processed in its last answer
        OUTPUTS:
            None
        """
        if mode < 0 or mode > 2:
            raise ValueError("Mode must be between 0 and 2")
        self.answerMode = mode
        self.send(self.prepareCommand('setAnswerMode', mode))

    def setPortNumber(self, portnumber : int = portnumber) -> None:
        """
        INPUTS:
            portnumber: int # number of port on the RVM [[1; 48]]
        OUTPUTS:
            None
        """
        self.portnumber = portnumber
        if portnumber < 1 or portnumber > 48:
            raise ValueError("Port number must be between 1 and 48")
        self.send(self.prepareCommand('setPortNumber', portnumber))

    def setSpeedVolume(self, speed : float, syringeVolume: int = syringeSize) -> int:
        """
        INPUTS:
            speed: float # Speed in ul/s [[0; +inf]]
            syringeVolume: float # Syringe volume in ul [[0; 5000]]
        OUTPUTS:
            int # Speed value
        """
        if syringeVolume != self.syringeSize and syringeVolume is not None:
            self.syringeSize = syringeVolume

        if self.typeProduct != "SPM":
            raise ValueError("Set speed volume is only for SPM and LSPOne")
        if speed < 0:
            raise ValueError("Speed must be positive")
        
        if self.syringeSize < 0 or self.syringeSize is None:
            raise ValueError("Syringe volume must be between 0 and 5000")
        
        time = self.syringeSize / speed
        speedValue = int(time * 1000 / 3)
        self.speed = speedValue
        self.send(self.prepareCommand('setSpeedVolume', speedValue))

    def setSpeed(self, speed : int) -> None:
        """
        INPUTS:
            speed: int
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Set speed is only for SPM and LSPOne")
        self.speed = speed
        self.send(self.prepareCommand('setSpeed', speed))

    def setSpeedCode(self, speed : int) -> None:
        """
        INPUTS:
            speed: int
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Set speed code is only for SPM and LSPOne")
        self.speed = None
        self.send(self.prepareCommand('setSpeedCode', speed))
       
    def setAccelerationRate(self, rate : int) -> None:
        """
        INPUTS:
            rate: int [[100; 59590]]
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Aceleration rate is only for SPM and LSPOne")
        if rate < 100 or rate > 59590:
            raise ValueError("Rate must be between 100 and 59590")
        self.send(self.prepareCommand('acelerationRate', rate))
        self.acelerationRate = rate

    def setDecelerationRate(self, rate : int) -> None:
        """
        INPUTS:
            rate: int [[100; 59590]]
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Deceleration rate is only for SPM and LSPOne")
        if rate < 100 or rate > 59590:
            raise ValueError("Rate must be between 100 and 59590")
        self.send(self.prepareCommand('decelerationRate', rate))
        self.decelerationRate = rate

    def setMicrostepResolution(self, argument : int) -> None:
        """
        INPUTS:
            argument: int [[0; 1]] # 0 : 0.01mm resolution/step, 1 : 0.00125mm resolution/step
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Scaling argument is only for SPM and LSPOne")
        if argument < 0 or argument > 1:
            raise ValueError("Argument must be between 0 and 1")
        self.send(self.prepareCommand('scalingArgument', argument))
        self.microstepResolution = argument
 
    def setSlowMode(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        if self.typeProduct != "RVMFS":
            raise ValueError("Slow mode is only for RVMFS")
        self.send(self.prepareCommand('slowMode'))
        self.valveSpeed = "slow"
    
    def setFastMode(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        if self.typeProduct != "RVMFS":
            raise ValueError("Fast mode is only for RVMFS")
        self.send(self.prepareCommand('fastMode'))
        self.valveSpeed = "fast"

    def setPumpStrengthAndHome(self, strength : int, block : bool = True) -> None:
        """
        INPUTS:
            None
        OUTPUTS: self.typeProduct !=
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Force and home is only for SPM and LSPOne")
        self.send(self.prepareCommand('forceAndHome', strength))

        if block: self.pullAndWait()
        self.pumpPosition = 0
    
    def setPlungerForce(self, force : int) -> None:
        """
        INPUTS:
            force: int
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Plunger force is only for SPM and LSPOne")
        self.send(self.prepareCommand('setPlungerForce', force))

    def setNoAwser(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        self.no_aws = True


############################################################################################################
#                                                                                                          #
#                                           LIST OF GET FUNCTION                                           #
#                                                                                                          #
############################################################################################################
    def getSerialPort(self, serialNumber : str = serialNumber) -> str:
        """
        INPUTS:
            serialNumber: str # Serial number of the product to connect to. Example: "P201-O00000001"
        OUTPUTS:
            str # Serial port to connect to. Example: "COM3"
        
        Find the serial port of the product with the specified serial number
        """
        if serialNumber is not None: self.serialNumber = serialNumber
        if self.serialNumber is not None:
            if os.name == 'nt': #si windows
                list_available_device = ftd2xx.listDevices()
                for i in range(len(list_available_device)):
                    if list_available_device[i].decode() == self.serialNumber:
                        device = ftd2xx.open(i)
                        comport = device.getComPortNumber()
                        device.close()
                        if comport is not None:
                            self.serialPort = "COM" + str(comport)
                            return "COM" + str(comport)
            elif os.name == 'posix': #si linux
                list_com_port = serial.tools.list_ports.comports()
                for com in list_com_port:
                    if com.serial_number == self.serialNumber:
                        self.serialPort = com.device
                        return com.device
            else : #si mac
                list_com_port = serial.tools.list_ports.comports()
                for com in list_com_port:
                    if com.serial_number == self.serialNumber:
                        self.serialPort = com.device
                        return com.device

        else:
            raise ConnectionError("No serial number specified")
        
    def getSerialNumber(self, serialPort = serialPort) -> str:
        """ 
        INPUTS:
            serialPort: str # Serial port to connect to. Example: "COM3"
        OUTPUTS:
            str # Serial number of the product to connect to. Example: "P201-O00000001"

        Get the serial number of the product 
        """
        if serialPort is not None:
            self.serialPort = serialPort
        if self.serialNumber is not None:
            return self.serialNumber
        if self.connected:
            self.disconnect()
        if os.name == 'nt': #si windows
            list_available_device = ftd2xx.listDevices()
            if list_available_device is None: return None
            for i in range(len(list_available_device)):
                device = ftd2xx.open(i)
                comport = device.getComPortNumber()
                device.close()
                if ("com"+str(comport)).lower().replace(" ", "") == self.serialPort.lower().replace(" ", ""):
                    self.serialNumber = list_available_device[i]
                    return self.serialNumber
        if os.name == 'posix': #si linux
            list_com_port = serial.tools.list_ports.comports()
            for com in list_com_port:
                if com.device.lower().replace(" ", "") == self.serialPort.lower().replace(" ", ""):
                    self.serialNumber = com.serial_number
                    return self.serialNumber
        else:  #si mac
            list_com_port = serial.tools.list_ports.comports()
            for com in list_com_port:
                if com.device.lower().replace(" ", "") == self.serialPort.lower().replace(" ", ""):
                    self.serialNumber = com.serial_number
                    return self.serialNumber
        raise ConnectionError("Could not find serial number")
    
    def getType(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        
        Autoset the type of the product
        """
        if self.connected:
            response = self.send(self.prepareCommand('getValveConfiguration'), force_aws=True)
            if "RVMFS" in response:
                self.typeProduct = "RVMFS"
            elif "SPM" in response:
                self.typeProduct = "SPM"
            elif "LSP" in response:
                self.typeProduct = "SPM"
            elif "RVMLP" in response:
                self.typeProduct = "RVMLP"
            else :
                raise Exception("Type of product not found")
            return self.typeProduct
        else:
            raise ConnectionError("product is not connected")

    def getPortNumber(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int # number of port on the RVM [[1; 48]]
        """
        self.portnumber = self.send(self.prepareCommand('getPortNumber'), integer = True, force_aws=True)
        return self.portnumber
    
    def getCurrentStatus(self) -> str:
        """
        INPUTS:
            None
        OUTPUTS:
            int # Current status of the product
        """
        return self.send(self.prepareCommand('getCurrentStatus'), force_aws=True)
    
    def getValvePosition(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        self.valvePosition = self.send(self.prepareCommand('getValvePosition'), integer = True, force_aws=True)
        return self.valvePosition
    
    def getNumberValveMovements(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        return self.send(self.prepareCommand('getNumberValveMovements'), integer = True, force_aws=True)
    
    def getNumberValveMovementsSinceLastReport(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        return self.send(self.prepareCommand('getNumberValveMovementsSinceLastReport'), integer = True, force_aws=True)
    
    def getSpeedMode(self) -> str:
        """
        INPUTS:
            None
        OUTPUTS:
            str # Speed mode (exemple : "0:slowmode")
        """
        if self.typeProduct != "RVMFS":
            raise ValueError("Speed mode is only for RVMFS")
        self.speedMode = self.send(self.prepareCommand('getSpeedMode'), force_aws=True)
        return self.speedMode
    
    def getFirmwareChecksum(self) -> str:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        return self.send(self.prepareCommand('getFirmwareChecksum'), force_aws=True)
        
    def getFirmwareVersion(self) -> str:
        """
        INPUTS:
            None
        OUTPUTS:
            str
        """
        self.firmwareVersion = self.send(self.prepareCommand('getFirmwareVersion'), force_aws=True)
        return self.firmwareVersion  
    
    def getValveAddress(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        self.productAddress = self.send(self.prepareCommand('getValveAddress'), integer = True, force_aws=True)
        return self.productAddress
        
    def getValveConfiguration(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        return self.send(self.prepareCommand('getValveConfiguration'), force_aws=True)
    
    def getMicrostepResolution(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Microstep resolution is only for SPM and LSPOne")
        self.microstepResolution = self.send(self.prepareCommand('getMicrostepResolution'), integer = True, force_aws=True)
        return self.microstepResolution
    
    def getPlungerCurrent(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Plunger current is only for SPM and LSPOne")
        return self.send(self.prepareCommand('getPlungerCurrent'), integer = True, force_aws=True)

    def getAnswerMode(self) -> str:
        """
        INPUTS:
            None
        OUTPUTS:
            str # Answer mode (exemple : Synchronousmode)"
        """
        return self.send(self.prepareCommand('getAnswerMode'), force_aws=True)

    def getAcceleration(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Acceleration is only for SPM and LSPOne")
        return self.send(self.prepareCommand('getAcceleration'), integer = True, force_aws=True)
    
    def getDeceleration(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Deceleration is only for SPM and LSPOne")
        return self.send(self.prepareCommand('getDeceleration'), integer = True, force_aws=True)

    def getSupplyVoltage(self) -> float:
        """
        INPUTS:
            None
        OUTPUTS:
            float
        """
        self.send(self.prepareCommand('getSuplyVoltage'), force_aws=True)
        
        return self.receive(float = True)
    
    def getUniqueID(self) -> str:
        """
        INPUTS:
            None
        OUTPUTS:
            str
        """
        return self.send(self.prepareCommand('getUniqueID'), force_aws=True)
    
    def getValveStatus(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        return self.send(self.prepareCommand('getValveStatus'),integer = True, force_aws = True)
    
    def getPumpStatus(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Pump status is only for SPM and LSPOne")
        return self.send(self.prepareCommand('getPumpStatus'), integer = True, force_aws = True)
    
    def getHomeStatus(self) -> bool:
        """
        INPUTS:
            None
        OUTPUTS:
            bool
        """
        if self.typeProduct != "SPM":
            resp = self.send(self.prepareCommand('gethomedRVM'), integer = True, force_aws=True)
            if resp == 0:
                return False
            else:
                return True
        else:
            resp = self.send(self.prepareCommand('gethomedSPM'), integer = True, force_aws=True)
            if resp == 0:
                return False
            else:
                return True
            
    def getDeviceInformation(self) -> object:
        """
        INPUTS:
            None
        OUTPUTS:
            object
        """
        if self.typeProduct == "RVMFS" :
            info = {}
            try: info["serialNumber"] = self.getSerialNumber() 
            except : info["serialNumber"] = None
            try : info["serialPort"] = self.getSerialPort()
            except : info["serialPort"] = None
            try: info["type"] = self.getType()
            except : info["type"] = None
            try: info["portNumber"] = self.getPortNumber()
            except : info["portNumber"] = None
            try: info["speedMode"] = self.getSpeedMode()
            except : info["speedMode"] = None
            try: info["firmwareVersion"] = self.getFirmwareVersion()
            except : info["firmwareVersion"] = None
            try: info["valveAddress"] = self.getValveAddress()
            except : info["valveAddress"] = None
            try: info["valveConfiguration"] = self.getValveConfiguration()
            except : info["valveConfiguration"] = None
            try: info["currentStatus"] = self.getCurrentStatus()
            except : info["currentStatus"] = None
            try: info["valveStatus"] = self.getValveStatus()
            except : info["valveStatus"] = None
            try: info["valvePosition"] = self.getValvePosition()
            except : info["valvePosition"] = None
            try: info["numberValveMovements"] = self.getNumberValveMovements()
            except : info["numberValveMovements"] = None
            try: info["numberValveMovementsSinceLastReport"] = self.getNumberValveMovementsSinceLastReport()
            except : info["numberValveMovementsSinceLastReport"] = None
            try: info["uniqueID"] = self.getUniqueID()
            except : info["uniqueID"] = None
            try: info["answerMode"] = self.getAnswerMode()
            except : info["answerMode"] = None
            try: info["firmwareChecksum"] = self.getFirmwareChecksum()
            except : info["firmwareChecksum"] = None
            try: info["home"] = self.getHomeStatus()
            except : info["home"] = None
            return info
        elif self.typeProduct == "SPM" or self.typeProduct == "LSPOne":
            info = {}
            try: info["serialNumber"] = self.getSerialNumber() 
            except : info["serialNumber"] = None
            try : info["serialPort"] = self.getSerialPort()
            except : info["serialPort"] = None
            try: info["type"] = self.getType()
            except : info["type"] = None
            try: info["portNumber"] = self.getPortNumber()
            except : info["portNumber"] = None
            try: info["syringeSize"] = self.syringeSize
            except : info["syringeSize"] = None
            try: info["firmwareVersion"] = self.getFirmwareVersion()
            except : info["firmwareVersion"] = None
            try: info["valveAddress"] = self.getValveAddress()
            except : info["valveAddress"] = None
            try: info["valveConfiguration"] = self.getValveConfiguration()
            except : info["valveConfiguration"] = None
            try: info["currentStatus"] = self.getCurrentStatus()
            except : info["currentStatus"] = None
            try: info["valveStatus"] = self.getValveStatus()
            except : info["valveStatus"] = None
            try: info["pumpStatus"] = self.getPumpStatus()
            except : info["pumpStatus"] = None
            try: info["valvePosition"] = self.getValvePosition()
            except : info["valvePosition"] = None
            try: info["numberValveMovements"] = self.getNumberValveMovements()
            except : info["numberValveMovements"] = None
            try: info["numberValveMovementsSinceLastReport"] = self.getNumberValveMovementsSinceLastReport()
            except : info["numberValveMovementsSinceLastReport"] = None
            try: info["uniqueID"] = self.getUniqueID()
            except : info["uniqueID"] = None
            try: info["answerMode"] = self.getAnswerMode()
            except : info["answerMode"] = None
            try: info["firmwareChecksum"] = self.getFirmwareChecksum()
            except : info["firmwareChecksum"] = None
            try: info["microstepResolution"] = self.getMicrostepResolution()
            except : info["microstepResolution"] = None
            try: info["plungerCurrent"] = self.getPlungerCurrent()
            except : info["plungerCurrent"] = None
            try: info["home"] = self.getHomeStatus()
            except : info["home"] = None
            try : info['acceleration'] = self.getAcceleration()
            except : info['acceleration'] = None
            try : info['deceleration'] = self.getDeceleration()
            except : info['deceleration'] = None
            return info
        elif self.typeProduct == "RVMLP":
            info = {}
            try: info["serialNumber"] = self.getSerialNumber() 
            except : info["serialNumber"] = None
            try : info["serialPort"] = self.getSerialPort()
            except : info["serialPort"] = None
            try: info["type"] = self.getType()
            except : info["type"] = None
            try: info["portNumber"] = self.getPortNumber()
            except : info["portNumber"] = None
            try: info["firmwareVersion"] = self.getFirmwareVersion()
            except : info["firmwareVersion"] = None
            try: info["valveAddress"] = self.getValveAddress()
            except : info["valveAddress"] = None
            try: info["valveConfiguration"] = self.getValveConfiguration()
            except : info["valveConfiguration"] = None
            try: info["currentStatus"] = self.getCurrentStatus()
            except : info["currentStatus"] = None
            try: info["valveStatus"] = self.getValveStatus()
            except : info["valveStatus"] = None
            try: info["valvePosition"] = self.getValvePosition()
            except : info["valvePosition"] = None
            try: info["numberValveMovements"] = self.getNumberValveMovements()
            except : info["numberValveMovements"] = None
            try: info["numberValveMovementsSinceLastReport"] = self.getNumberValveMovementsSinceLastReport()
            except : info["numberValveMovementsSinceLastReport"] = None
            try: info["uniqueID"] = self.getUniqueID()
            except : info["uniqueID"] = None
            try: info["answerMode"] = self.getAnswerMode()
            except : info["answerMode"] = None
            try: info["firmwareChecksum"] = self.getFirmwareChecksum()
            except : info["firmwareChecksum"] = None
            try: info["home"] = self.getHomeStatus()
            except : info["home"] = None
            return info
        else:
            raise ValueError("Type of product not found")

    def getRealPlungerPosition(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Real plunger position is only for SPM and LSPOne")
        self.pumpPosition = self.send(self.prepareCommand('getRealPlungerPosition'), integer = True, force_aws=True)
        return self.pumpPosition
    
    def getPlungerPosition(self) -> int:
        """
        INPUTS:
            None
        OUTPUTS:
            int
        """
        if self.typeProduct != "SPM" and self.typeProduct != "LSPOne":
            raise ValueError("Plunger position is only for SPM and LSPOne")
        self.pumpPosition = self.send(self.prepareCommand('getPlungerPosition'), integer = True, force_aws=True)
        return self.pumpPosition

############################################################################################################
#                                                                                                          #
#                                          GLOBAL ACTION FUNCTION                                          #
#                                                                                                          #
############################################################################################################
             
    def checkValveStatus(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        response = self.getValveStatus()
        try : return self.VALVE_ERROR[str(response)]
        except KeyError as e: raise KeyError(f"Valve status {response} not found")
    
    def checkPumpStatus(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        response = self.getPumpStatus()
        try : return self.PUMP_ERROR[str(response)]
        except KeyError as e: raise KeyError(f"Pump status {response} not found")

    def sendBrute(self, command : str, blocked : bool = True, force_aws : bool = False) -> None:
        """
        INPUTS:
            command: str
        OUTPUTS:
            None
        """
        if self.connected:
            preparedComande : str = self.FIRST_CHAR + str(self.productAddress) + command + self.LAST_CHAR
            aws = self.send(preparedComande, force_aws=force_aws)
            if blocked :
                self.pullAndWait()
            if not(self.no_aws) or force_aws:
                return aws
        else:
            raise ConnectionError("product is not connected")
    
    def internalReset(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        self.send(self.prepareCommand('internalReset'))

    def executeLastCommand(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        self.send(self.prepareCommand('executeLastCommand'))

    def delay(self, delay : int) -> None:
        """
        INPUTS:
            delay: int # Delay in ms [[0; +inf]]
        OUTPUTS:
            None
        """
        if delay < 0:
            raise ValueError("Delay must be positive")
        self.send(self.prepareCommand('delay', delay))

    def home(self, block= True) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        self.send(self.prepareCommand('home'))
        if block: self.pullAndWait(homming_mode=True)

    def valveShortestPath(self, target: int, enforced : bool = False, block : bool = True) -> None:
        """
        INPUTS:
            target: int # Target port [[1; nbPort]]
            enforced: bool # Enforced shortest path
        OUTPUTS:
            None
        """
        if target < 1 or target > self.portnumber:
            raise ValueError("Target must be between 1 and "+str(self.portnumber))
        if enforced:
            self.send(self.prepareCommand('enforcedShortestPath', target))
        else:
            self.send(self.prepareCommand('ShortestPath', target))
        
        if block: self.pullAndWait()
    
    def valveIncrementalMove(self, target: int, enforced : bool = False, block : bool = True) -> None:
        """
        INPUTS:
            target: int
            enforced: bool
        OUTPUTS:
            None
        """
        if target < 1 or target > self.portnumber:
            raise ValueError("Target must be between 1 and "+str(self.portnumber))
        if enforced:
            self.send(self.prepareCommand('enforcedIncrementalMove', target))
        else:
            self.send(self.prepareCommand('IncrementalMove', target))

        if block: self.pullAndWait()
    
    def valveClockwiseMove(self, target: int, enforced : bool = False, block : bool = True) -> None:
        self.valveIncrementalMove(target, enforced= enforced, block = block)

    def valveDecrementalMove(self, target: int, enforced : bool = False, block : bool = True) -> None:
        """
        INPUTS:
            target: int
            enforced: bool
        OUTPUTS:
            None
        """
        if target < 1 or target > self.portnumber:
            raise ValueError("Target must be between 1 and "+str(self.portnumber))
        if enforced:
            self.send(self.prepareCommand('enforcedDecementalMove', target))
        else:
            self.send(self.prepareCommand('DecrementalMove', target))

        if block: self.pullAndWait()

    def valveCounterClockwiseMove(self, target: int, enforced : bool = False, block : bool = True) -> None:
        self.valveDecrementalMove(target, enforced = enforced, block = block)

    def valveMove(self, target: int, mode:int = 0, enforced = False, block : bool = True):
        """
        INPUTS:
            target: int
            mode: int # 0: ShortestPath, 1: IncrementalMove, 2: DecrementalMove
            enforced: bool
        OUTPUTS:
            None
        """
        if mode == 0:
            self.valveShortestPath(target, enforced)
        elif mode == 1:
            self.valveIncrementalMove(target, enforced)
        elif mode == 2:
            self.valveDecrementalMove(target, enforced)
        else:
            raise ValueError("Mode must be between 0 and 2")
        
        if block: self.pullAndWait()
    
    def hardStop(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Hard stop is only for SPM and LSPOne")
        self.send(self.prepareCommand('hardStop'))
    
    def powerOff(self) -> None:
        """
        INPUTS:
            None
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Power off is only for SPM and LSPOne")
        self.send(self.prepareCommand('powerOff'))

############################################################################################################
#                                                                                                          #
#                                           PUMP ACTION FUNCTION                                           #
#                                                                                                          #
############################################################################################################
    def pumpAbsolutePosition(self, position : int, block : bool = True) -> None:
        """
        INPUTS:
            position: int
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Absolute pump position is only for SPM and LSPOne")
        self.send(self.prepareCommand('AbsolutePumpPosition', position))

        if block: self.pullAndWait()
    
    def pump(self, position : int, block : bool = True):
        self.pumpAbsolutePosition(position, block = block)

    def pumpVolume(self, volume : int, syringeVolume: int = syringeSize, block : bool = True) -> None:
        if syringeVolume != self.syringeSize and syringeVolume is not None:
            self.syringeSize = syringeVolume
        if self.syringeSize == None: raise ValueError("Syringe volume must be specified")
        if self.microstepResolution == None: self.getMicrostepResolution()
        if self.microstepResolution == 0:
            to_pump = int(volume * 3000 / self.syringeSize)
        else:
            to_pump = int(volume * 24000 / self.syringeSize)
        return self.pumpAbsolutePosition(to_pump, block = block)

    def pumpRelativePickup(self, position : int, block : bool = True) -> None:
        """
        INPUTS:
            position: int
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Relative pump pickup is only for SPM and LSPOne")
        self.send(self.prepareCommand('RelativePumpPickup', position))

        if block: self.pullAndWait()

    def pumpPickup(self, position : int, block : bool = True):
        self.pumpRelativePickup(position, block = block)

    def pumpPickupVolume(self, volume : int, syringeVolume: int = syringeSize, block : bool = True) -> None:
        if syringeVolume != self.syringeSize and syringeVolume is not None:
            self.syringeSize = syringeVolume
        if self.syringeSize == None: raise ValueError("Syringe volume must be specified")
        if self.microstepResolution == None: self.getMicrostepResolution()
        if self.microstepResolution == 0:
            to_pickup = int(volume * 3000 / self.syringeSize)
        else:
            to_pickup = int(volume * 24000 / self.syringeSize)
        return self.pumpRelativePickup(to_pickup, block = block)

    def pumpRelativeDispense(self, position : int, block : bool = True) -> None:
        """
        INPUTS:
            position: int
        OUTPUTS:
            None
        """
        if self.typeProduct != "SPM":
            raise ValueError("Relative pump dispense is only for SPM and LSPOne")
        self.send(self.prepareCommand('RelativePumpDispense', position))
        if block: self.pullAndWait()

    def pumpDispense(self, position : int, block : bool = True):
        self.pumpRelativeDispense(position, block = block)

    def pumpDispenseVolume(self, volume : int, syringeVolume: int = syringeSize, block : bool = True) -> None:
        if syringeVolume != self.syringeSize and syringeVolume is not None:
            self.syringeSize = syringeVolume
        if self.syringeSize == None: raise ValueError("Syringe volume must be specified")
        if self.microstepResolution == None: self.getMicrostepResolution()
        if self.microstepResolution == 0:
            to_dispense = int(volume * 3000 / self.syringeSize)
        else:
            to_dispense = int(volume * 24000 / self.syringeSize)
        return self.pumpRelativeDispense(to_dispense, block = block)
    
class util:
    def getProductList(specified_type = None) -> list:
        """
        INPUTS:
            specified_type: str # Type of product to find. "SPM" or "RVMFS" or "RVMLP"
        OUTPUTS:
            list # List of product found (list of Device type object)
        """
        result = []
        if os.name == 'nt': #si windows
            devicelist = ftd2xx.listDevices()
            if devicelist is None:
                return result
            for device in devicelist:
                sn = device.decode()
                if "P100" in sn or "P200" in sn or "P201" in sn or "P101" in sn:
                    product = AMF(sn)
                    dev = Device()
                    dev.serialnumber = product.serialNumber
                    dev.comPort = product.serialPort
                    dev.deviceType = product.typeProduct
                    product.disconnect()
                    if dev.deviceType == specified_type or specified_type is None:
                        result.append(dev)
        elif os.name == 'posix': #si linux
            try :
                list_com_port = serial.tools.list_ports.comports()
            except:
                return result
            if list_com_port is None:
                return result
            for com in list_com_port:
                if "P100" in com.serial_number or "P200" in com.serial_number or "P201" in com.serial_number:
                    product = AMF(com.serial_number)
                    dev = Device()
                    dev.serialnumber = product.serialNumber
                    dev.comPort = product.serialPort
                    dev.deviceType = product.typeProduct
                    product.disconnect()
                    result.append(dev)
        else : #si mac
            try :
                list_com_port = serial.tools.list_ports.comports()
            except:
                return result
            if list_com_port is None:
                return result
            for com in list_com_port:
                if "P100" in com.serial_number or "P200" in com.serial_number or "P201" in com.serial_number:
                    product = AMF(com.serial_number)
                    dev = Device()
                    dev.serialnumber = product.serialNumber
                    dev.comPort = product.serialPort
                    dev.deviceType = product.typeProduct
                    product.disconnect()
                    result.append(dev)
        return result
    

    

if __name__ == "__main__":
    # TEST des methodes de la classe AMF

    list_product = util.getProductList()
    for product in list_product:
        print(product)
    
    product = AMF(list_product[0])
    print(product.getFirmwareVersion())