import random


def gerar_populacao(populacao_inicial, itens, capacidade_caminhao):
    populacao = []
    populacao_tamanho = 0

    while populacao_tamanho < populacao_inicial:
        dna = []

        for _ in itens:
            dna.append(random.getrandbits(1))

        if valida_dna(dna, capacidade_caminhao, itens):
            populacao.append(dna)
            populacao_tamanho += 1

    return populacao


def valida_dna(dna, capacidade, itens):
    fitness = 0

    for index, gene in enumerate(dna):
        if gene == 1:
            fitness += itens[index]

    if capacidade < fitness:
        return False

    return True


def calcula_fitness(populacao, itens):
    fitness = []
    for dna in populacao:
        avaliacao = 0
        for index, gene in enumerate(dna):
            if gene == 1:
                avaliacao += itens[index]

        fitness.append(avaliacao)

    return fitness


def roleta(fitness, total_vencedores):
    fitness.sort(reverse=True)
    vencedor = 0
    sorteado = []

    while vencedor < total_vencedores:
        acumulado = []
        valor_acumulado = 0

        for index, nota in enumerate(fitness):
            if nota:
                valor_acumulado = valor_acumulado + nota
                acumulado.insert(index, valor_acumulado)
            else:
                acumulado.insert(index, False)

        valor_sorteado = random.randrange(0, valor_acumulado)

        for index, nota in enumerate(acumulado):
            if nota > valor_sorteado:
                sorteado.append(index)
                fitness[index] = False
                break

        vencedor = vencedor + 1

    return sorteado


def evoluir_geracao(populacao, selecionados, taxa_mutacao):
    nova_geracao = []
    nova_populacao = []

    for selecionado in selecionados:
        nova_geracao.append(populacao[selecionado])

    individuo = 0

    while individuo < len(nova_geracao):
        genes = 0
        filho1 = []
        filho2 = []

        dna_pai = nova_geracao[individuo]
        dna_mae = nova_geracao[individuo + 1]

        while genes <= random.randrange(0, len(dna_pai)):
            filho1.append(dna_pai[genes])
            filho2.append(dna_mae[genes])
            genes = genes + 1

        while genes < len(dna_mae):
            filho1.append(dna_mae[genes])
            filho2.append(dna_pai[genes])
            genes = genes + 1

        filho1 = mutacao(filho1, taxa_mutacao)
        filho2 = mutacao(filho2, taxa_mutacao)
        nova_populacao.append(filho1)
        nova_populacao.append(filho2)
        individuo = individuo + 2

    return nova_populacao


def mutacao(dna, taxa_mutacao):
    sorteio_mutacao = random.randrange(0, 100)

    if sorteio_mutacao <= taxa_mutacao:
        gene_mutacao = random.randrange(0, len(dna) - 1)
        gene = dna[gene_mutacao]

        if gene == 1:
            dna[gene_mutacao] = 0
        else:
            dna[gene_mutacao] = 1

    return dna


def gera_itens(quantidade, menor, maior):
    itens = []
    i = 0
    while i < quantidade:
        itens.append(random.randrange(menor, maior))
        i += 1

    return itens


def gera_dna_visual(melhor_dna):
    dna_final = ""
    for gene in melhor_dna:
        dna_final += str(gene)

    return dna_final
