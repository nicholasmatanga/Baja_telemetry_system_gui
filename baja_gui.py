import tkinter as tk
import serial
import serial.tools.list_ports
import time
import nexmo

# Global variables
time_start = time.time()
minutes=0
seconds=0
ser = None
num=None
submit=None
enter_num=None
client = nexmo.Client(key='f7cc0105',secret='KduKWk6cxp7Y7oZx')


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

# Display function which receives data from the arduino, separates it, and displays it
# Also updates the notifications settings
def update_and_display():
    data = ser.readline().decode().strip()
    lit=None
    val = None
    if data:
        result=data
        val=result.split()
    speed_label['text']='Speed:%s km/hr'%(val[0])
    temp_label['text']='Temp:%s degrees'%(val[1])

    if int(val[2]) == 0:
        lit='OFF'
    else:
        lit='ON'
    lights_label['text']='Lights:%s'%(lit)
    # Checking for warnings when values are exceeded
    if int(val[0])>400:
        notif_label['text']='WARNING:Speed over the limit!'
        notif_frame['bg']='#4F3466'
        notif_label['bg']='#4F3466'

    master.after(600,update_and_display)

def setup_entry():
    global enter_num
    global submit
    enter_num=tk.Entry(container,bg='#808080',font=(14))
    enter_num.place(relwidth=0.4,relheight=0.08,relx=0.15,rely=0.75)
    
    submit=tk.Button(container,bg='#808080',font=(14),text='Submit',command=lambda:store_num(enter_num.get()))
    submit.place(relwidth=0.2,relheight=0.08,relx=0.56,rely=0.75)

def store_num(number):
    num=int(number)
    enter_num.destroy()
    submit.destroy()
    return num


master = tk.Tk()
master.geometry("600x700")
master.configure(bg='#130013')

# Label where time is displayed
time_label=tk.Label(master,fg='white',bg='#130013',font=(18))
time_label.grid(row=0,column=0)

# Container frame which will be the parent of all additional widgets
container = tk.Frame(master,bg='#130013')
container.place(relx=0.1,rely=0.1,relheight=0.8,relwidth=0.8)

#Below is the frame and buttons code,defining the frame sizes and background colors
# The frames will contain all the variable labels and values
speed_frame = tk.Frame(container,bg='#800080')
speed_frame.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.1)

temp_frame = tk.Frame(container,bg='#800080')
temp_frame.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.25)

lights_frame=tk.Frame(container,bg='#800080')
lights_frame.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.4)

notif_frame=tk.Frame(container,bg='#130013')
notif_frame.place(relwidth=1,relheight=0.1)

gps_tracking=tk.Button(container,text='GPS',font=(14),bg='#2A192A',fg='white',bd=1)
gps_tracking.place(relwidth=0.3,relheight=0.08,relx=0.35,rely=0.55)

text_msg = tk.Button(container,text='SMS notifications',font=(14),bg='#2A192A',fg='white',bd=1,command=lambda: setup_entry())
text_msg.place(relwidth=0.35,relheight=0.08,relx=0.325,rely=0.65)

# Labels and values section
speed_label = tk.Label(speed_frame,fg='white', font=(14),bg='#800080')
speed_label.pack(side='left')

temp_label = tk.Label(temp_frame,fg='white',font=(14),bg='#800080')
temp_label.pack(side='left')

lights_label = tk.Label(lights_frame,fg='white',font=(14),bg='#800080')
lights_label.pack(side='left')

notif_label = tk.Label(notif_frame,fg='white',font=(14),bg='#130013')
notif_label.pack(side='left')


# Serial Setup
connectPort = ser_setup()
ser = serial.Serial(connectPort,9600)
notif_label['text']='No Notifications'
# Function calls
timer()
update_and_display()
master.mainloop()
