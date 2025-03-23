# Checklist Upgrade de Plataforma - Modelo

# Informações

* Cluster: linuxtips-lab-cluster
* Versão Atual: 1.19
* Versão do Upgrade: 1.20 
* Data do Upgrade: 24/03/2025
* Ponto Focal: Matheus Scarpato Fidelis


## Pré-Upgrade

- [ ] Confirmar versão atual e target do upgrade (ex: 1.31 → 1.32)
- [ ] Confirmar versões dos Addons Gerenciados para a nova versão

| Addon | Namespace | Versão Atual | Versão Upgrade | Validação  |
|coreds| kube-system | 1.15.0     | 1.32.1       | :white_check_mark:    |

- [ ] Confirmar versões dos Helm Charts de Componentes de Plataforma

| Helm | Namespace | Versão Atual | Versão Upgrade | Validação  |
|-------|----------|--------------|----------------|------------|
|kube-foo| kube-system | 1.58.2     | 1.76.1       | :white_check_mark:    |

- [ ] Identificar APIs deprecated ou removidas

Ferramenta: pluto

* v1 ComponentStatus is deprecated in v1.19+
* extensions/v1beta1 Ingress is deprecated in v1.14+, unavailable in v1.22+; use networking.k8s.io/v1 Ingress
* policy/v1beta1 PodSecurityPolicy is deprecated in v1.21+, unavailable in v1.25+

[ ] Verificar a Dispersão de Pods dos Componentes Críticos

[ ] Verificar a Dispersão de Pods das Aplicações

[ ] Definir janela de manutenção com stakeholders

* Data Upgrade Develop: 23/04/2025
* Data Upgrade Homolog: 25/04/2025
* Data Upgrade Production: 04/05/2025

### Backups
- [ ] Backup completo via Velero (`velero backup create`)
- [ ] Backup do etcd (clusters self-managed)
- [ ] Exportar recursos críticos com kubedump


## During Upgrade 

## Atualização do Cluster

- [ ] Atualizar os Nodegroups
- [ ] Atualizar a versão do control plane
- [ ] Atualizar `coredns`, `kube-proxy`, `vpc-cni`
- [ ] Atualizar a nova versão dos helm charts
- [ ] Monitorar eventos e status dos pods em tempo real
- [ ] Validar PDBs aplicados e se há pods pendentes ou stuck

## Observação Ativa
- [ ] Validar readiness/liveness probes
- [ ] Acompanhar logs, traces e métricas
- [ ] Rodar smoke tests automatizados ou manuais

## Restore das Aplicações

- [ ] Restarurar as aplicações via velero (se aplicável)
- [ ] Restarurar as aplicações via kubedump (se aplicável)


## Pós-Upgrade

### Verificação de Estado
- [ ] Validar estado de todos os Deployments, StatefulSets, CronJobs, etc
- [ ] Confirmar status dos DaemonSets e CSI plugins
- [ ] Conferir integridade de CRDs e dados migrados
- [ ] Avaliar latência, erros e throughput pós-upgrade
- [ ] Verificar alertas de falhas ou degradações de performance
- [ ] Comparar métricas pré e pós-upgrade