#!/bin/bash
# arg1: number of hours
minutes=$(($1 * 60))
for ((i=0; i < minutes; i++))
do
    echo "$timestamp i = $i"
    timestamp=$(date +%s)
    kubectl get pods -o json > "pods_info/${timestamp}.json"
    kubectl get nodes -o json > "nodes_info/${timestamp}.json"
    sleep 60
done