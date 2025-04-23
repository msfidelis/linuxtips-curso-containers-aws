
# Guia do Projeto Final do Módulo de EKS!!!

Primeiramente, saiba que eu estou extremamente orgulhoso de você ter chego até aqui. Sei que é uma jornada árdua mediante a correria do dia a dia, mas todo esforço vai valer a pena. O mundo é de quem não para :heart: 

O objetivo desse projeto é criar um ambiente distribuido de multiplos clusters de Kubernetes na AWS, onde iremos gerenciar todos os helm charts, addons e cargas de trabalho de aplicações de forma centralizada entre eles com o ArgoCD e também centralizar de forma resiliênte e inteligente o ferramental de observability que irá receber traces, logs e metricas de vários clusters e disponibizá-los para consumo. 

Assim como o [projeto de ecs](/extras/ecs-projeto-final/), a ideia é fornecer mecanismos que nos ajudem a escalar de forma sustentável e com muita resiliência em ambientes corporativos de médio/grande porte. 


## Repositórios do Projeto

| Repositório                       | Link                                                                                                                  |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| VPC / Networking                  | [Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-eks-networking)                                  |
| Ingress Application Load Balancer | [Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-eks-multicluster-management/tree/main/ingress)   |
| EKS Cluster 01 e 02               | [Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-eks-multicluster-management/tree/main/clusters)  |
| EKS Control Plane do ArgoCD       | [Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-eks-multicluster-management/tree/main/clusters)  |


## Primeira Parte - Gestão Multi-Cluster com ArgoCD 

![ArgoCD](/assets/projeto-final-argocd-workload.drawio.png)

O objetivo da primeira parte é utilizar o ArgoCD como um control plane, de forma que seja possivel gerenciar o conteúdo de multiplos clusters de forma simples e segura. Na arquitetura proposta iremos ter **dois clusters de produção em modelo ativo/ativo**, um **balanceador que irá controlar a % de distribuição de trafego entre ambos** os clusters de forma customizada via terraform, um **cluster de ArgoCD que irá ter permissões para realizar deploy** de recursos em ambos os clusters de produção.

O modelo proposto deverá permitir que qualquer cluster consiga ser totalmente retirado de carga para eventuais manutenções, testes e upgrades. 


## Segunda Parte - Cluster de Observability 

![Observability](/assets/projeto-final-observability.drawio.png)

* **Grafana Loki**: Indexação de Logs
* **Grafana Tempo**: Indexação de Traces e Spans
* **Grafana Mimir**: Indexação de Métricas do prometheus 
* **Grafana Dashboard**: Visualização de Dados, Métricas, Logs e Traces
* **FluentBit**: Captura e envio de logs do Kubernetes para o Loki
* **OpenTelemetry Collector**: Envio de Traces e Spans para o Tempo
* **Prometheus**: Coleta de Métricas e envio para o Mimir


![Grafana](/assets/projeto-final-grafana.png)