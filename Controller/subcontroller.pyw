import paramiko
from tkinter import *
from tkinter import messagebox
import subprocess

#path to vlc for viewing video stream
#placed at the start of the file for convenience
vlc_path = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"

#issues a command to move servos up
def Up():
    try:
        #enters 1 for the servocontroller
        #which in its code translates to up
        stdin_servo.write('1\n')
        stdin_servo.flush()
        
    except:
        messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")

#issues a command to move servos down
def Down():
    try:
        #enters 2 for the servocontroller
        #which in its code translates to down
        stdin_servo.write('2\n')
        stdin_servo.flush()
        
    except:
        messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")


#issues a command to re-adjust servos at default level
def Straight():
    try:
        #enters 1 for the servocontroller
        #which in its code translates to up
        stdin_servo.write('0\n')
        stdin_servo.flush()

    except:
        messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")


#function to properly close the sensor reading window
def CloseTemp(window):
    updatetemp.set(False)
    tempbutton.config(state = 'normal')
    window.destroy()

#function to open sensor reading window and initiate the reading of values
def Check_Temperature():

    #disable the button and set the update temp flag to True
    tempbutton.config(state = 'disabled')
    updatetemp.set(True)

    #Create a new window to visualise temperature and humidity in sub
    tempwin = Toplevel()
    tempwin.title("Sensor Reading")
    tempwin.iconbitmap("images/temp.ico")
    tempwin.resizable(0,0)

    #When the window is closed, CloseTemp will be called to re-enable the button
    tempwin.protocol("WM_DELETE_WINDOW", lambda: CloseTemp(tempwin))

    #call the functio to update temp_reading and humidity_reading with current and future values
    Update_Temperature()

    #labels to display temp and humidity in
    Temp_Label = Label(tempwin, textvariable = temp_reading, font = ("Times New Roman", 22))
    Temp_Label.grid(row = 0)
    Humidity_Label = Label(tempwin, textvariable = humidity_reading, font = ("Times New Roman", 22))
    Humidity_Label.grid(row = 1)

#Function that updates temperature and humidity, places them in temp_reading and humidity_reading
#as long as the update temp flag is 1 it will keep updating and calling itself to update 10s later
def Update_Temperature():
    
    if(updatetemp.get() == 1):
        #executes the temp.py on the raspberry
        #inputs can be put in stdin
        #outputs from the code are in stdout
        #and errors are in stderr
        try:
            stdin, stdout, stderr = ssh.exec_command("sudo python temp.py")
            
            #processes the output and places it in a neat way in temp_reading and humidity_reading
            readoutput = stdout.readlines()
            temp_reading.set("Temperature:\t" + readoutput[0][:-1] + "°C")
            humidity_reading.set("Humidity:\t" + readoutput[1][:-1] + "%")
           
        except:
            messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")
            
        #after 10s, the function calls itself again to update values if possible
        window.after(10000, Update_Temperature)


#function that checks every 1s if vlc has closed or not
#once it closes the video button is re-enabled
def CheckVideoStatus(vlc):
    #vlc.poll is None as long as the application is still open
    if(vlc.poll() is None):
        #check after 1s if it is still open
        window.after(1000, lambda:CheckVideoStatus(vlc))
    else:
        #vlc is now closed, the user can use the button to open it again
        videobutton.config(state='normal')

#orders the pi to start streaming, it then opens VLC media player to view the stream
def Start_Video():
    try:
        #orders the pi to start streaming
        ssh.exec_command("sudo python camtest.py")
        try:
            #opens vlc with the video streram's IP and port
            vlc = subprocess.Popen([vlc_path, "tcp/mjpeg://192.168.0.1:8000"])
            #disables pressing the video button
            videobutton.config(state='disabled')
            #after 1s calls the function CheckVideoStatus to see if VLC is still open
            window.after(1000, lambda: CheckVideoStatus(vlc))
        except:
            #if vlc could not be opened shows error
            messagebox.showerror("Error", "VLC could not be opened.\nMake sure VLC is installed and its path is as specified.")
    except:
        #in case streaming could not be initiated
        messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")

