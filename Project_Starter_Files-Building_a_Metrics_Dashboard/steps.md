# Projects Steps

## 1. Up-and-running with vagrant
1. Rename Vagrantfile.sample to Vagrantfile
2. bring up Vagrant machine
```bash
vagrant up
```




## 2. Install Prometheus and Grafana
1. Install Helm 
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
2. Create Monitoring namespace
```bash
kubectl create namespace monitoring
```
3. Install Prometheus and Grafana
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm repo add stable https://kubernetes-charts.storage.googleapis.com # this is deprecated
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml
```
4. Verify installation
```bash
# Screenshot 001.png
kubectl get pods,svc --namespace=monitoring
```
5. Expose Grafana using port-forward command and add Prometheus as data source
```bash
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring
# Screenshot 002.png
```

## 3. Install Jaeger
1. Create Observability namespace
```bash
kubectl create namespace observability
```
2. Install Jaeger Operator
```bash
# Please use the last stable version
export jaeger_version=v1.28.0 
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/operator.yaml
```
3. Enable Jaeger Cluster-wide permission
```bash
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/cluster_role_binding.yaml

```
4. Add Jaeger as Grafana Data Source
```
# Add Jaeger using Grafana UI using this URL
jaeger-operator-metrics.default.svc.cluster.local:16686
```

## 4. Deploy python application
1. Install Vagrant plugin
```bash
vagrant plugin install vagrant-scp
```
2. Copy Manifest files to vagrant
```bash
vagrant scp manifests/app/backend.yaml backend.yaml
vagrant scp manifests/app/frontend.yaml frontend.yaml
vagrant scp manifests/app/trial.yaml trial.yaml
```
3. Apply Manifest to Kubernetes 
```bash
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f trial.yaml
```

## 5. Expose Grafana
1. Expose Grafana Service
```bash
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring
```

## 6. Expose Front-end application
```bash
kubectl port-forward svc/frontend-service 8080:8080
```