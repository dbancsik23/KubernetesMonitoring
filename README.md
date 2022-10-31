# KubernetesMonitoring
## ELK Stack installation on Kubernetes with Minikube

### Requirements :
  docker
  minikube
  helm

### Commands: 
  helm repo add elastic https://helm.elastic.co \
  helm repo update
  #### Elasticsearch:
    helm install elk-elasticsearch elastic/elasticsearch -f values-2.yaml
      kubectl port-forward svc/elasticsearch-master 9200
    helm install kibana elastic/kibana
      kubectl port-forward deployment/kibana-kibana 5601
    helm install metricbeat elastic/metricbeat
      curl http://localhost:9200/_cat/indices
    helm install filebeat elastic/filbeat
  ### Python-microserv:
    kubectl apply -f pv.yml
    kubectl apply -f pvc.yml
    kubectl apply -f deployment.yml
      kubectl port-forward deployment/python-docker 3251


