import picamera
import time
import socket

#for easier typing, replaces the full name by 'camera'
with picamera.PiCamera() as camera:
    
    #setting up camera options
    camera.resolution = (720, 480)
    camera.framerate=24

    #preparing for network connection
    server_socket = socket.socket()

    #the stream is at the pi's IP adress port 8000
    try:
	server_socket.bind(('0.0.0.0', 8000))
    except:
	print("Port is already in use... quitting.")
	exit()

    #listens on the port and waits for someone to attempt connecting	
    server_socket.listen(0)

    #the code accepts only one connection and makes a temp file
    connection=server_socket.accept()[0].makefile('wb')
    
    #once a connection is established start streaming for 10mins
    #the stream can be stopped earlier by interrupting
    #which VLC will do when closing its connection
    try:
        camera.start_recording(connection, format='mjpeg')
	camera.wait_recording(6000)
    #if an exception occurs or once streaming is done
    #close connection
    finally:
	camera.stop_recording()
        connection.close()
        server_socket.close()