#function to start or stop the sub's motor
#based on its current status (which is shown by the flag engine_on)
def Start_Stop_Engine():
    if(engine_on.get()):
        #engine was on, send command to stop and update icon and flag
        try: 
            ssh.exec_command("sudo python stopmotor.py")
            engine_on.set(False)
            enginebutton.configure(image = engine_start_img)
        except:
            messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")
    else:
        #engine was off, send command to start and update icon and flag
        try:
            ssh.exec_command("sudo python startmotor.py")
            engine_on.set(True)
            enginebutton.configure(image = engine_stop_img)
        except:
            messagebox.showerror("Error", "Unable to communicate with the pi.\nPlease check your connection.")

#function that is called when main window is closed to stop the motor in any case before closing
def CloseWindow():
    try:
        #sends the command to stop the fan
        #if it's already stopped will do nothing
        ssh.exec_command("sudo python stopmotor.py")

        #enters a strange number for the servocontroller
        #which in its code translates to return to normal and then quit loop and close after a few seconds
        stdin_servo.write('4\n')
        stdin_servo.flush()
        
    except:
        messagebox.showerror("Error", "Could not properly close connection!")

    #it will then close the window
    window.destroy()


#setup SSH connection with the Pi for use later
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    #connect to the pi's address, to user pi which has the password raspberry
    ssh.connect('192.168.0.1', username='pi', password='raspberry')
except:
    #in case connection fails
    messagebox.showerror("Error", "Unable to connect to the pi.\nMake sure you are on 'raspi' wifi.")
    exit()

#setting up main window title, frame, and icon    
window = Tk()
window.title("RC Sub Controller")
window.resizable(0,0)
window.iconbitmap("images/light.ico")

#start the servo controller on the pi for later use
#and bind stdin_servo, stdout_servo, and stderr_servo to the channel
#of the servocontroller to be able to control it
stdin_servo, stdout_servo, stderr_servo = ssh.exec_command("sudo python servocontroller.py")


#image variables for each button
up_img = PhotoImage(file = "images/up.gif")
down_img = PhotoImage(file = "images/down.gif")
straight_img = PhotoImage(file = "images/straight.gif")
video_img = PhotoImage(file = "images/video.gif")
temp_img = PhotoImage(file = "images/temp.gif")
engine_start_img = PhotoImage(file = "images/start.gif")
engine_stop_img = PhotoImage(file = "images/stop.gif")

#declaring and initialising variables for the GUI
#indicates if engine is on
engine_on = BooleanVar()

#indicates if temperature should be updated regularly
updatetemp = BooleanVar()

#will contain the temperature reading from the pi
temp_reading = StringVar()

#will contain the humidity reading from the pi
humidity_reading = StringVar()

#initializes engine to off and temperature update to false
engine_on.set(False)
updatetemp.set(False)    

#When the window is closed, CloseWindow will be called to stop the fan before closing
window.protocol("WM_DELETE_WINDOW", CloseWindow)

#Up Button: setup and display button
upbutton = Button (window, image = up_img, command = Up)
upbutton.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, sticky = NSEW)

#Straight Button: setup and display button
straightbutton = Button(window, image = straight_img, command = Straight)
straightbutton.grid(row = 2, column = 0, columnspan = 2, sticky = NSEW)

#Down Button: setup and display button
downbutton = Button (window, image = down_img, command = Down)
downbutton.grid(row = 3, column = 0, rowspan = 2, columnspan = 2, sticky = NSEW)

#Video Button: setup and display button
videobutton = Button(window, image = video_img, command = Start_Video)
videobutton.grid(row = 0,column = 2, sticky = NSEW)

#Temperature & Humidity: setup and display button
tempbutton = Button(window, image = temp_img, command = Check_Temperature)
tempbutton.grid(row = 1,column = 2, sticky = NSEW)

#Start/Stop Engine Button: setup and display button
enginebutton = Button(window, image = engine_start_img, command = Start_Stop_Engine)
enginebutton.grid(row = 2, column = 2, sticky = NSEW)

#RCSUB Vertical Text (used to fill empty space)
filltxt = Label(window, text = "R\nC\nS\nU\nB", font = ("Helvetica", 22))
filltxt.grid(row = 3, column = 2, rowspan = 2, sticky = NSEW)

#keeps the main window running till closed
window.mainloop()
