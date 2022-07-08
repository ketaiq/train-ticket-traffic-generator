#!/bin/bash
echo "Scaling Start:"
# kubectl autoscale deployment ts-auth-service --cpu-percent=80 --min=1 --max=60
kubectl autoscale deployment ts-travel-service --cpu-percent=80 --min=1 --max=60
kubectl autoscale deployment ts-order-mongo --cpu-percent=80 --min=1 --max=50
kubectl autoscale deployment ts-route-service --cpu-percent=80 --min=1 --max=50
kubectl autoscale deployment ts-user-mongo --cpu-percent=80 --min=1 --max=60
kubectl autoscale deployment ts-auth-mongo --cpu-percent=80 --min=1 --max=60
kubectl autoscale deployment ts-route-mongo --cpu-percent=80 --min=1 --max=20
kubectl autoscale deployment ts-inside-payment-service --cpu-percent=80 --min=1 --max=20
kubectl autoscale deployment ts-order-service --cpu-percent=80 --min=1 --max=20
kubectl autoscale deployment ts-seat-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-avatar-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-execute-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-food-map-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-food-map-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-food-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-food-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-inside-payment-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-order-other-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-order-other-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-payment-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-payment-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-route-plan-service --cpu-percent=80 --min=1 --max=50
kubectl autoscale deployment ts-security-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-security-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-travel-plan-service --cpu-percent=80 --min=1 --max=50
kubectl autoscale deployment ts-travel2-mongo --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-travel2-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-ui-dashboard --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-user-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-verification-code-service --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-voucher-mysql --cpu-percent=80 --min=1 --max=10
kubectl autoscale deployment ts-voucher-service --cpu-percent=80 --min=1 --max=10
echo "Scaling End"