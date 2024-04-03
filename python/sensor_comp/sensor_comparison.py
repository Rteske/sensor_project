import threading
import datetime
from python.sensor_comp.sensor import Sensor
from python.sensor_comp.linear_encoder import LinearEncoder
from threading import Thread
import os
import time
import csv
import matplotlib.pyplot as plt
import sys

class SensorComparison:
    def __init__(self):
        self.session_name = ''
        self.session_start = datetime.datetime.now()
        
        dt = datetime.datetime.now()
        date_string = dt.strftime("%d_%m_%Y_%H_%M_%S")
        dir_name = os.getcwd()
        self.data_filepath = dir_name + "\\data" + f"\\{date_string}" + ".csv"

        self.plot_update_rate = 0.001

        self.establish_peak_line()

        res = input("Run w plot?: Y or N >")
        if res == "Y":
            self.plot_run = True
        else:
            self.plot_run = False

        self.write2file(["distance", "linear_encoder_position", "measurement_delta", "linear_encoder_timestamp", 'distance_timestamp', "measurement_time_delta"])

        self.init_instruments()

    def establish_peak_line(self):
        # Calculate Slope and y intercepts
        # Establish peak lines 
        self.int1 = [.065, 8000.0]
        self.int2 = [.20, 800.0]
        self.int3 = [2.200, 75.0]
        self.line_1_slope = self.int2[1] - self.int1[1] / self.int2[0] - self.int1[0]
        self.line_2_slope = self.int3[1] - self.int2[1] / self.int3[0] - self.int2[0]
        self.line_1_y_intercept = ((self.line_1_slope * self.int1[0]) - self.int1[1]) * -1
        self.line_2_y_intercept = ((self.line_2_slope * self.int2[0]) - self.int2[1]) * -1

    def init_plot(self, x, y, selected, linear_encoder_pos):
        plt.xlabel('Distance (m)')
        plt.ylabel('Amplitude')
        plt.title('Distance vs Amplitude')
        # set axis limits
        plt.xlim(0, 2.4)
        plt.ylim(0, 4000)

        # plt.axvline(main[0], color="r")
        plt.axvline(selected[0], color="r")
        plt.plot(x, y)
        plt.plot([self.int1[0], self.int2[0], self.int3[0]], [self.int1[1], self.int2[1], self.int3[1]], linestyle="solid")
        # plt.scatter(x, y)
        plt.draw()
        plt.pause(self.plot_update_rate)
        plt.clf()

    def get_data(self):

        distance, distances, distance_timestamp = self.sensor.get_current_distance()

        if distance:
            linear_encoder_position, linear_encoder_timestamp = self.linear_encoder.get_position()

            measurement_time_delta = abs(distance_timestamp - linear_encoder_timestamp)
            measurement_delta = abs(linear_encoder_position - distance[0])

            print(f"Delta: {measurement_delta}, Linear Encoder Position in Meters: {linear_encoder_position}, Distance in Meters: {distance}, Measurement Time Delta: {measurement_time_delta}")

            self.write2file([distance[0], linear_encoder_position, measurement_delta, linear_encoder_timestamp, distance_timestamp, measurement_time_delta])

            if self.plot_run:
                self.init_plot(distances[0], distances[1], distance, linear_encoder_position)

    def write2file(self, array):
        with open(self.data_filepath, 'a', encoding="utf-8", newline='') as ff:
            writer = csv.writer(ff)
            writer.writerow(array)

            ff.close()

    def init_instruments(self):
        self.sensor = Sensor()
        self.linear_encoder = LinearEncoder()

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,**self._kwargs)
            
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

if __name__ == "__main__":
    app = SensorComparison()
    try:
        while True:
            app.get_data()
    except KeyboardInterrupt:
        print("ALL DONE")
        sys.exit()
        