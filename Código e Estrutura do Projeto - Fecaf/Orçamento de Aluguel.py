import csv
import datetime
import calendar


# ----------------------------------------------------------
# FUNÇÕES AUXILIARES (formatação de número e data)
# ----------------------------------------------------------
# REGRAS DE FORMATAÇÃO PARA O CSV (EXCEL EM PORTUGUÊS)
# - O Excel BR espera VÍRGULA como separador decimal (ex: 700,00),
#   por isso a função fmt() troca o ponto do Python pela vírgula.
# - O CSV usa PONTO E VÍRGULA (;) como separador de colunas, então
#   a vírgula do número não conflita com a separação das colunas.
# - As datas são geradas no formato dd/mm/aaaa (padrão brasileiro),
#   calculadas a partir da data de hoje com a função somar_meses().
# ----------------------------------------------------------

def fmt(valor):
    """Formata número no padrão brasileiro (vírgula como decimal)."""
    return f'{valor:.2f}'.replace('.', ',')


def somar_meses(data, meses):
    """Soma 'meses' a uma data, ajustando o dia se o mês de destino
    tiver menos dias (ex: dia 31 de janeiro + 1 mês = 28/29 de fevereiro)."""
    mes_total = data.month - 1 + meses
    ano = data.year + mes_total // 12
    mes = mes_total % 12 + 1
    ultimo_dia_do_mes = calendar.monthrange(ano, mes)[1]
    dia = min(data.day, ultimo_dia_do_mes)
    return datetime.date(ano, mes, dia)


def perguntar_sn(mensagem):
    """Pergunta algo ao usuário até receber 's' ou 'n' como resposta."""
    resposta = input(mensagem).strip().lower()
    while resposta not in ('s', 'n'):
        print('Opção inválida! Digite apenas S para Sim ou N para Não.')
        resposta = input(mensagem).strip().lower()
    return resposta


# ----------------------------------------------------------
# CLASSE BASE: IMOVEL
# ----------------------------------------------------------
# Todo imóvel (Apartamento, Casa ou Estúdio) tem essas características
# em comum. As regras específicas de cada tipo (o que pode ser
# adicionado, com quanto custa) ficam nas subclasses.
# ----------------------------------------------------------

class Imovel:
    def __init__(self, codigo, localizacao, metragem, banheiros, valor_base):
        self.codigo = codigo
        self.localizacao = localizacao
        self.metragem = metragem
        self.banheiros = banheiros
        self.valor_base = valor_base

        # Valores que podem mudar de acordo com as escolhas do cliente
        self.quartos = '1'
        self.garagem = 'Não'
        self.crianca = 'n'
        self.adicional_quartos = 0.0
        self.adicional_garagem = 0.0
        self.desconto = 0.0

    def perguntar_opcionais(self):
        """Cada subclasse (Apartamento, Casa, Estúdio) define suas
        próprias perguntas. Por isso essa classe base não implementa
        nada aqui - só serve de 'contrato' para as filhas."""
        raise NotImplementedError

    def valor_mensal(self):
        """Aluguel final: base + adicionais - desconto."""
        return self.valor_base + self.adicional_quartos + self.adicional_garagem - self.desconto

    @property
    def tipo(self):
        """O tipo é o nome da própria classe (Apartamento, Casa, Estudio)."""
        return type(self).__name__


class Apartamento(Imovel):
    ADICIONAL_QUARTO = 200.00
    ADICIONAL_GARAGEM = 300.00
    DESCONTO_SEM_CRIANCA = 0.05

    def perguntar_opcionais(self):
        if perguntar_sn('Deseja 2 Quartos? (S) Sim | (N) Não: ') == 's':
            self.quartos = '2'
            self.adicional_quartos = self.ADICIONAL_QUARTO

        if perguntar_sn('Deseja vaga de garagem? (S) Sim | (N) Não: ') == 's':
            self.adicional_garagem = self.ADICIONAL_GARAGEM
            self.garagem = 'Sim'

        self.crianca = perguntar_sn('Possui criança? (S) Sim | (N) Não: ')
        if self.crianca == 'n':
            subtotal = self.valor_base + self.adicional_quartos + self.adicional_garagem
            self.desconto = subtotal * self.DESCONTO_SEM_CRIANCA


class Casa(Imovel):
    ADICIONAL_QUARTO = 250.00
    ADICIONAL_GARAGEM = 300.00

    def perguntar_opcionais(self):
        if perguntar_sn('Deseja 2 Quartos? (S) Sim | (N) Não: ') == 's':
            self.quartos = '2'
            self.adicional_quartos = self.ADICIONAL_QUARTO

        if perguntar_sn('Deseja vaga de garagem? (S) Sim | (N) Não: ') == 's':
            self.adicional_garagem = self.ADICIONAL_GARAGEM
            self.garagem = 'Sim'


