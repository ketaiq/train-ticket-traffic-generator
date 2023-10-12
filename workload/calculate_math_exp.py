import csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

file_name_wl_pattern_weekdays = "wl_pattern_weekdays.csv"
file_name_wl_pattern_weekends = "wl_pattern_weekends.csv"


def get_wl_pattern(wl_pattern_file_name):
	workload = defaultdict(list)
	with open(wl_pattern_file_name) as fil:
		csv_reader = csv.DictReader(fil, delimiter=",")
		for row in csv_reader:
			for key, value in row.items():
				workload[key].append(value)

	users_list = [int(xx) for xx in list(workload.items())[0][1]]
	return users_list


if __name__ == "__main__":
	file_name_wl = "wl_fi_1.csv"

	wl_pattern_weekdays = get_wl_pattern(file_name_wl_pattern_weekdays)
	wl_pattern_weekends = get_wl_pattern(file_name_wl_pattern_weekends)

	plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
	plt.hist(wl_pattern_weekdays)
	plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
	plt.show()

	mean = int(round(np.median(wl_pattern_weekdays) * 5/7 + np.median(wl_pattern_weekends) * 2/7))
	std = int(round(np.std(wl_pattern_weekdays + wl_pattern_weekends)))
	the_rate = mean + 1 * std

	print("Mean:", mean)
	print("Std:", std)
	print("The rate:", the_rate)

	wl_list = [the_rate for ii in range(60 * 24 * 7)]

	with open(file_name_wl, 'w') as fil:
		writer = csv.writer(fil)
		writer.writerow(["Users", "SpawnRate"])
		for xx in wl_list:
			writer.writerow([xx, 1])