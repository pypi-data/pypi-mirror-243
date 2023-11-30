import paho.mqtt.client as pahomqtt
from time import sleep

class ESPMega:
    mqtt: pahomqtt.Client
    input_chnaged_cb = None
    input_buffer = [0]*16
    humidity_buffer: float = None
    room_temperature_buffer: float = None
    ac_mode_buffer: str = None
    ac_temperature_buffer: int = None
    ac_fan_speed_buffer: str = None
    def __init__(self, base_topic: str, mqtt: pahomqtt.Client, mqtt_callback = None, input_callback = None):
        self.mqtt = mqtt
        self.base_topic = base_topic
        self.mqtt.subscribe(f'{base_topic}/input/#')
        self.mqtt.subscribe(f'{base_topic}/ac/humidity')
        self.mqtt.subscribe(f'{base_topic}/ac/room_temperature')
        self.mqtt.subscribe(f'{base_topic}/ac/mode')
        self.mqtt.subscribe(f'{base_topic}/ac/temperature')
        self.mqtt.subscribe(f'{base_topic}/ac/fan_speed')
        self.mqtt_callback_user = mqtt_callback
        self.mqtt.on_message = self.handle_message
        self.request_state_update()
        sleep(1)
    def digital_read(self, pin: int) -> bool:
        return self.input_buffer[pin]
    def digital_write(self, pin: int, state: bool) -> None:
        self.mqtt.publish(f'{self.base_topic}/pwm/{"%02d"}/set/state'%pin,"on" if state else "off")
        self.mqtt.publish(f'{self.base_topic}/pwm/{"%02d"}/set/value'%pin, 4095 if state else 0)
    def analog_write(self, pin: int, state: bool, value: int):
        self.mqtt.publish(f'{self.base_topic}/pwm/{"%02d"}/set/state'%pin,"on" if state else "off")
        self.mqtt.publish(f'{self.base_topic}/pwm/{"%02d"}/set/value'%pin, int(value))
    def dac_write(self, pin: int, state: bool, value: int):
        self.mqtt.publish(f'{self.base_topic}/dac/{"%02d"}/set/state'%pin,"on" if state else "off")
        self.mqtt.publish(f'{self.base_topic}/dac/{"%02d"}/set/value'%pin, int(value))
    def set_ac_mode(self, mode: str):
        self.mqtt.publish(f'{self.base_topic}/ac/set/mode', mode)
    def set_ac_temperature(self, temperature: int):
        self.mqtt.publish(f'{self.base_topic}/ac/set/temperature', str(temperature))
    def set_ac_fan_speed(self, fan_speed: str):
        self.mqtt.publish(f'{self.base_topic}/ac/set/fan_speed', fan_speed)
    def get_ac_mode(self):
        return self.ac_mode_buffer
    def get_ac_temperature(self):
        return self.ac_temperature_buffer
    def get_ac_fan_speed(self):
        return self.ac_fan_speed_buffer
    def read_room_temperature(self):
        return self.room_temperature_buffer
    def read_humidity(self):
        return self.humidity_buffer
    def send_infrared(self, code: dict):
        self.mqtt.publish(f'{self.base_topic}/ir/send', str(code))
    def request_state_update(self):
        self.mqtt.publish(f'{self.base_topic}/requeststate',"req")
    def handle_message(self, client: pahomqtt.Client, data, message: pahomqtt.MQTTMessage):
        if (message.topic.startswith(self.base_topic+"/input/")):
            id = int(message.topic[len(self.base_topic)+7:len(message.topic)])
            state = int(message.payload)
            if self.input_chnaged_cb != None:
                self.input_chnaged_cb(id, state)
            self.input_buffer[id] = state
        elif (message.topic == (f'{self.base_topic}/ac/humidity')):
            if not message.payload==(b'ERROR'):
                self.humidity_buffer = float(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/room_temperature')):
            if not message.payload==(b'ERROR'):
                self.room_temperature_buffer = float(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/mode')):
            self.ac_mode_buffer = message.payload.decode("utf-8")
        elif (message.topic == (f'{self.base_topic}/ac/temperature')):
            self.ac_temperature_buffer = int(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/fan_speed')):
            self.ac_fan_speed_buffer = message.payload.decode("utf-8")
        if (self.mqtt_callback_user!=None):
            self.mqtt_callback_user(client, data, message)
    def get_input_buffer(self):
        return self.input_buffer
class ESPMega_standalone(ESPMega):
    def __init__(self, base_topic: str, mqtt_server: str, mqtt_port: int, mqtt_use_auth: bool = False,
                  mqtt_username: str = None, mqtt_password: str = None, mqtt_callback = None, 
                  input_callback = None):
        self.mqtt = pahomqtt.Client()
        if(mqtt_use_auth):
            self.mqtt.username_pw_set(mqtt_username, mqtt_password)
        self.mqtt.connect(host=mqtt_server,port=mqtt_port,keepalive=60)
        self.mqtt.loop_start()
        super().__init__(base_topic=base_topic, mqtt=self.mqtt, mqtt_callback=mqtt_callback, input_callback=input_callback)