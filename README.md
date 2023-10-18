# train-ticket-analysis

Run `locust` to start sending requests.

Run `python test.py` to do unit testing.

## Resources

SBB’s route network: https://data.sbb.ch/explore/dataset/linie/information/  
Number of SBB station users: https://data.sbb.ch/explore/dataset/anzahl-sbb-bahnhofbenutzer/information/  
Direct Trains in Europe: https://data.sbb.ch/explore/dataset/direktverbindungen/information/

## Environment Configuration

1. Install all required packages by running `conda create -n train-ticket-test --channel=conda-forge python locust pandas pymongo`.
2. Activate the conda environment by running `conda activate train-ticket-test`.

## Quick Start

### Collect node and pod information per minute in JSON files
```sh
nohup bash collect_node_pod.sh 14 &
```

### Update *experiment_config.yaml*
- *tt_host*: the URL of the dashboard of TrainTicket system
- *wl_file_name*: the filename of the used workload
- *wl_start_hour*: the starting hour of the workload, from 0 to 23.
