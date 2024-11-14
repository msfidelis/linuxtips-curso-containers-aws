
# Guia do Projeto Final do Módulo de ECS!!!

Primeiramente, saiba que eu estou extremamente orgulhoso de você ter chego até aqui. Sei que é uma jornada árdua mediante a correria do dia a dia, mas todo esforço vai valer a pena. O mundo é de quem não para :heart: 

O objetivo desse projeto é criar um workload multi-region, capaz de operar tanto `ATIVO/ATIVO` quando `ATIVO/PASSIVO`. Precisamos criar as camadas de networking em duas regiões, conectá-las, replicar a infraestrutura para manter as duas regiões operando sempre com os mesmos recursos e padrões, operar os mecanismos de replicação de dados da AWS para garantir consistência entre ambas, modularizar os componentes complexos de terraform e criar mecanismos de chavemento de tráfego entre as regiões para que seja possível "Ligar" e "Desligar" alguma das regiões se necessário. E é claro, em um fluxo de entrega contínua ~bem proximo~ do mundo real, claro com limitações de escopo pra não complicar a vida de ninguém.

As aplicações que vão realizar o trábalho de processamento já estão prontas e com sua documentação abaixo de como utilizá-las com suas dependências. Cabe a nós transformar isso em um workload real, com elasticidade, tolerância a falhas, performático e principalmente... Legal demais :heart: 

Abaixo iremos detalhar um pouco mais sobre a arquitetura, propostas, componentes e recursos das aulas. 

# Arquitetura Multi-Region

A arquitetura iremos ter um endpoint REST que irá receber requisições de registros de venda, irá persistir esses dados e encaminhar por meio do SNS esse objeto de domínio para se processado de fato. O SNS irá publicar a mensagem em uma - ou mais - filas SQS fazendo Fanout, que será consumida por um worker que irá tratar os dados, "processar a compra" e salvar para um "lake" no S3. Tudo isso mediante a idempotencia. 

![Arquitetura Multi-Region](/assets/projeto-final-ecs.drawio.png)


Nessa arquitetura iremos utilizar 

* API Gateway + Custom Domain Names
* AWS Global Accelerator
* Network Load Balancers e Application Load Balancers
* Amazon ECS (Cluster, Service, Tasks)
* DynamoDB + DynamoDB Streams
* DynamoDB Global Tables (Replicação
* Simple Notification Service (SNS) com Fanout Cross Region
* Simple Queue Service (SQS)
* Parameter Stores como Feature Toggles
* E mais o que você quiser, você é livre a partir daqui... 


# Recursos das Aulas

| Recurso / Aula                                  | Repositório                                                                                         |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Registry de Modules                             | [Link do Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-modules)               |
| Modulo de Terraform da VPC                      | [Link do Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-modules/vpc)           |
| VPC / Networking - MultiRegion                  | [Link do Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-multiregion-vpc)       |
| Modulo de Terraform do Cluster                  | [Link do Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-modules/cluster)       |
| Cluster - MultiRegion                           | [Link do Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-multiregion-cluster)   |
| Routing / AWS Global Accelerator - MultiRegion  | [Link do Github](https://github.com/msfidelis/linuxtips-curso-containers-aws-multiregion-routing)   |
| Script de Pseudo-Pipeline Multi-Region          | [Link do Github](/extras/ecs-projeto-final/pipeline.sh)                                             |
| Script de Destroy                               | [Link do Github](/extras/ecs-projeto-final/pipeline-destroy.sh)                                     |
| Exemplo de Pipeline Multi-Region no Actions     | [Link do Github](/extras/ecs-projeto-final/workflows/multiregion.yml)                               |



# Aplicações 

## Sales API

### Infomações Importantes

* Descrição: API REST responsável por receber os pedidos de venda de uma loja, registrar e enviar para processamento. 
* Porta: `8080`
* Recursos Mínimos: `256m` de CPU e `512Mb` de RAM
* Healthcheck: `/healthcheck`
* Imagem: `fidelissauro/sales-rest-api:latest`

### Variáveis de Ambiente

| Name                          | Value                                                                                     |
|-------------------------------|-------------------------------------------------------------------------------------------|
| `AWS_REGION`                  | Região na qual a aplicação está rodando                                                   |
| `SNS_SALES_PROCESSING_TOPIC`  | ARN do tópico do SNS que a aplicação publicará os pedidos de venda                        |
| `SSM_PARAMETER_STORE_STATE`   | Parameter Store que guarda o estado da aplicação. Entende os valores `ACTIVE` e `PASSIVE` |
| `DYNAMO_SALES_TABLE`          | Nome da tabela do DynamoDB que salva as vendas                                            |

### Rotas da API 

| Name          | Método    | Descrição                                                                                 |
|---------------|-----------|-------------------------------------------------------------------------------------------|
| `/sales`      | `POST`    | Cria um registro de venda no sistema e retorna o mesmo com um `id` para consulta          |
| `/sales/{id}` | `GET`     | Consulta os dados da venda de um registro informado pelo `id`                             |
| `/sales/{id}` | `DELETE`  | Cancela uma venda informada pelo `id`                                                     |


### Payloads de Exemplo

> Novo Registro de Venda

```bash
curl -X POST http://sales.linuxtips.demo/sales -d '{"product":"O Pequeno Principe", "amount": 14.00}' -i
```

> Consultando uma venda

```bash
curl -X GET http://sales.linuxtips.demo/sales/{id}  -i
```


> Cancelando uma venda

```bash
curl -X DELETE http://sales.linuxtips.demo/sales/{id}  -i
```


## Sales Worker

### Infomações Importantes

* Descrição: Aplicação responsável por consumir os pedidos de venda de um SQS, "processá-los" mediante a idempotencia e salvar os metadados no S3 de um "datalake" hipotético
* Porta: `8080`
* Recursos Mínimos: `256m` de CPU e `512Mb` de RAM
* Healthcheck: `/healthcheck`
* Imagem: `fidelissauro/sales-worker:latest`


* Variáveis de Ambiente

| Name                              | Value                                                                                     |
|-----------------------------------|-------------------------------------------------------------------------------------------|
| `AWS_REGION`                      | Região na qual a aplicação está rodando                                                   |
| `SQS_SALES_QUEUE`                 | URL da Queue que processa os pedidos de venda                                             |
| `SSM_PARAMETER_STORE_STATE`       | Parameter Store que guarda o estado da aplicação. Entende os valores `ACTIVE` e `PASSIVE` |
| `DYNAMO_SALES_TABLE`              | Nome da tabela do DynamoDB que salva as vendas                                            |
| `DYNAMO_SALES_IDEMPOTENCY_TABLE`  | Nome da tabela do DynamoDB que controla idempotencia do processamento                     |
| `S3_SALES_BUCKET`                 | Bucket do S3 onde serão armazenados os registros processados                              |
