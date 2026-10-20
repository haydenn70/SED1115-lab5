# Lab 5 - make a histogram from log.txt
# Run this on your computer after copying log.txt from the Pico
import matplotlib.pyplot as plt

file = open("log.txt", "r")
times = []

for line in file:
    times.append(int(line.strip()))

file.close()

plt.hist(times, bins=range(min(times), max(times) + 2), edgecolor="black")
plt.xlabel("Time (seconds)")
plt.ylabel("Number of times")
plt.title("15 Second Game")
plt.savefig("histogram.png")
plt.show()
