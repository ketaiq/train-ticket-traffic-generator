import yaml

with open("experiment_config.yaml") as stream:
    experiment_config = yaml.safe_load(stream)
tt_host = experiment_config["tt_host"]
wl_file_name = experiment_config["wl_file_name"]
wl_start_hour = int(experiment_config["wl_start_hour"])
wl_day = int(experiment_config["wl_day"])  # 0 to 6 -> Monday to Sunday
use_2week_workload = experiment_config["use_2week_workload"]

with open("workload/workload_config.yaml") as stream:
    workload_config = yaml.safe_load(stream)
weekday_peak_hours = workload_config["weekday_peak_hours"]
weekend_peak_hours = workload_config["weekend_peak_hours"]
wl_interval_mins = workload_config["wl_interval_mins"]
wl_num_start_interval = workload_config["wl_num_start_interval"]
