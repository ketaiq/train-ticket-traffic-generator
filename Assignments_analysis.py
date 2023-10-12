from datetime import datetime
import numpy as np

"""
date_time_str = '2003-09-19 01:55:19,920'
date_time_obj_1 = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S,%f')
date_time_str = '2003-09-19 01:56:19,930'
date_time_obj_2 = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S,%f')
print("The type of the date is now",  type(date_time_obj_1))
print("The date is", date_time_obj_1)
rr = date_time_obj_2 - date_time_obj_1
print(type(rr), rr, int(rr.total_seconds()))
"""


def extract_till_minute(time_point_str):
	time_point_arr = time_point_str.split(":")
	time_str = time_point_arr[0] + ":" + time_point_arr[1]

	return time_str


f = open("assignments-2023-06-27_21:44:41.log", "r")
log_lines = f.read().split('\n')
f.close()

users_start = dict()
users_end = dict()
completed_tasks = dict()
incomplete_tasks = dict()

for line_idx, line in enumerate(log_lines):
	if line == "":
		continue

	line_arr = line.split(" ")
	line_num = line_idx + 1
	# print(line_num, line_arr)

	log_date = line_arr[0]
	log_time = line_arr[1]
	log_name = line_arr[2]
	log_status = line_arr[3]

	log_time = log_time.split(",")[0]
	date_time_str = log_date + " " + log_time

	if log_status == "start":
		if log_name not in users_start:
			users_start[log_name] = date_time_str
		else:
			print(line_num, "Double start of the task", log_name)
			exit()
	else:
		if log_status == "end":
			if log_name not in users_end:
				if log_name in users_start:
					start_date_str = users_start[log_name]
					start_date_obj = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
					end_date_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
					duration = int((end_date_obj - start_date_obj).total_seconds())
					users_end[log_name] = duration
					del users_start[log_name]

					if start_date_str not in completed_tasks:
						completed_tasks[start_date_str] = [duration]
					else:
						completed_tasks[start_date_str].append(duration)

				else:
					print(line_num, "The task does not have a start", log_name)
					exit()
			else:
				print(line_num, "Double end of the task", log_name)
				exit()
		else:
			print(line_num, "Status is undefined", log_name)
			exit()

# print("Users End:", users_end)
# print("Users Start:", users_start)

for user in users_start:

	start_date_str = users_start[user]

	if start_date_str not in incomplete_tasks:
		incomplete_tasks[start_date_str] = 1
	else:
		incomplete_tasks[start_date_str] += 1

# print("\nCompleted Tasks:")
# [print(task, completed_tasks[task], round(np.mean(completed_tasks[task]), 2), round(np.std(completed_tasks[task]), 2)) for task in completed_tasks]
# print("\nIncomplete Tasks:")
# [print(task, incomplete_tasks[task]) for task in incomplete_tasks]


completed_tasks_per_minutes = dict()
for time_point in completed_tasks:
	minute = extract_till_minute(time_point)

	if minute not in completed_tasks_per_minutes:
		completed_tasks_per_minutes[minute] = completed_tasks[time_point]
	else:
		completed_tasks_per_minutes[minute] += completed_tasks[time_point]

print("\nCompleted Tasks per minute:")
[print(task, round(np.mean(completed_tasks_per_minutes[task]), 2), round(np.std(completed_tasks_per_minutes[task]), 2)) for task in completed_tasks_per_minutes]


incomplete_tasks_per_minutes = dict()
for time_point in incomplete_tasks:
	minute = extract_till_minute(time_point)

	if minute not in incomplete_tasks_per_minutes:
		incomplete_tasks_per_minutes[minute] = [incomplete_tasks[time_point]]
	else:
		incomplete_tasks_per_minutes[minute] += [incomplete_tasks[time_point]]

print("\nIncomplete Tasks per minute:")
[print(task, round(np.mean(incomplete_tasks_per_minutes[task]), 2), round(np.std(incomplete_tasks_per_minutes[task]), 2)) for task in incomplete_tasks_per_minutes]