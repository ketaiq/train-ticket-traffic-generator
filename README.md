# train-ticket-analysis

Run `locust` to start sending requests.

Run `python test.py` to do unit testing.

## Resources

SBB’s route network: https://data.sbb.ch/explore/dataset/linie/information/  
Number of SBB station users: https://data.sbb.ch/explore/dataset/anzahl-sbb-bahnhofbenutzer/information/  
Direct Trains in Europe: https://data.sbb.ch/explore/dataset/direktverbindungen/information/

## Environment Configuration

- Conda

1. Install all required packages by running ``.
2. Activate the conda environment by running ``.

## Quick Start

### Create Google Cloud Virtual Machine

- Machine: e2-medium (2 vCPU, 1 core, 4 GB memory)
- Disk size: 50 GB
- Network: expose port 8089 for locust report

### Install Packages

```sh
# install git
sudo apt update
sudo apt install git

# install gcloud and kubectl
sudo apt-get install apt-transport-https ca-certificates gnupg curl sudo
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-451.0.1-linux-x86_64.tar.gz
tar -xf google-cloud-cli-451.0.1-linux-x86_64.tar.gz

./google-cloud-sdk/install.sh
./google-cloud-sdk/bin/gcloud init

gcloud components install kubectl

# install conda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

# initialize conda
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

# install Python and related packages
conda create -n train-ticket --channel=conda-forge python=3.10 locust=2.17 pandas=2.1 pymongo=4.5 pyyaml=6.0
```

### Start locust

```sh
# activate conda environment
conda activate train-ticket
nohup locust &
```

### Connect to TrainTicket cluster

```sh
gcloud container clusters get-credentials train-ticket-cluster --zone us-central1-c --project iron-bedrock-366809
```

### Collect node and pod information per minute in JSON files
```sh
nohup bash collect_node_pod.sh 14 &
```

### Update *experiment_config.yaml*
- *tt_host*: the URL of the dashboard of TrainTicket system
- *wl_file_name*: the filename of the used workload
- *wl_start_hour*: the starting hour of the workload, from 0 to 23.

### Collect Locust Metrics
```sh
tar -czvf archive.tar.gz *.log *.csv nohup.out nodes_info pods_info train-ticket-report.html
gcloud compute scp --project "iron-bedrock-366809" train-ticket-traffic-generator-102009:/home/ketai/train-ticket-traffic-generator/archive.tar.gz ~/Downloads/
```