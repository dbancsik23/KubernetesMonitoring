# KubernetesMonitoring
## ELK Stack installation on Kubernetes with Minikube


### Description : 
    A python micro service, which can be deployed in k8s. The available resources are [GET = "/","api/v1/products?ProductCode="], [POST = /api/v1/product -JSON body];
    JSON format 
        {
    "ProductName":"productname",
    "ProductCode":"productcode",
    "Price":1000
        }
    The database is an sqlite file, which is saved on a persistent volume.

### Requirements :
    docker
    minikube
    helm

### Commands: 
    helm repo add elastic https://helm.elastic.co
    helm repo update
#### Elasticsearch:
    helm install elk-elasticsearch elastic/elasticsearch -f values.yaml
      kubectl port-forward svc/elasticsearch-master 9200
    helm install kibana elastic/kibana
      kubectl port-forward deployment/kibana-kibana 5601
    helm install metricbeat elastic/metricbeat
      curl http://localhost:9200/_cat/indices
    helm install filebeat elastic/filbeat
### Python microserv:
    kubectl apply -f pv.yml
    kubectl apply -f pvc.yml
    kubectl apply -f deployment.yml
    kubectl port-forward deployment/python-docker 3251
### Grafana:
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    helm install grafana grafana/grafana -f .\values.yml
    kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}"
    kubectl --namespace default port-forward deployment/grafana 3000


