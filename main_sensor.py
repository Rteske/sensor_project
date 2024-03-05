import serial
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from threading import Thread
from queue import Queue
import time
import datetime
import os
import csv
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter, find_peaks

class Sensor:
    def __init__(self):
        self.data_queue = Queue(0)

        self.establish_peak_line()
        # Switch this back for Mac
        # Open serial port
        # port = '/dev/cu.usbmodem306F345C31331'
        port = "COM3"

        # This is how many data points are on your plot at one time
        self.num_plot_data = 300
        self.xerror_delta = 0.05
        self.plot_update_rate = 0.001

        dt = datetime.datetime.now()
        date_string = dt.strftime("%d_%m_%Y_%H_%M_%S")
        dir_name = os.getcwd()

        self.data_filepath = dir_name + "\data" + f"\{date_string}" + ".csv"
        self.write2file(["Distance(Meters)","Amplitude"])

        self.ser = serial.Serial(port, 115200)
        print("What type of peak detection would you like to use?")
        print("Enter Num and Hit enter")
        print("1. Basic Limit and Max Peaks")
        print("2. Spline Interpolated Peaks <Works the best>")
        selection = input("> ")
        self.peak_detection_type = int(selection) - 1

    def read_data(self):
        data_string = self.ser.readline().decode('utf-8').strip()
        data = self.parse_data(data_string)
        return data

    # Parse data
    def parse_data(self, data):
        data = data.split(',')
        return data
    
    # Initialize Plot
    def init_plot(self, x, y, peaks, main):
        plt.xlabel('Distance (m)')
        plt.ylabel('Amplitude')
        plt.title('Distance vs Amplitude')
        # set axis limits
        plt.xlim(0, main[0] + 0.5)
        plt.ylim(0, main[1] + 100)
        # if there are no peaks dont bother 
        if len(peaks) > 0:
            # this is if you want to see where all are crossing the limit threshold
            # for peak in peaks:
            plt.axvline(main[0], color="r")

        plt.plot(x, y)
        plt.plot([self.int1[0], self.int2[0], self.int3[0]], [self.int1[1], self.int2[1], self.int3[1]], linestyle="solid")
        # plt.scatter(x, y)
        plt.draw()
        plt.pause(self.plot_update_rate)
        plt.clf()

    # Thread to read data from serial port
    def read_thread(self):
        while True:
            read_data = self.ser.readline().decode('utf-8').strip()
            if (read_data != ''):
                self.data_queue.put(read_data)

        print("Serial port closed")


    def write2file(self, array):
        with open(self.data_filepath, 'a', encoding="utf-8") as ff:
            writer = csv.writer(ff)
            writer.writerow(array)

            ff.close()

    def establish_peak_line(self):
        # Calculate Slope and y intercepts
        # Establish peak lines 
        self.int1 = [.065, 800.0]
        self.int2 = [.20, 200.0]
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

    def find_spline_peaks(self, unique_x, y_smooth):
        # Spline interpolation
        spline = UnivariateSpline(unique_x, y_smooth, s=0.5)
        x_dense = np.linspace(min(unique_x), max(unique_x), 1000)

        # Evaluate the spline on the dense x-values
        y_dense = spline(x_dense)

        # Find peaks in the dense y-values
        peaks, _ = find_peaks(y_dense)

        # If peaks were found, identify the maximum one based on y-value
        if peaks.size > 0:
            max_peak_index = peaks[np.argmax(y_dense[peaks])]
            max_peak_x = x_dense[max_peak_index]
            max_peak_y = y_dense[max_peak_index]

            x_peaks = x_dense[peaks]
            y_peaks = y_dense[peaks]

            within_limit = self.limit_detection(x_peaks, y_peaks)
            x_peaks = x_peaks[within_limit]
            y_peaks = y_peaks[within_limit]

            peaks = []
            for index, x_value in enumerate(x_peaks):
                peaks.append([x_value, y_peaks[index]])

        return peaks, [max_peak_x, max_peak_y]
    
    def find_moving_average_peaks(self, x, y):
        window_size=5
        x = np.array(x)
        y = np.array(y)

        # Calculate the moving average
        moving_avg = np.convolve(y, np.ones(window_size) / window_size, mode='valid')

        # Find peaks on the smoothed data
        peaks_indices = find_peaks(moving_avg)[0]

        # Adjust indices to align peaks with the original data
        adjusted_indices = peaks_indices + (window_size // 2)

        # Ensure indices do not exceed the bounds of the original data
        adjusted_indices = adjusted_indices[adjusted_indices < len(x)]

        # Extract the peak values
        peaks_x = x[adjusted_indices]
        peaks_y = moving_avg[peaks_indices]

        within_limit = self.limit_detection(peaks_x, peaks_y)
        if len(within_limit) > 1:
            peaks_x = peaks_x[within_limit]
            peaks_y = peaks_y[within_limit]

            # Combine the x and y coordinates of the peaks into tuples
            peaks = list(zip(peaks_x, peaks_y))

            # Identify the maximum peak
            if peaks:
                max_peak = max(peaks, key=lambda item: item[1])
            else:
                max_peak = []

            return peaks, max_peak
        else:
            return [], []

    def find_threshold_peaks(self, x, y):
        # For loop only iterating through x values and providing an index to match call out y values
        # X values that are within limit
        x_ = np.array(x)
        y_ = np.array(y)

        within_limit = self.limit_detection(x_, y_)

        if len(within_limit) > 0:
            y_peaks = y_[within_limit]
            x_peaks = x_[within_limit]

            peaks = []
            for index, x_value in enumerate(x_peaks):
                peaks.append([x_value, y_peaks[index]]) 

            max_peak_y = np.max(y_peaks)
            max_peak_x = x_peaks[np.argmax(max_peak_y)]

            return peaks, [max_peak_x, max_peak_y]
        else:
            peaks = []
            main = [0,0]

            return peaks, main
            

    # Main function
    def main(self):

        # Setting local variables for assignment
        peaks=[]
        counter = 0
        x = []
        y = []

        # Initialize Plot
        # self.init_plot(x, y, peaks, main_peak, avg_peak)

        # Infinite Loop
        while True:
            # Read data from stream and parse
            data = self.read_data()
            if (data != ''):
                # if the microprocesser determines a distance then the try loop goes into exception and plots the results
                if counter > self.num_plot_data:
                    if (x != [] and y != []):
                        # sort both x and y according to x
                        x, y = zip(*sorted(zip(x, y)))

                        if self.peak_detection_type == 0:
                            x, y = self.savgol_smoothing(x, y)
                            peaks, main = self.find_threshold_peaks(x, y) 
                        elif self.peak_detection_type == 1:   
                            x, y = self.savgol_smoothing(x, y)
                            peaks, main = self.find_spline_peaks(x, y)

                        for peak in peaks:
                            self.write2file(peak)

                        self.init_plot(x, y, peaks, main)
                        # Reset locals
                        x = []
                        y = []
                    counter = 0
                else:
                    if len(data[0]) < 10:
                        _x = float(data[0])
                        _y = float(data[1])
                        x.append(_x)
                        y.append(_y)
                        counter = counter + 1

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