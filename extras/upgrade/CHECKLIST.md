# Checklist Upgrade de Plataforma - Modelo

# Informações

* Cluster: linuxtips-lab-cluster
* Versão Atual: 1.31
* Versão do Upgrade: 1.32 
* Data do Upgrade: 24/03/2025
* Ponto Focal: Matheus Scarpato Fidelis


## Pré-Upgrade

- [ ] Confirmar versão atual e target do upgrade (ex: 1.31 → 1.32)
- [ ] Confirmar versões dos Addons Gerenciados para a nova versão
- [ ] Confirmar versões dos Helm Charts de Componentes de Plataforma

| Helm | Namespace | Versão Atual | Versão Upgrade | Validação  |
|-------|----------|--------------|----------------|------------|
|kube-foo| kube-system | 1.58.2     | 1.76.1       | :check:    |