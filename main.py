from machine import Pin, PWM
from time import sleep
import sys
import socket
import network


wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.config(essid="ESP-WIFI")

host = '192.168.4.1'
port = 9900

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5)


# CONSTANTS
KEY_UP = const(0)
KEY_DOWN = const(1)

keys = [['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

# These are the notes with equivalent frequency
# https://www.blackghostaudio.com/blog/basic-music-theory-for-beginners
B0  = 31; C1  = 33; CS1 = 35; D1  = 37
DS1 = 39; E1  = 41; F1  = 44; FS1 = 46
G1  = 49; GS1 = 52; A1  = 55; AS1 = 58
B1  = 62; C2  = 65; CS2 = 69; D2  = 73
DS2 = 78; E2  = 82; F2  = 87; FS2 = 93
G2  = 98; GS2 = 104; A2  = 110; AS2 = 117
B2  = 123; C3  = 131; CS3 = 139; D3  = 147
DS3 = 156; E3  = 165; F3  = 175; FS3 = 185
G3  = 196; GS3 = 208; A3  = 220; AS3 = 233
B3  = 247; C4  = 262; CS4 = 277; D4  = 294
DS4 = 311; E4  = 330; F4  = 349; FS4 = 370
G4  = 392; GS4 = 415; A4  = 440; AS4 = 466
B4  = 494; C5  = 523; CS5 = 554; D5  = 587
DS5 = 622; E5  = 659; F5  = 698; FS5 = 740
G5  = 784; GS5 = 831; A5  = 880; AS5 = 932
B5  = 988; C6  = 1047; CS6 = 1109; D6  = 1175
DS6 = 1245; E6  = 1319; F6  = 1397; FS6 = 1480
G6  = 1568; GS6 = 1661; A6  = 1760; AS6 = 1865
B6  = 1976; C7  = 2093; CS7 = 2217; D7  = 2349
DS7 = 2489; E7  = 2637; F7  = 2794; FS7 = 2960
G7  = 3136; GS7 = 3322; A7  = 3520; AS7 = 3729
B7  = 3951; C8  = 4186; CS8 = 4435; D8  = 4699
DS8 = 4978

notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'C']
tones = [1915, 1700, 1519, 1432, 1275, 1136, 1014, 956]

# pins of keyboard
rows = [2, 4, 5, 18]
cols = [19, 16, 15, 17]

# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

# set pin for buzzer
p23 = Pin(23, Pin.OUT)
buzzer = PWM(p23)
buzzer.duty(0)


def send_message(mes):
    client.send(mes.encode('utf-8'))


def init():
    for row in range(0,4):
        for col in range(0,4):
            row_pins[row].off()


def scan(row, col):

    # set the current column to high
    row_pins[row].on()
    key = None

    # check for keypressed events
    if col_pins[col].value() == KEY_DOWN:
        key = KEY_DOWN
    if col_pins[col].value() == KEY_UP:
        key = KEY_UP
    row_pins[row].off()

    # return the key state
    return key

# Function for playing sound
def play(pin, melodies, delays, duty):

    pwm = PWM(pin)
    for note in melodies:
        if note != 0:
            pwm.freq(note)
        pwm.duty(duty)
        sleep(delays)
    pwm.duty(0)
    pwm.deinit()

# function for setting melody for symbols
def set_melody(sym):
    if sym == 'A':
        return [
            E7, E7, 0, E7, 0, C7, E7, 0,
            G7, 0, 0, 0, G6, 0, 0, 0,
            C7, 0, 0, G6, 0, 0, E6, 0,
            0, A6, 0, B6, 0, AS6, A6, 0,
            G6, E7, 0, G7, A7, 0, F7, G7,
            0, E7, 0, C7, D7, B6, 0, 0,
            C7, 0, 0, G6, 0, 0, E6, 0,
            0, A6, 0, B6, 0, AS6, A6, 0,
            G6, E7, 0, G7, A7, 0, F7, G7,
            0, E7, 0, C7, D7, B6, 0, 0,
            ]
    if sym == 'B':
        return [
            E7, E7, E7, 0,
            E7, E7, E7, 0,
            E7, G7, C7, D7, E7, 0,
            F7, F7, F7, F7, F7, E7, E7, E7, E7, D7, D7, E7, D7, 0, G7, 0,
            E7, E7, E7, 0,
            E7, E7, E7, 0,
            E7, G7, C7, D7, E7, 0,
            F7, F7, F7, F7, F7, E7, E7, E7, G7, G7, F7, D7, C7, 0
        ]
    if sym == 'C':
        return [
            C6, C6, G6, G6, A6, A6, G6, 0,
            F6, F6, E6, E6, D6, D6, C6, 0,
            G6, G6, F6, F6, E6, E6, D6, 0,
            G6, G6, F6, F6, E6, E6, D6, 0,
            C6, C6, G6, G6, A6, A6, G6, 0,
            F6, F6, E6, E6, D6, D6, C6, 0,
            ]
    if sym == 'D':
        return [
                1915, 0, 1700, 0,
                1519, 0, 1432, 0,
                1275, 0, 1136, 0,
                1014, 0, 956, 0
                ]


print("Welcome to our Wonderful Piano!")
client, address = sock.accept()
print("You can start to play!")
print(f"Client with address {address} is waiting for you!")

# set all the columns to low
init()

# main
try:
    while True:
        for row in range(4):
            for col in range(4):
                key = scan(row, col)
                if key == KEY_DOWN:
                    cur_key = keys[row][col]
                    if cur_key == "0":
                        send_message("Close session")
                        client.close()
                        sys.exit()
                    elif cur_key in "12345678":
                        buzzer.freq(tones[int(cur_key) - 1])
                        buzzer.duty(50)
                        sleep(0.5)
                        buzzer.duty(0)
                        send_message(f"Key: {notes[int(cur_key) - 1]}")
                        print(f"Key: {notes[int(cur_key) - 1]}")
                    elif cur_key in "ABCD":
                        send_message(f"Song {cur_key} is playing. Enjoy)")
                        print(f"Song {cur_key} is playing. Enjoy)")
                        play(p23, set_melody(cur_key), 0.15, 50)

except KeyboardInterrupt:
    print('Interrupted by user...')
except Exception as e:
    print(e)
finally:
    print("Closing socket...")
    sock.close()
    print("See you again!")
