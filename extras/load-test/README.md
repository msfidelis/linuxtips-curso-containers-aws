## Relatório de Teste de Performance - Produto de Cobrança de Vendas - Time de Engenharia 

--- 

## 1. Visão Geral

**Data**: DD/MM/AAAA  

**Aplicação / Jornada**: Checkout de Cartão de Crédito

**Versão**: 1.x.x  

**Ambiente de Teste**: Produção / Pré-produção / Desenvolvimento  

**Ferramentas Utilizadas**: Apache JMeter, Grafana K6, Locust, etc.

---

## 2. Objetivos do Teste

**Finalidade**: Avaliar o novo microserviço de checkout para garantir os SLA's de produto e encontrar oportunidades de melhoria de gargalos.

### Metas:

- **Tempo de Resposta**: Manter um tempo de resposta abaixo de 800 ms para 95% das requisições.
- **Throughput**: Garantir que o sistema processe ao menos 600 transações por segundo (TPS) com 800 usuários ativos.
- **Taxa de Erros**: Taxa de erro inferior a 0.1% em condições normais e de pico.
- **Escalabilidade**: Verificar as politicas de autoscaling para garanrit a capacidade transacional de escalar horizontalmente sem degradação total ou parcial.

---

## 3. Cenários de Teste

### 3.0. Pré-teste 

- **Objetivo**: Testar a capacidade de uma única réplica da aplicação de checkout.
- **Carga Simulada**: 100 requisições/s para 1 réplica
- **Protocolos Testados**: HTTP
- **Duração do Teste**: 10 minutos

**Expectativas**:
- A réplica deve suportar o tráfego sem degradação.
- Recursos como CPU e Memória devem ser utilizados dentro dos limites de 80%.

**Resultados**:
- CPU: 75% de utilização
- Memória: 60% de utilização
- Tempo de Resposta: 300ms
- Taxa de Erros: 0%
- Observações: O sistema conseguiu suportar a carga sem degradação, mantendo o uso de recursos dentro dos limites.

**Evidências**:

![Evidencia](/extras/load-test/images/teste-inicial.drawio.png)

---

### 3.1. Cenário 1: Carga Média (Average Load)

- **Objetivo**: Avaliar o comportamento do sistema sob condições de carga média constante.
- **Carga Simulada**: 500 usuários simultâneos
- **Protocolos Testados**: HTTP e Kafka
- **Duração do Teste**: 4 horas

**Expectativas**:
- Tempo de resposta médio < 300 ms
- Tempo de resposta p95 < 800 ms
- Taxa de erro <= 0.1% 

**Resultados**:
- Tempo de resposta médio: 250 ms
- Tempo de resposta do p95: 600 ms
- Taxa de erro: 0.0%
- Observações: O sistema se manteve dentro dos parâmetros esperados, sem sinais de sobrecarga durante todo o tempo proposto.

**Evidências**:

![Evidencia](/extras/load-test/images/teste-average.drawio.png)

---

### 3.2. Cenário 2: Carga de Pico (Spike Test)

- **Objetivo**: Simular os picos de tráfego dos principais horários de compra para identificar como o sistema reage aos aumentos repentinos.
- **Carga Simulada**: 2000 usuários simultâneos (pico) por 15 minutos
- **Protocolos Testados**: HTTP e Kafka
- **Duração do Teste**: 2 testes de 15 minutos

**Expectativas**:
- Tempo de resposta médio < 400 ms
- Tempo de resposta p95 < 800 ms
- Taxa de erro <= 0.1% 

**Resultados**:
- Tempo de resposta médio: 400 ms
- Tempo de resposta do p95: 700 ms
- Taxa de erro: 0.1%
- Observações: O sistema se aproximou do limite superior do tempo de resposta. Pequena degradação observada nos componentes de checkout e microserviços de comunicação com o parceiro.

**Evidências**:

![Evidencia](/extras/load-test/images/teste-spike.drawio.png)

---


### 3.3. Cenário 3: Stress Test

- **Objetivo**: Simular um tráfego de estresse no sistema com carga acima do previsto.
- **Carga Simulada**: 2000 usuários simultâneos (pico) por 1 hora
- **Protocolos Testados**: HTTP e Kafka
- **Duração do Teste**: 1 hora com aumento de 500 usuários a cada 15 minutos. 

**Expectativas**:
- Tempo de resposta médio < 400 ms
- Tempo de resposta p95 < 800 ms
- Taxa de erro <= 0.1% 

**Resultados**:
- Tempo de resposta médio: 500 ms
- Tempo de resposta do p95: 1300 ms
- Taxa de erro: 1%
- Observações: O sistema ofendeu aos limites estabelecidos pelo produto em torno de 1500 usuários. Identificamos a oportunidade de otimização de 2 queries no banco de dados do serviço de checkout que validam a idempotencia da transação e manipulam o estado de conclusão do pagamento. Após analises junto ao time de DBA's podemos superar esse problema criando um indice novo. 

**Evidências**:

![Evidencia](/extras/load-test/images/teste-stress.drawio.png)

---

### 3.4. Cenário 4: Breakpoint

- **Objetivo**: Encontrar em que momento de uso os limites estabelecidos começam a ser ofendidos e em que momentos as falhas começam a afetar o funcionamento a níveis críticos
- **Carga Simulada**: de 0 até 10000 usuários simultâneos até um limite de 24 horas. 
- **Protocolos Testados**: HTTP e Kafka
- **Duração do Teste**: limite de 24 horas com aumento incremental de 10 usuários por minuto


**Resultados**:
- Após 1300 usuários ativos, os tempos de resposta da aplicação começaram a subir e atingir o p95 de 800ms. 
- Após 1600 usuários ativos, os tempos de resposta da aplicação começaram a subir e atingir o p95 de 1500ms com 5% de taxa de erro. 
- Após 3000 usuários os erros por timeout começaram a se tornar constantes, chegando até 10% de todo o tráfego. O p95 chegou até 30 segundos. 
- Encontramos o limite de 3700 usuários. As aplicações começaram a falhar em cascata e os databases a travarem. 
 
**Evidências**:

![Evidencia](/extras/load-test/images/teste-breakpoint.drawio.png)