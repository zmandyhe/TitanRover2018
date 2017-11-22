#Written by Brandon Hawkinson and Timothy Parks
#atlasCore is an interactive shell tool to run, debug and change states of the rover from multiple input sources.

import socket
import time
import sys

version = "0.1.1" 

localCommands = dict([
    ("help", "Lists all of the interactive core commands"),
    ("connect", "Attempts to connect to atlas core"),
    ("restart", "Restarts the active connection to atlas core"),
    ("quit", "quits the atlasCore terminal program")
])

coreCommands = dict([
    ("whichMode","returns which mode the core manager is in(Autonomy, Science, Remote or Manual(Default))"),
    ("setModeAutonomy" , "sets the core's mode to autonomy"),
    ("setModeScience" , "sets the core's mode to science"),
    ("setModeRemote" , "sets the core's mode to Remote"),
    ("setModeManual" , "sets the core's mode to Manual(Default)"),
    ("setModeDefault" , "sets the core's mode to Manual(Default)"),
    ("resetCurrent" , "resets the core, returning to it's current mode on reboot"),
    ("resetCore" , "resets the core, returning it to default"),
    ("getVersion", "gets the core's version number")
])

def Main():
    isConnected = False
    host = "127.0.0.1"
    port = 5000
    count = 0 #counter int to keep track of how many 
    m = "" #message recieved back from the server
    s = socket.socket() #socket object

    print("Welcome to atlasCore version " + version + ", please enter a command...\n")
    while m != "quit":
        if isConnected:
            print("You are connected to the core, you may use core commands\n")

        for key, value in localCommands.items():
            if isConnected and key != "connect":
                print(key + " - " + value)
            elif isConnected == False:
                print(key + " - " + value)

        m = input(" -> ")
        print("")

        if m.lower() == "help": 
            for key, value in coreCommands.items():
                print(key + ' - ' + value)

        elif m == "connect":
            while isConnected == False:        
                try:
                    s.connect((host, port))
                    isConnected = True
                    m = "getVersion"
                    s.send(m.encode())
                    d = s.recv(1024).decode()
                    print("Connection to core established... took " + str(count) + " times\n")
                    count = 0
                    
                    if d == version:
                        print('Versions match: ' + d + "\n")
                    else:
                        print('Version mismatch!\n atlasCore version: ' + version + "\n core version: " + d + "\n Some core commands may not work\n")

                except socket.error:
                    print("Connection not established... " + str(count) + " times")
                    time.sleep(.5)
                    
                    if count % 20 == 0 and count != 0:
                        print("Failed to connect to core... try again? (y -> yes)")
                        m = input(" -> ")
                        if m != "y":
                            break
                            print("exiting...")

                    count += 1
                
        elif m == "restart":
            if isConnected:
                s.close()
                isConnected = False
                print("Restarting the connection...")
            else:
                print("No connection to restart!")
        elif m == "quit":
            if isConnected:
                s.close()
            break
        elif m in coreCommands:
            if isConnected:
                s.send(m.encode())
                d = s.recv(1024).decode()

                print('Command executed: ' + d + "\n")
            else:
                print("Valid command but no connection established, please use \"connect\" command first...")
        else:
            print('Invalid input, type "Help" for a list of commands')
           

if __name__ == '__main__':
    Main()