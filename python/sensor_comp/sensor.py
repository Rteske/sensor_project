import serial
import numpy as np
import math
import time

class Sensor:
    def __init__(self):
        self.establish_peak_line()
        port = "COM3"
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

            return selected
        else:
            return [0,0]

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
            return x,y
        else:
            return False

    def get_current_distance(self, plot_run=True):
        data_string = self.read_data()
        x, y = self.process_frame(data_string)
        if len(x) == 400:
            package_recieved_time = time.time()
            selected = self.find_threshold_peaks(x, y)

            return selected, [x, y], package_recieved_time
        else:
            return False, False, False