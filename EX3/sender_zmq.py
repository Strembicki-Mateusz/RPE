import zmq
import random
from time import sleep
from my_point_pb2 import Pose

context = zmq.Context()
port_publisher = "2000"
socket_publisher = context.socket(zmq.PUB)
socket_publisher.bind(f"tcp://127.0.0.1:{port_publisher}")

pose = Pose()

while True:
	pose.position.x = random.uniform(-5, 5)
	pose.position.y = random.uniform(-5, 5)
	pose.position.z = random.uniform(-5, 5)
	pose.orientation.x = random.uniform(-10, 10)
	pose.orientation.y = random.uniform(-10, 10)
	pose.orientation.z = random.uniform(-10, 10)
	pose.orientation.w = random.uniform(-10, 10)

	# Allow client to connect before sending data
	sleep(2)
	socket_publisher.send(pose.SerializeToString())