class Estudio(Imovel):
    ESTACIONAMENTO_BASE = 250.00  # já inclui 2 vagas
    VAGA_EXTRA = 60.00

    def perguntar_opcionais(self):
        if perguntar_sn('Deseja estacionamento? (S) Sim | (N) Não: ') == 's':
            self.garagem = 'Sim'
            vagas_extras = self._perguntar_vagas_extras()
            self.adicional_garagem = self.ESTACIONAMENTO_BASE + vagas_extras * self.VAGA_EXTRA

    def _perguntar_vagas_extras(self):
        while True:
            try:
                vagas = int(input('Quantas vagas extras deseja adicionar? '))
                if vagas >= 0:
                    return vagas
                print('Digite um número igual ou maior que zero.')
            except ValueError:
                print('Digite apenas números inteiros.')


# ----------------------------------------------------------
# CLASSE CONTRATO
# ----------------------------------------------------------

class Contrato:
    VALOR = 2000.00
    FORMAS_PAGAMENTO = {
        'B': 'Boleto',
        'P': 'Pix',
        'D': 'Débito em Conta',
        'CC': 'Cartão de Crédito',
    }

    def __init__(self):
        self.forma_pagamento = None
        self.n_parcelas = None
        self.valor_parcela = None

    def escolher_forma_pagamento(self):
        while True:
            opcao = input('''
Selecione a forma de pagamento do contrato:
(B)  - Boleto
(P)  - Pix
(D)  - Débito em Conta
(CC) - Cartão de Crédito
Digite a opção desejada: ''').strip().upper()

            if opcao in self.FORMAS_PAGAMENTO:
                self.forma_pagamento = self.FORMAS_PAGAMENTO[opcao]
                return

            print('Opção inválida! Escolha B, P, D ou CC.')

    def escolher_parcelamento(self):
        while True:
            try:
                n = int(input('Digite a quantidade de parcelas do contrato (1 a 5): '))
                if 1 <= n <= 5:
                    self.n_parcelas = n
                    self.valor_parcela = self.VALOR / n
                    return
                print('Digite um número entre 1 e 5.')
            except ValueError:
                print('Digite apenas números.')

    def descricao_parcelamento(self):
        return f'{self.n_parcelas}x de R$ {fmt(self.valor_parcela)}'


# ----------------------------------------------------------
# CLASSE ORÇAMENTO
# ----------------------------------------------------------
# Junta cliente + imóvel escolhido + contrato, e sabe como
# exibir o resumo e exportar tudo para CSV.
# ----------------------------------------------------------

class Orcamento:
    def __init__(self, cliente, imovel, contrato):
        self.cliente = cliente
        self.imovel = imovel
        self.contrato = contrato
        self.data = datetime.date.today()

    def valor_total(self):
        return self.imovel.valor_mensal() + self.contrato.VALOR

    def valor_mensal_com_parcela(self):
        return self.imovel.valor_mensal() + self.contrato.valor_parcela

    def exibir_resumo(self):
        imovel = self.imovel
        contrato = self.contrato

        print('\n=========== RESUMO DO ORÇAMENTO ===========')
        print(f'Cliente: {self.cliente}')
        print(f'Imóvel: {imovel.codigo} - {imovel.tipo}')
        print(f'Localização: {imovel.localizacao}')
        print(f'Metragem: {imovel.metragem} | Banheiros: {imovel.banheiros} | Quartos: {imovel.quartos}')
        print(f'Aluguel base: R$ {imovel.valor_base:.2f}')
        if imovel.adicional_quartos:
            print(f'Adicional quartos: R$ {imovel.adicional_quartos:.2f}')
        if imovel.adicional_garagem:
            print(f'Adicional garagem/estacionamento: R$ {imovel.adicional_garagem:.2f}')
        if imovel.desconto:
            print(f'Desconto (sem criança): -R$ {imovel.desconto:.2f}')
        print(f'Aluguel mensal (pago à parte, todo mês): R$ {imovel.valor_mensal():.2f}')
        print(f'Contrato imobiliário (parcelável): R$ {contrato.VALOR:.2f}')
        print(f'Forma de pagamento do contrato: {contrato.forma_pagamento}')
        print(f'Parcelamento do contrato: {contrato.descricao_parcelamento()}')
        print(f'Valor mensal enquanto durar o parcelamento (aluguel + parcela do contrato): '
              f'R$ {self.valor_mensal_com_parcela():.2f}')
        print(f'Total geral (aluguel + contrato): R$ {self.valor_total():.2f}')

    def exportar_csv(self, caminho='orcamento_aluguel.csv'):
        imovel = self.imovel
        contrato = self.contrato

        with open(caminho, 'w', newline='', encoding='utf-8-sig') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')

            escritor.writerow(['R.M IMOBILIÁRIA - ORÇAMENTO DE LOCAÇÃO'])
            escritor.writerow([])

            escritor.writerow(['Data', self.data.strftime('%d/%m/%Y')])
            escritor.writerow(['Cliente', self.cliente])
            escritor.writerow(['Tipo de Imóvel', imovel.tipo])
            escritor.writerow(['Código do Imóvel', imovel.codigo])
            escritor.writerow(['Localização', imovel.localizacao])
            escritor.writerow(['Metragem', imovel.metragem])
            escritor.writerow(['Quartos', imovel.quartos])
            escritor.writerow(['Banheiros', imovel.banheiros])
            escritor.writerow(['Vaga de Garagem', imovel.garagem])
            escritor.writerow(['Possui Criança', imovel.crianca])
            escritor.writerow(['Forma de Pagamento do Contrato', contrato.forma_pagamento])
            escritor.writerow(['Parcelamento do Contrato', contrato.descricao_parcelamento()])
            escritor.writerow([])

            escritor.writerow(['DESCRIÇÃO', 'VALOR (R$)'])
            escritor.writerow(['Aluguel Base', fmt(imovel.valor_base)])
            escritor.writerow(['Adicional de 2 Quartos', fmt(imovel.adicional_quartos)])
            escritor.writerow(['Vaga de Garagem', fmt(imovel.adicional_garagem)])
            escritor.writerow(['Desconto de 5%', fmt(imovel.desconto)])
            escritor.writerow(['Valor do Aluguel Mensal', fmt(imovel.valor_mensal())])
            escritor.writerow(['Valor do Contrato', fmt(contrato.VALOR)])
            escritor.writerow([])

            escritor.writerow(['CRONOGRAMA DAS 12 PARCELAS'])
            escritor.writerow(['Parcela', 'Vencimento', 'Valor (R$)'])

            for mes in range(1, 13):
                if mes <= contrato.n_parcelas:
                    valor_mes = imovel.valor_mensal() + contrato.valor_parcela
                else:
                    valor_mes = imovel.valor_mensal()
                vencimento = somar_meses(self.data, mes)
                escritor.writerow([mes, vencimento.strftime('%d/%m/%Y'), fmt(valor_mes)])

        print(f"\nArquivo '{caminho}' gerado com sucesso!")


