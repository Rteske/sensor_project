import serial
import matplotlib.pyplot as plt
from threading import Thread
from queue import Queue
import time
import datetime
import os
import csv
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter, find_peaks
import re
import math

class Sensor:
    def __init__(self):
        self.data_queue = Queue(0)

        self.establish_peak_line()
        # Switch this back for Mac
        # Open serial port

        port = "COM3"

        # This is how many data points are on your plot at one time
        self.plot_update_rate = 0.001

        dt = datetime.datetime.now()
        date_string = dt.strftime("%d_%m_%Y_%H_%M_%S")
        dir_name = os.getcwd()
        self.data_counter = 0
        self.current_selected = [0,0]
        self.data_filepath = dir_name + "/data" + f"\\{date_string}" + ".csv"

        self.ser = serial.Serial(port, 115200)

    def read_data(self):
        start_data = self.ser.read_until(b"Processed data:").decode().strip()
        data = " ".join(start_data.split())
        data = data.split(" ")

        return data
    
    def process_frame(self, data):
        start = 0.0025
        step = .005
        x = []
        y = []

        for iq_point in data:
            try:
                real, imaginary = iq_point.split("+")
                imaginary = imaginary[:-1]
                y_coord = math.sqrt((float(real) ** 2) + (float(imaginary) ** 2))
                x_coord = start + ((len(x) - 1)  * step)
                x.append(x_coord)
                y.append(y_coord)
            except:
                print("rr")

        return x, y
            
    # Initialize Plot
    def init_plot(self, x, y, peaks, main, selected):
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

    # Thread to read data from serial port
    def read_thread(self):
        while True:
            read_data = self.ser.read_all().decode('utf-8').strip()
            if (read_data != ''):
                self.data_queue.put(read_data)

        print("Serial port closed")

    def write2file(self, array):
        with open(self.data_filepath, 'a', encoding="utf-8", newline='') as ff:
            writer = csv.writer(ff)
            writer.writerow(array)

            ff.close()

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

    def savgol_smoothing(self, x, y, window_length=11, polyorder=2):
        x = np.array(x)
        y = np.array(y)

        # Sort the data and remove duplicates (if necessary)
        indices = np.argsort(x)
        x_sorted, y_sorted = x[indices], y[indices]
        unique_x, indices = np.unique(x_sorted, return_index=True)
        y_unique = y_sorted[indices]
        
        # Smoothing the data using Savitzky-Golay filter
        y_smooth = savgol_filter(y_unique, window_length=window_length, polyorder=polyorder)

        return unique_x, y_smooth
    
    def limit_detection(self, x, y):
        within_limit = []

        for index, value in enumerate(x):
            if value > self.int1[0] and value < self.int2[0]:
                # Calculate Limit based on slope and y intercept
                limit = (value * self.line_1_slope) + self.line_1_y_intercept
                # Compare Limit to actual value for delta
                limit_delta = y[index] - limit
                # If greater than 0 we know that our lines are in the positive,positive quadrant therefore exceeding 0 means that it is a peak
                if limit_delta > 0:
                    within_limit.append(index)
            # set limits to 250mm to 2.2m for Line2
            elif value > self.int2[0] and value < self.int3[0]:
                # Calculate Limit based on slope and y intercept
                limit = (value * self.line_2_slope) + self.line_2_y_intercept
                # Compare Limit to actual value for delta
                limit_delta = y[index] - limit
                # If greater than 0 we know that our lines are in the positive,positive quadrant therefore exceeding 0 means that it is a peak
                if limit_delta > 0:
                    within_limit.append(index)

        return within_limit
    
    def find_threshold_peaks(self, x, y):
        # For loop only iterating through x values and providing an index to match call out y values
        # X values that are within limit
        x_ = np.array(x)
        y_ = np.array(y)
        selected = [0,0]

        within_limit = self.limit_detection(x_, y_)

        if len(within_limit) > 0:
            y_peaks = y_[within_limit]
            x_peaks = x_[within_limit]

            peaks = []
            for index, x_value in enumerate(x_peaks):
                peaks.append([x_value, y_peaks[index]])

            max_peak_y = np.max(y_peaks)
            max_peak_x = x_peaks[np.argmax(max_peak_y)]
            max_coords = [max_peak_x, max_peak_y]

            first_threshold_x = np.min(x_peaks)
            first_threshold_y = y_peaks[np.argmin(first_threshold_x)]

            first_below_threshold_x = first_threshold_x - 0.005
            first_below_threshold_y = 0

            for index, value in enumerate(x_):
                if value == first_below_threshold_x:
                    first_below_threshold_y = y_[index]

            l1 = self.general_form_line([first_below_threshold_x, first_below_threshold_y], [first_threshold_x, first_threshold_y])

            if first_threshold_x > self.int1[0] and first_threshold_x < self.int2[0]:
                l2 = self.general_form_line(self.int1, self.int2)
            elif first_threshold_x > self.int2[0] and first_threshold_x < self.int3[0]:
                l2 = self.general_form_line(self.int2, self.int3)

            threshold_cross = self.intersection_cramers_rule(l1, l2)

            # Jims Equation
            selected = ((first_threshold_y - threshold_cross[0]) / (first_threshold_y - first_below_threshold_y)) * (first_threshold_x - first_below_threshold_x) + first_below_threshold_x
            selected = [selected, 0]

            return peaks, max_coords, selected
        else:

            return [], [0,0], [0,0]

    def general_form_line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0] * p2[1] - p2[0] * p1[1])

        return A, B, -C

    def intersection_cramers_rule(self, L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]

        if D != 0:
            x = Dx / D
            y = Dy / D
            return x, 
        else:
            return False

    # Main function
    def main(self):
        # Setting local variables for assignment
        peaks=[]

        # Infinite Loop
        while True:
            data_string = self.read_data()
            x, y = self.process_frame(data_string)
            if len(x) == 400:
                peaks, main, selected = self.find_threshold_peaks(x, y)
                self.write2file(selected)
                self.init_plot(x, y, peaks, main, selected)
                print("FULL FRAME")


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