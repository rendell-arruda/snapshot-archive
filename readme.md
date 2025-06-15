# 🧊 Snapshot Archiver – AWS EC2 Snapshot Tier Automation

Automação em Python para arquivar snapshots do Amazon EBS que ainda estão no **storage tier padrão**.  
Este script assume uma role em outra conta AWS (via STS), lista os snapshots e arquiva apenas os que ainda não estão no tier `archive`.

Ideal para equipes de **FinOps** e **CloudOps** que desejam reduzir custos com snapshots antigos.

---

## 🚀 Funcionalidades

- ✅ Assume role em outra conta AWS com `boto3` e `sts.assume_role`
- ✅ Lista todos os snapshots da conta (proprietário = self)
- ✅ Filtra apenas os snapshots no tier `standard`
- ✅ Arquiva os snapshots com suporte a `dry-run`
- ✅ Tratamento de erro com `ClientError`
- 🔜 Pronto para integração com **logs estruturados**, **Slack**, **dashboard**, e **Lambda**

---
## 📦 Requisitos

Instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## 📁 Estrutura do Projeto

```
snapshot_archiver/
├── snapshot_archiver.py
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 📚 Explicação dos Arquivos

- `snapshot_archiver.py`: script principal com as funções de login, filtragem e arquivamento
- `requirements.txt`: dependências Python necessárias (`boto3`)
- `LICENSE`: licença do projeto (MIT)
- `README.md`: este arquivo que você está lendo

---

## 🧠 Conceitos Utilizados

- **STS Assume Role** – para operar em outra conta AWS com permissões temporárias
- **EC2 Snapshot Tier** – uso do método `modify_snapshot_tier` com `DryRun` para simulação
- **Filtro inteligente** – apenas snapshots `standard` são arquivados
- **FinOps Ready** – pensado para redução de custos e automações simples

---

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 🤝 Contribuição

Quer contribuir? Faça um fork ou entre em contato comigo!

> Feito pelo IlustreDev para ajudar na jornada FinOps!