import serial

ser = serial.Serial('COM6', 9600)
led = ser.readline().decode()
if led:
    print(led)
