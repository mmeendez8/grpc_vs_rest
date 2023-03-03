# gRPC vs REST


## 1. Base Benchmark

Deploy gRPC and REST servers:

```bash
kubectl apply -f base_benchmark/grpc/k8s/deployment.yaml
kubectl apply -f base_benchmark/rest/k8s/deployment.yaml
```

Once they are deployed and ready, run the benchmark client.

Note you need to update http and grpc urls in the [client deployment file](base_benchmark/client/k8s/deployment.yaml).

```bash
kubectl apply -f base_benchmark/client/k8s/deployment.yaml
```

## 2. Torchserve Benchmark

Deploy Torchserve:

```bash
kubectl apply -f torchserve_benchmark/torchserve/k8s/deployment.yaml
```

Note this deployment requires GPU available in the cluster and that you need to update http and grpc urls in the [client deployment file](torchserve_benchmark/client/k8s/deployment.yaml).

Register example model from torchserve registry:

```bash
curl -X POST "http://[SERVICE-URL]:8081/models?url=https://torchserve.pytorch.org/mar_files/densenet161.mar&initial_workers=1"
```
