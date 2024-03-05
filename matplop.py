import matplotlib.pyplot as plt

x = [0.050045, 0.060055, 0.070064, 0.080073, 0.090082, 0.100091, 0.210191, 0.2202, 0.230209, 0.240218, 0.250227, 0.260237, 0.270246, 0.280255, 0.290264, 0.300273, 0.310282, 0.320291, 0.3303, 0.340309, 0.350318, 0.360327, 0.370337, 0.380346, 0.390355, 0.400364, 0.410373, 0.420382, 0.430391, 0.4404, 0.450409, 0.460418, 0.470428, 0.480437, 0.490446, 0.500455, 0.510464, 0.520473, 0.530482, 0.540491, 0.5505, 0.560509, 0.570519, 0.580528, 0.590537, 0.600546, 0.610555, 0.620564, 0.630573, 0.640582, 0.650591, 0.6606, 0.670609, 0.680619, 0.690628, 0.700637, 0.710646, 0.720655, 0.730664, 0.740673, 0.750682, 0.760691, 0.7707, 0.78071, 0.790719, 0.800728, 0.810737, 0.820746, 0.830755, 0.840764, 0.850773, 0.860782, 0.870791, 0.8808, 0.89081, 0.900819, 0.910828, 0.920837, 0.930846, 0.940855, 0.950864, 0.960873, 0.970882, 0.980891, 0.990901, 1.00091, 1.010919, 1.020928, 1.030937, 1.040946, 1.050955, 1.060964, 1.070973, 1.080982, 1.090991, 1.101001, 1.11101, 1.121019, 1.131028, 1.141037, 1.151046, 1.161055, 1.171064, 1.181073, 1.191082, 1.201092, 1.211101, 1.22111, 1.231119, 1.241128, 1.251137, 1.261146, 1.271155, 1.281164, 1.291173, 1.301183, 1.311192, 1.321201, 1.33121, 1.341219, 1.351228, 1.361237, 1.371246, 1.381255, 1.391264, 1.401273, 1.411283, 1.421292, 1.431301, 1.44131, 1.451319, 1.461328, 1.471337, 1.481346, 1.491355, 1.501364, 1.511373, 1.521383, 1.531392, 1.541401, 1.55141, 1.561419, 1.571428, 1.581437, 1.591446, 1.601455, 1.611464, 1.621474, 1.631483, 1.641492, 1.651501, 1.66151, 1.671519, 1.681528, 1.691537, 1.701546, 1.711555, 1.721564, 1.731574, 1.741583, 1.751592, 1.761601, 1.77161, 1.781619, 1.791628, 1.801637, 1.811646, 1.821655, 1.831665, 1.841674, 1.851683, 1.861692, 1.871701, 1.88171, 1.891719, 1.901728, 1.911737, 1.921747, 1.931756, 1.941765, 1.951774, 1.961783, 1.971792, 1.981801, 1.99181, 2.001819, 2.011828, 2.021837, 2.031847, 2.041856, 2.051865, 2.061874, 2.071883, 2.081892, 2.091901, 2.10191, 2.111919, 2.121928, 2.131937, 2.141947, 2.151956, 2.161965, 2.171974, 2.181983, 2.191992, 2.202001, 2.21201, 2.222019, 2.232028, 2.242038, 2.252047, 2.262056, 2.272065, 2.282074, 2.292083, 2.302092, 2.312101, 2.32211, 2.332119, 2.342129, 2.352138, 2.362147, 2.372156, 2.382165, 2.392174, 2.402183, 2.412192, 2.422201, 2.43221]
y = [248.0, 271.0, 153.0, 10.0, 27.0, 26.0, 5.0, 6.0, 4.0, 10.0, 0.0, 21.0, 7.0, 7.0, 2.0, 11.0, 17.0, 16.0, 2.0, 15.0, 14.0, 3.0, 17.0, 23.0, 12.0, 8.0, 28.0, 9.0, 2.0, 4.0, 7.0, 11.0, 19.0, 19.0, 12.0, 13.0, 8.0, 6.0, 10.0, 6.0, 17.0, 9.0, 8.0, 22.0, 23.0, 40.0, 12.0, 13.0, 33.0, 37.0, 15.0, 6.0, 12.0, 24.0, 10.0, 13.0, 11.0, 6.0, 27.0, 25.0, 9.0, 10.0, 7.0, 15.0, 9.0, 15.0, 12.0, 12.0, 6.0, 2.0, 4.0, 4.0, 7.0, 10.0, 5.0, 9.0, 5.0, 0.0, 16.0, 14.0, 8.0, 7.0, 15.0, 9.0, 12.0, 7.0, 4.0, 12.0, 12.0, 11.0, 1.0, 2.0, 8.0, 2.0, 8.0, 3.0, 4.0, 0.0, 1.0, 14.0, 7.0, 13.0, 7.0, 3.0, 14.0, 4.0, 4.0, 12.0, 2.0, 8.0, 5.0, 4.0, 2.0, 0.0, 3.0, 2.0, 1.0, 2.0, 5.0, 1.0, 5.0, 1.0, 3.0, 2.0, 4.0, 7.0, 1.0, 1.0, 1.0, 3.0, 3.0, 4.0, 3.0, 6.0, 4.0, 2.0, 4.0, 6.0, 8.0, 3.0, 6.0, 4.0, 3.0, 1.0, 6.0, 2.0, 3.0, 5.0, 3.0, 0.0, 4.0, 4.0, 5.0, 4.0, 1.0, 5.0, 4.0, 3.0, 5.0, 5.0, 1.0, 2.0, 6.0, 7.0, 2.0, 4.0, 3.0, 7.0, 3.0, 3.0, 1.0, 0.0, 2.0, 3.0, 1.0, 3.0, 2.0, 2.0, 0.0, 2.0, 1.0, 3.0, 2.0, 3.0, 8.0, 6.0, 4.0, 1.0, 2.0, 1.0, 3.0, 3.0, 2.0, 3.0, 5.0, 3.0, 3.0, 2.0, 1.0, 3.0, 4.0, 1.0, 0.0, 2.0, 2.0, 2.0, 1.0, 3.0, 0.0, 0.0, 2.0, 0.0, 1.0, 1.0, 3.0, 0.0, 2.0, 1.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 2.0]
plt.xlabel('Distance (m)')
plt.ylabel('Amplitude')
plt.title('Distance vs Amplitude')
# set axis limits
plt.xlim(0, 2.4)
plt.ylim(0, 1000)
plt.axvline(2,color='r')

int1 = [.065, 800.0]
int2 = [.250, 200.0]
int3 = [2.200, 75.0]
plt.plot([int1[0], int2[0], int3[0]], [int1[1], int2[1], int3[0]], linestyle="solid")

plt.plot(x, y,'-.')
plt.draw()
plt.pause(0.0000000001)
plt.clf()

input()