import zmq
from time import sleep
from my_point_pb2 import Pose

context = zmq.Context()
port_subscriber = "2000"
socket_subscriber = context.socket(zmq.SUB)
socket_subscriber.connect(f"tcp://127.0.0.1:{port_subscriber}")  # Make sure to use the same address as the sender
socket_subscriber.setsockopt(zmq.SUBSCRIBE, b"")

count = 1

while True:
	serialized_data = socket_subscriber.recv()
	pose = Pose()
	pose.ParseFromString(serialized_data)
	sleep(1)
	print("Received Data")
	#print(f"Position: x={pose.position.x}, y={pose.position.y}, z={pose.position.z}")
	#print(f"Orientation: x={pose.orientation.x}, y={pose.orientation.y}, z={pose.orientation.z}, w={pose.orientation.z}")
	print(f"Received {count}:\n{pose}")
	count += 1
	
