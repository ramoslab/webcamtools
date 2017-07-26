### USE WITH PYTHON 2.7 ###
import Tkinter as tk
import paramiko
import subprocess as sub
import socket
import time

# Definitions of functions that start shell scripts
def connect_ssh():
    print("Connecting to the PISA PC")
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect('192.168.137.4',22,'tecnalia','tecnalia')
    return client

def disconnect_ssh(client):
    print "Disconnecting from the PISA PC"
    client.close()

def show_local_video(dev_number):
    print "Showing local video of device", str(dev_number)
    sub.Popen(["vlc", "v4l2:///dev/video" + str(dev_number)])

def list_remote_video():
    stdin, stdout, stderr = client.exec_command('ls /dev/video*')
    nc = 0
    for line in stdout:
        nc += 1
        cam_id = line.strip('\n')[10:]
        print "Camera " + str(cam_id) + " found." 
        tk.Button(root,text="Show camera "+cam_id,command=lambda cid = cam_id : check_remote_video(str(cid))).pack()
    
    if nc < 3:
        print "WARNING: Could only find " + str(nc) + " cameras found. Recording script might fail."

def check_remote_video(dev_number):
    stdin, stdout, stderr = client.exec_command('killall vlc')
    for line in stdout:
        print line
    
    stdin, stdout, stderr = client.exec_command('./WebcamRecording/checkvideo_ssh.sh '+dev_number)
    time.sleep(.5)
    sub.Popen(['/home/tecnalia/video/checkvideo.sh'])

def stop_streaming():
    print "Stopping streaming of video"
    stdin, stdout, stderr = client.exec_command('killall vlc')
    for line in stdout:
        print line
    
#def start_webcam_server():
#    print "Starting up webcam server using default configuration."
#    
#    client = paramiko.SSHClient()
#    client.load_system_host_keys()
#    client.connect('192.168.137.4',22,'tecnalia','tecnalia')
#    stdin, stdout, stderr = client.exec_command('./WebcamRecording/WebcamServer '+str(60000))
#    print "Response from Server:"
    #for line in stdout:
    #    print line

#    client.close()

def manually_start_video_recording():
    print "Starting video recording"
    stop_streaming()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.137.4', 60000))
    s.send('start')
    s.close()
    
def manually_stop_video_recording():
    print "Stopping video recording"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.137.4', 60000))
    s.send('stop')
    s.close()

def test_fct():
    #sub.Popen('test.sh', creationflags = sub.CREATE_NEW_CONSOLE)
    sub.Popen('python /home/tecnalia/tools/startserver.py', shell=True)

# Connect SSH
client = connect_ssh()

# Definition of the graphical user interface

WINDOW_SIZE = "350x300"

root = tk.Tk()
root.wm_title("Camera control system")
root.geometry(WINDOW_SIZE)

tk.Label(root, text="Comupter: IsMore").pack()
tk.Button(root, text="Show position camera of the robot", command=lambda: show_local_video(0)).pack()
tk.Label(root, text="Comupter: Pisa").pack()
list_remote_video()
tk.Button(root, text="End streaming from remote PC", command=stop_streaming).pack()
#tk.Button(root, text="Start WebcamServer", command=start_webcam_server).pack()
tk.Button(root, text="Manually start video recording", command=manually_start_video_recording).pack()
tk.Button(root, text="Manually stop video recording", command=manually_stop_video_recording).pack()
#tk.Button(root, text="Test", command=test_fct).pack()
tk.mainloop()
