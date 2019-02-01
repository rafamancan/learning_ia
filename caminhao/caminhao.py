import genetica
from prettytable import PrettyTable
import sys


def progress(count, total, suffix=''):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '█' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


print('Algoritmo genetico\n\n')

# parametros iniciais
geracoes = 5000
menor_item = 1
maior_item = 7
taxa_mutacao = 5
taxa_evolucao = 20
quantidade_itens = 50
populacao_inicial = 1000
capacidade_caminhao = 150

tabela_parametros = PrettyTable(
    [
        "Gerações",
        "Taxa de mutação",
        "Taxa de sobrevivência na evolução",
        "População inicial",
        "Capacidade do caminhão"
    ]
)

tabela_parametros.add_row(
    [
        geracoes,
        str(taxa_mutacao) + '%',
        str(taxa_evolucao) + '%',
        populacao_inicial,
        capacidade_caminhao
    ]
)

print(tabela_parametros)

print('Gerando itens aleatoriamente...')
itens = genetica.gera_itens(quantidade_itens, menor_item, maior_item)

print('Gerando população aleatoriamente...')
populacao = genetica.gerar_populacao(
    populacao_inicial,
    itens,
    capacidade_caminhao
)

print('Iniciando evolução...\n\n')
melhor_geracao = 0
melhor_geracao_valor = 0
melhor_dna = []
geracao = 1
while geracao <= geracoes:
    progress(geracao, geracoes, 'Completo')
    fitness = genetica.calcula_fitness(populacao, itens)
    for index, dna in enumerate(populacao):
        # removendo dnas que passaram da capacidade do caminhão
        if int(fitness[index]) > int(capacidade_caminhao):
            del populacao[index]
            del fitness[index]
        # classificando dna com melhor avaliacao
        elif fitness[index] > melhor_geracao_valor:
            melhor_geracao_valor = fitness[index]
            melhor_geracao = geracao
            melhor_dna = populacao[index]

    geracao += 1
    sobreviventes = int((len(populacao) * taxa_evolucao) / 100)

    # corrige se sobreviventes for ímpar
    if sobreviventes % 2 > 0:
        sobreviventes += 1

    # se sobreviventes for menor que 1 casal, gera população novamente
    if sobreviventes < 2:
        populacao = genetica.gerar_populacao(
            populacao_inicial,
            itens,
            capacidade_caminhao
        )
        sobreviventes = int((len(populacao) * taxa_evolucao) / 100)
        fitness = genetica.calcula_fitness(populacao, itens)

    sorteados = genetica.roleta(fitness, sobreviventes)
    populacao = genetica.evoluir_geracao(populacao, sorteados, taxa_mutacao)

print('Preparando dados para exibição...\n\n')
tabela = PrettyTable(["Melhor Geração", "Fitness", "Maior Fitness possível"])
tabela.add_row([melhor_geracao, melhor_geracao_valor, capacidade_caminhao])

tabela_dna = PrettyTable(["DNA"])
tabela_dna.add_row([genetica.gera_dna_visual(melhor_dna)])

print(tabela.get_string(title="Resultados"))
print(tabela_dna)
