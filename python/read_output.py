import serial
from queue import Queue
import time
import datetime
import os

class Sensor:
    def __init__(self):
        # Switch this back for Mac
        # Open serial port
        # port = '/dev/cu.usbmodem306F345C31331'
        port = "COM12"

        dt = datetime.datetime.now()
        date_string = dt.strftime("%d_%m_%Y_%H_%M_%S")
        dir_name = os.getcwd()

        self.data_filepath = dir_name + "\data" + f"\{date_string}" + ".txt"

        self.ser = serial.Serial(port, 115200)

    def read_data(self):
        try:
            data_string = self.ser.readline().decode('utf-8').strip()
            data = self.parse_data(data_string)
            return data
        except:
            print("failure")

    # Parse data
    def parse_data(self, data):
        # data = data.split(',')
        return data

    # Thread to read data from serial port
    def read_thread(self):
        while True:
            read_data = self.ser.readline().decode('utf-8').strip()
            if (read_data != ''):
                self.data_queue.put(read_data)

        print("Serial port closed")


    def write2file(self, array):
        with open(self.data_filepath, 'a', encoding="utf-8") as ff:
            ff.write(array)
            ff.close()

    # Main function
    def main(self):
        
        # Infinite Loop
        while True:
            # Read data from stream and parse
            data = self.read_data()
            print(data)
            self.write2file(data)

        # Close serial port
        self.ser.close()

if __name__ == '__main__':
    def shutdown():
        sensor.ser.close()
        print("Serial port closed")

    sensor = Sensor()

    # If user presses Ctrl+C, close serial port
    try:
        sensor.main()
    except KeyboardInterrupt:
        shutdown()