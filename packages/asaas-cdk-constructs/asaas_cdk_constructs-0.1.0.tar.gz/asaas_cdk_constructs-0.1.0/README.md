
# Projeto módulo de criação de regras do WAF usando CDK e Python!

<p align="center">
 <a href="#-sobre-o-projeto">Sobre</a> •
 <a href="#-funcionadades">Funcionalidades</a> • 
 <a href="#-como-usar-o-módulo-nos-projetos">Como usar o módulo nos projetos</a> • 
 <a href="#-gerando-uma-nova-versao-do-módulo">Gerando uma nova versão do módulo</a> • 
 <a href="#-tecnologias">Tecnologias</a> • 
</p>


## 💻 Sobre o projeto

Projeto módulo de criação de regras do WAF usando CDK e Python

---

## ⚙️ Funcionalidades

Esse é o módulo que cria os seguintes itens na AWS: 

- IPSet 
- WebACL

E as seguintes regras:

- GlobalIpRateLimit
- BlockApiOutsideAccess

---

## 🚀 Como usar o módulo nos projetos

Baixe a dependencia (módulo):

```
$ poetry shell
```

```
$ poetry add asaas-waf-module
```

Instale ou atualize as dependencias:

```
$ poetry install && poetry update
```

### 📦 Criando um novo IP Set com uma lista de IP's

No arquivo app.py inclua as informações conforme o exemplo abaixo:

```python

from asaas_waf_module.asaas_waf_module_stack import WafConstructStack

waf_stack = WafConstructStack(
    app,
    '<Nome_Recurso>WafConstructStack',
    aws_profile="sandbox",
    rate_limit=1000,
    is_allowed_asaas_ips=False,
    addresses=[
        "IP/32",
        "IP-01/32",
        "IP-NN/32",
    ],
    search_string_block_outside_access=["/api", "/srv"],
    env=cdk.Environment(
            account='276456543520',
            region='us-east-1'
        ),
)
```
---

### 📦 Usando o IP Set já existente

No arquivo app.py inclua as informações conforme o exemplo abaixo:

```python

from asaas_waf_module.asaas_waf_module_stack import WafConstructStack

waf_stack = WafConstructStack(
    app,
    '<Nome_Recurso>WafConstructStack',
    aws_profile="sandbox",
    rate_limit=1000,
    is_allowed_asaas_ips=True,
    search_string_block_outside_access=["/api", "/srv"],
    ip_set_id="<ID_IPSET>",
    env=cdk.Environment(
            account='276456543520',
            region='us-east-1'
        ),
)
```
---



## 🎲 Gerando uma nova versão do módulo ou criando um novo

Adicione o `CloudRepo` para poder exportar o módulo e atualizar:

```bash
$ poetry source add --priority=supplemental asaas-cdk-modules https://asaas.mycloudrepo.io/repositories/asaas-cdk-modules
$ poetry config http-basic.asaas-cdk-modules devops@asaas.com.br <senha>
$ poetry add --source asaas-cdk-modules private-package
```

Realize as devidas alterações ou correções e depois para atualizar o módulo faça:

No arquivo `setup.py` altere a versão do módulo na linha:

```
version='0.1.0',
```

Depois execute os comandos para atualizar o módulo:

```bash
$ poetry publish --build --repository asaas-cdk-modules
```
---

## 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

-   **[AWS CDK](https://docs.aws.amazon.com/cdk/api/v2/python/)**
-   **[Python](https://www.python.org/)**
-   **[Poetry](https://python-poetry.org/docs/)**
