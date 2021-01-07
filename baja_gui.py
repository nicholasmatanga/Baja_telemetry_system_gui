import tkinter as tk
import serial
import time

time_start = time.time()

minutes=0
seconds=0

def timer():
    global seconds
    global minutes
    seconds = int(time.time() - time_start) -  minutes * 60
    if seconds >= 60:
        minutes += 1
        seconds = 0
    master.after(1000,timer)
    label['text']='Time running:%s minutes %s seconds'%(minutes, seconds)


master = tk.Tk()
master.geometry("500x500")
master.configure(bg='#00030D')

label=tk.Label(master,fg='white',bg='black',font=(18))
label.grid(row=0,column=1)

timer()
master.mainloop()
