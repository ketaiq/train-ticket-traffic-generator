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

Collect node and pod information per minute in JSON files
```sh
sh collect_node_pod.sh 3
```