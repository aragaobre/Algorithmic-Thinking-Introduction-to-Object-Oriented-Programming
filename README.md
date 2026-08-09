# Orçamento de Aluguel R.M Imobiliária

Sistema de orçamento de locação em Python, desenvolvido para a disciplina de Pensamento Algorítmico e Introdução à Programação Orientada a Objetos.

A aplicação simula o sistema de uma imobiliária fictícia (R.M) que trabalha com três tipos de imóvel **Apartamento**, **Casa** e **Estúdio**, cada um com suas próprias regras de valores adicionais e descontos. O programa coleta os dados do cliente, calcula o orçamento completo (aluguel + contrato) e exporta um arquivo `.csv` com o cronograma das 12 parcelas.

## Funcionalidades

- Cadastro de imóveis com localização, metragem, banheiros e valor base
- Regras específicas por tipo de imóvel:
  - **Apartamento** (R$ 700,00): +R$ 200,00 para 2 quartos, +R$ 300,00 garagem, 5% de desconto sem criança
  - **Casa** (R$ 900,00): +R$ 250,00 para 2 quartos, +R$ 300,00 garagem
  - **Estúdio** (R$ 1.200,00): +R$ 250,00 estacionamento (2 vagas), +R$ 60,00 por vaga extra
- Contrato de R$ 2.000,00 parcelável em até 5 vezes
- Validação de todas as entradas do usuário (código do imóvel, respostas Sim/Não, forma de pagamento, número de parcelas)
- Geração automática de arquivo `.csv` com as 12 parcelas e datas de vencimento calculadas a partir da data atual

## Tecnologias

- Python 3
- Módulos da biblioteca padrão: `csv`, `datetime`, `calendar`

## Estrutura orientada a objetos

```
Imovel (classe base)
├── Apartamento
├── Casa
└── Estudio

Contrato
Orcamento (compõe Imovel + Contrato)
```

- **Herança**: `Apartamento`, `Casa` e `Estudio` herdam de `Imovel`
- **Polimorfismo**: cada subclasse implementa `perguntar_opcionais()` à sua própria maneira
- **Encapsulamento**: cada classe guarda seus próprios dados e constantes de regra de negócio
- **Composição**: `Orcamento` combina um `Imovel` e um `Contrato` para gerar o resumo e o CSV

## Como executar

```bash
python "Orçamento_de_Aluguel.py"
```

O programa é interativo via terminal: peça o nome do cliente, escolha um imóvel pelo código exibido, responda às perguntas específicas do tipo escolhido, selecione a forma de pagamento e o número de parcelas do contrato.

Ao final, é gerado o arquivo `orcamento_aluguel.csv` na mesma pasta, com o resumo completo e o cronograma de 12 parcelas.

## Exemplo de uso

```
Digite o nome do cliente: Maria

=========== IMÓVEIS DISPONÍVEIS ===========
AP01 - Apartamento | Av. Oceânica, 1450 - Barra - Salvador/BA | 68 m² | R$ 700.00
...

Digite o código do imóvel desejado: AP02
Deseja 2 Quartos? (S) Sim | (N) Não: s
Deseja vaga de garagem? (S) Sim | (N) Não: s
Possui criança? (S) Sim | (N) Não: n
...
```

## Documentação

O fluxograma da aplicação (elaborado no [draw.io](https://app.diagrams.net)) e a descrição do pensamento algorítmico aplicado estão no relatório em PDF entregue junto com este repositório (Parte Teórica).

## Autor
- Aluno: Brenda Aragão
- Disciplina: Algorithmic Thinking & Introduction to Object-Oriented Programming
- UniFECAF