# ----------------------------------------------------------
# CADASTRO DE IMÓVEIS (BAHIA)
# ----------------------------------------------------------
# Cada linha guarda a CLASSE que deve ser instanciada (Apartamento,
# Casa ou Estudio) junto com os dados fixos daquele imóvel.
# ----------------------------------------------------------

CADASTRO_IMOVEIS = {
    'AP01': (Apartamento, 'Av. Oceânica, 1450 - Barra - Salvador/BA', '68 m²', 1, 700.00),
    'AP02': (Apartamento, 'Rua Amazonas, 320 - Pituba - Salvador/BA', '74 m²', 2, 700.00),
    'AP03': (Apartamento, 'Alameda dos Sombreiros, 210 - Caminho das Árvores - Salvador/BA', '82 m²', 2, 700.00),

    'CS01': (Casa, 'Rua Praia de Itapuã, 55 - Vilas do Atlântico - Lauro de Freitas/BA', '110 m²', 2, 900.00),
    'CS02': (Casa, 'Rua das Mangueiras, 310 - Centro - Camaçari/BA', '128 m²', 2, 900.00),
    'CS03': (Casa, 'Av. Getúlio Vargas, 890 - Centro - Feira de Santana/BA', '145 m²', 3, 900.00),

    'ES01': (Estudio, 'Rua Fonte do Boi, 120 - Rio Vermelho - Salvador/BA', '32 m²', 1, 1200.00),
    'ES02': (Estudio, 'Av. Oceânica, 2780 - Ondina - Salvador/BA', '36 m²', 1, 1200.00),
    'ES03': (Estudio, 'Av. Olívia Flores, 980 - Candeias - Vitória da Conquista/BA', '40 m²', 1, 1200.00),
}


# ----------------------------------------------------------
# PROGRAMA PRINCIPAL
# ----------------------------------------------------------

def main():
    cliente = input('Digite o nome do cliente: ')

    print('\n=========== IMÓVEIS DISPONÍVEIS ===========')
    for codigo, (classe, localizacao, metragem, banheiros, valor_base) in CADASTRO_IMOVEIS.items():
        print(f'{codigo} - {classe.__name__} | {localizacao} | {metragem} | R$ {valor_base:.2f}')

    codigo_imovel = input('\nDigite o código do imóvel desejado: ').strip().upper()
    while codigo_imovel not in CADASTRO_IMOVEIS:
        print('Código de imóvel inválido! Tente novamente.')
        codigo_imovel = input('Digite o código do imóvel desejado: ').strip().upper()

    classe, localizacao, metragem, banheiros, valor_base = CADASTRO_IMOVEIS[codigo_imovel]

    # Aqui a classe certa (Apartamento, Casa ou Estudio) é instanciada
    # automaticamente, e cada uma sabe fazer as perguntas certas
    # sozinha - isso é polimorfismo.
    imovel = classe(codigo_imovel, localizacao, metragem, banheiros, valor_base)
    imovel.perguntar_opcionais()

    contrato = Contrato()
    contrato.escolher_forma_pagamento()
    contrato.escolher_parcelamento()

    orcamento = Orcamento(cliente, imovel, contrato)
    orcamento.exibir_resumo()
    orcamento.exportar_csv()


if __name__ == '__main__':
    main()