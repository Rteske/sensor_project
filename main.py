"""

BEGIN:Distance(m),Amplitude

0.120109,31

0.130118,39

0.140127,27

0.150136,23

0.160146,21

...

...

...

3.723384,6

3.783438,14

3.843493,4

3.903548,5

END:Distance(m),Amplitude

1 detected distances: 1.999607 m

BEGIN:Distance(m),Amplitude

...

...

...

"""

# The serial port prints the data in the above foramt continously

# Read data between BEGIN and END and plot it in real time using matplotlib on a line graph



import serial

import matplotlib.pyplot as plt

from threading import Thread

from queue import Queue



# Global variables

x = []

y = []

data_queue = Queue(0)



# Open serial port

# port = '/dev/cu.usbmodem306F345C31331'
port = "COM3"
ser = serial.Serial(port, 115200)



# Read data from serial port

def read_data():

    return ser.readline().decode('utf-8').strip()



# Parse data

def parse_data(data):

    data = data.split(',')

    return data



# Plot data

def plot_data(x, y, p):

    plt.xlabel('Distance (m)')

    plt.ylabel('Amplitude')

    plt.title('Distance vs Amplitude')

    # set axis limits

    plt.xlim(0, 2.4)

    plt.ylim(0, 1000)

    plt.axvline(p,color='r')

    plt.plot(x, y,'-.')

    plt.draw()

    plt.pause(0.001)

    plt.clf()



# Thread to read data from serial port

def read_thread():

    while True:

        read_data = ser.readline().decode('utf-8').strip()

        if(read_data != ''):

            data_queue.put(read_data)



    print("Serial port closed")



"""

def write2file(array):

    filename = '\\downloads\\data.txt'

    fff = open(filename, 'a')

    fff.write(array)

    fff.close()

"""



def write2file(array):

    filename = 'data.txt'

    fff = open(filename, 'a')

    #print(array)

    try:

        fff.write('%s,%s\n'%(array[0],array[1]))

    except:

        fff.write('%s\n' %array)



    fff.close()

# Main function

def main():

    global x, y

    # # Start thread to read data from serial port

    # t1 = Thread(target=read_thread)

    # t1.start()



    # # Read data from queue and plot it

    # while True:

    #     if(not data_queue.empty()):

    #         data = data_queue.get()

    #         print(data)

    peak=0

    while (True):
        data = read_data()
        if (data != ''):

            data = parse_data(data)

            print(data)

            write2file(data)

            try:

                _x = float(data[0])

                _y = float(data[1])

            except:

                if data[0][2:21]=='detected distances:':

                    print(data)

                    peak=float(data[0][22:26])

                    print(type(peak))

                if (x != [] and y != []):

                    # sort both x and y according to x

                    x, y = zip(*sorted(zip(x, y)))

                    plot_data(x, y, peak)



                    x = []

                    y = []

                continue

            x.append(_x)

            y.append(_y)

	    

    # Close serial port

    ser.close()



if __name__ == '__main__':

    main()

    # If user presses Ctrl+C, close serial port

    try:

        while True:

            pass

    except KeyboardInterrupt:

        ser.close()

        print("Serial port closed")

