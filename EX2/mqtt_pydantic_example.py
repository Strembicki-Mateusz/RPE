import random
import time
import paho.mqtt.client as mqtt
from pydantic import BaseModel
from typing import List

# Pydantic model for temperature data
class TemperatureData(BaseModel):
    sensor_name: str
    temperature: float

class TemperatureSensor:
    def __init__(self, sensor_name: str, mqtt_broker: str, mqtt_topic: str):
        self.sensor_name = sensor_name
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.client = mqtt.Client()
        self.client.connect(mqtt_broker)
        self.client.loop_start()

    def publish_random_temperature(self):
        temperature = random.uniform(0, 30)
        data = TemperatureData(sensor_name=self.sensor_name, temperature=temperature)
        self.client.publish(self.mqtt_topic, data.json())

# Pydantic model for humidity data
class HumidityData(BaseModel):
    sensor_name: str
    humidity: float

class HumiditySensor:
    def __init__(self, sensor_name: str, mqtt_broker: str, mqtt_topic: str):
        self.sensor_name = sensor_name
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.client = mqtt.Client()
        self.client.connect(mqtt_broker)
        self.client.loop_start()

    def publish_random_humidity(self):
        humidity = random.uniform(20, 100)
        data = HumidityData(sensor_name=self.sensor_name, humidity=humidity)
        self.client.publish(self.mqtt_topic, data.json())


class MonitoringUnit:
    def __init__(self, mqtt_broker: str, mqtt_topic: str):
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(mqtt_broker)
        self.client.subscribe(f"{mqtt_topic}/+") # + - single level wildcard
        self.client.loop_start()

    def on_message(self, client, userdata, message):
        payload = message.payload.decode('utf-8')
        #print(message.topic)
        try:
            if message.topic == "/sensors/t1" or message.topic == "/sensors/t2":
                data = TemperatureData.parse_raw(payload) 
                print(f"Received data from {data.sensor_name}: Temperature = {data.temperature}")
            elif message.topic == "/sensors/h1" or message.topic == "/sensors/h2":
                data = HumidityData.parse_raw(payload)
                print(f"Received data from {data.sensor_name}: Humididy = {data.humidity}")
        except Exception as e:
            print(f"Failed to validate message: {str(e)}")

if __name__ == "__main__":
    # Start a monitoring unit that subscribes to all subtopics published on "sensors"
    monitoring_unit = MonitoringUnit(mqtt_broker="localhost", mqtt_topic="/sensors")
    # Start a temperature sensor that publishes to "/sensors/t1"
    h1_sensor = HumiditySensor(sensor_name="h1", mqtt_broker="localhost", mqtt_topic="/sensors/h1")
    t1_sensor = TemperatureSensor(sensor_name="t1", mqtt_broker="localhost", mqtt_topic="/sensors/t1")
    h2_sensor = HumiditySensor(sensor_name="h2", mqtt_broker="localhost", mqtt_topic="/sensors/h2")
    t2_sensor = TemperatureSensor(sensor_name="t2", mqtt_broker="localhost", mqtt_topic="/sensors/t2")
    
    while True:
        h1_sensor.publish_random_humidity()
        t1_sensor.publish_random_temperature()
        time.sleep(1)
        h2_sensor.publish_random_humidity()
        t2_sensor.publish_random_temperature()
        time.sleep(1)