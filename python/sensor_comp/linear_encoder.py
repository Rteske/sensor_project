import serial
import time

class LinearEncoder:
    def __init__(self):
        port = "COM12"

        self.ser = serial.Serial(port, 115200)

    def read_data(self):
        try:
            self.ser.reset_input_buffer()
            data_string = self.ser.readline().decode('utf-8').strip()
            print(data_string)
            return data_string
        except:
            print("failure")

    def get_position(self):
        data = self.read_data()
        if data != '':
            return int(data) / 1e+6, time.time()
        else:
            return 0, time.time()