import tkinter as tk
import serial
import serial.tools.list_ports
import time

# Global variables
time_start = time.time()
minutes=0
seconds=0
ser = None


# Serial communication setup function
def ser_setup():
    ports = serial.tools.list_ports.comports()
    commPort='None'
    numConnection=len(ports)

    for i in range(0, numConnection):
        port=ports[i]
        strPort=str(port)

        if 'Serial' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
    
    return commPort

#Timer function which keeps track of how long it has been since the application was opened
def timer():
    global seconds
    global minutes
    seconds = int(time.time() - time_start) -  minutes * 60
    if seconds >= 60:
        minutes += 1
        seconds = 0
    master.after(1000,timer)
    time_label['text']='Time running:%s minutes %s seconds'%(minutes, seconds)


master = tk.Tk()
master.geometry("600x700")
master.configure(bg='#130013')

# Label where time is displayed
time_label=tk.Label(master,fg='white',bg='#130013',font=(18))
time_label.grid(row=0,column=0)

# Container frame which will be the parent of all additional widgets
container = tk.Frame(master,bg='#130013')
container.place(relx=0.1,rely=0.1,relheight=0.8,relwidth=0.8)

#Below is the frame code,defining the frame sizes and background colors
# The frames will contain all the variable labels and values
speed_frame = tk.Frame(container,bg='#470047')
speed_frame.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.1)

temp_frame = tk.Frame(container,bg='#470047')
temp_frame.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.25)

lights_frame=tk.Frame(container,bg='#470047')
lights_frame.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.4)

notif_frame=tk.Frame(container,bg='#130013')
notif_frame.place(relwidth=1,relheight=0.1)

# Labels and values section
speed_label = tk.Label(speed_frame,fg='white', font=(14),bg='#470047')
speed_label.pack(side='left')

temp_label = tk.Label(temp_frame,fg='white',font=(14),bg='#470047')
temp_label.pack(side='left')

lights_label = tk.Label(lights_frame,fg='white',font=(14),bg='#470047')
lights_label.pack(side='left')

notif_label = tk.Label(notif_frame,fg='white',font=(14),bg='#130013')
notif_label.pack(side='left')

# Serial Setup
connectPort = ser_setup()
ser = serial.Serial(connectPort,9600)
notif_label['text']='No Notifications'


# Timer start
timer()
master.mainloop()
