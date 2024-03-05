import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Sample data (replace with your actual data)
x = np.linspace(0, 2.4, 100)  # 100 sample points between 0 and 2.4 meters
y = np.random.randint(0, 1000, size=100)  # Random amplitude values between 0 and 1000 dB

# Finding peaks
peaks, _ = find_peaks(y, height=800)
print(peaks)  # Adjust 'height' as needed

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Amplitude')
plt.plot(x[peaks], y[peaks], 'x', label='Peaks')
plt.title('Peak Detection in Signal')
plt.xlabel('Distance (meters)')
plt.ylabel('Amplitude (dB)')
plt.legend()
plt.grid(True)
plt.show()
