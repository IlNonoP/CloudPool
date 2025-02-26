import sys
import os

command = str(sys.argv[1:2])
try:
    second_command = str(sys.argv[2:3])
except:
    pass    
command = command.replace("['", "").replace("']", "")

if command == "start":
    print("Starting....")
    os.system("python3 main.py")
elif command == "config":
    os.system("rclone --config rclone-nodes.conf config")
elif "change-dir" == command:
    try:
        folder=str(second_command).replace("['", "").replace("']", "")
        linee = ""
        with open("/opt/cloudpool/config.conf", "r") as file:
            for ln in file:
                if "user_folder=" in ln:
                    linee = linee + "user_folder="+folder
                else:
                    linee = linee + ln
        with open("/opt/cloudpool/config.conf", "w") as file:
            file.write(linee)
        print("Direcory change to: "+str(folder))
    except:
        print("Error: Error during the directory change")
    
   
    



elif command == "help":
    print("Welcome to Cloud Pool!")
    print("")
    print("cloudpool -")
    print("          |- start          start the program")
    print("          |- config         enter to Rclone setup for add or remove Nodes")
    print("          |- change-dir     change the folder of file")


else:
    print("Unknow command. Write help to see a guide")
