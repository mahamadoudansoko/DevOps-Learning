#!/bin/bash
# Deploy Flask app to Kubernetes

set -e

ENVIRONMENT=${1:-dev}
NAMESPACE="flask-app"

echo "🚀 Deploying Flask app to $ENVIRONMENT environment..."

# Create namespace if not exists
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply base manifests
echo "📦 Applying base manifests..."
kubectl apply -f k8s/overlays/$ENVIRONMENT/

# Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/flask-api -n $NAMESPACE

echo "✅ Deployment complete!"
kubectl get pods -n $NAMESPACE