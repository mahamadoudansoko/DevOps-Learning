#!/bin/bash
# Cleanup Flask app from Kubernetes

set -e

NAMESPACE="flask-app"

echo "🧹 Cleaning up Flask app from Kubernetes..."

# Uninstall Helm release
echo "⎈ Uninstalling Helm release..."
helm uninstall flask-app -n $NAMESPACE || true

# Delete all resources in namespace
echo "🗑️ Deleting all resources..."
kubectl delete all --all -n $NAMESPACE || true
kubectl delete pvc --all -n $NAMESPACE || true
kubectl delete configmap --all -n $NAMESPACE || true
kubectl delete secret --all -n $NAMESPACE || true
kubectl delete ingress --all -n $NAMESPACE || true

# Delete namespace
echo "🗑️ Deleting namespace..."
kubectl delete namespace $NAMESPACE || true

echo "✅ Cleanup complete!"