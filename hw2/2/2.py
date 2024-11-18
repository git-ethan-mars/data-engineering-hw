import os

import numpy

threshold = 515

m = numpy.load("second_task.npy")
x, y = (m > threshold).nonzero()
z = m[m > threshold]
numpy.savez("second_task_result.npz", x, y, z)
numpy.savez_compressed("second_task_result_compressed.npz", x, y, z)
print(
    f"COMPRESSED FILE = {os.stat("second_task_result_compressed.npz").st_size}, COMMON FILE = {os.stat("second_task_result.npz").st_size}")
