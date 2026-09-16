"""
Arquivo dividido em 3 partes:

    1. ALGORITMOS DE ORDENACAO   -> funcoes insertion_sort e quick_sort
    2. DADOS DE TESTE            -> funcoes que geram os dados de cada cenario
    3. TESTE DE DESEMPENHO       -> mede o tempo e mostra os resultados

As funcoes de ordenacao nao sabem nada sobre os dados de teste -
elas so recebem uma lista e ordenam. Quem decide QUAIS dados usar
e a parte 2, e quem chama tudo e mede o tempo e a parte 3.
"""

import time
import random

# 1. ALGORITMOS DE ORDENACAO

def insertion_sort(lista):
    """
    Ordena 'lista' IN-PLACE (ou seja, modifica a propria lista
    recebida, não cria uma lista nova).

    Ideia: a cada passo, pega o elemento da posição i e "insere"
    ele na posição correta dentro da parte já ordenada (posições
    0 ate i-1), empurrando os elementos maiores uma casa para a direita.
    """
    n = len(lista)

    for i in range(1, n):
        chave = lista[i]      # elemento que sera posicionado corretamente
        j = i - 1

        # desloca os elementos maiores que 'chave' uma posicao a frente
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j = j - 1

        # posicao correta encontrada para 'chave'
        lista[j + 1] = chave

    return lista   # devolve a mesma lista, ja ordenada


def quick_sort(lista):
    """
    Ordena 'lista' e retorna uma LISTA NOVA ordenada
    (a lista original recebida NÃO é modificada).

    Metodo "dividir para conquistar":
        1. Escolhe um elemento como pivo.
        2. Separa o resto da lista em duas partes: menores que o
           pivo e maiores que o pivo.
        3. Ordena cada parte recursivamente (chamando quick_sort
           de novo) e junta tudo: menores + pivo + maiores.
    """

    # caso base (condicao de parada da recursao): lista com 0 ou 1 já está ordenada por definição
    if len(lista) <= 1:
        return lista

    pivo = lista[len(lista) // 2]

    menores = [x for x in lista if x < pivo]   # elementos MENORES que o pivô
    iguais = [x for x in lista if x == pivo]    # elementos IGUAIS ao pivô
    maiores = [x for x in lista if x > pivo]    # elementos MAIORES que o pivô

    return quick_sort(menores) + iguais + quick_sort(maiores)


# 2. DADOS DE TESTE

def gerar_dados_pequenos():
    # Gera uma lista com 100 numeros aleatorios (cenário n <= 100).

    random.seed(55)  # sempre gera os mesmos numeros, para poder repetir o teste
    dados = []
    for x in range(100): # o 'x' não será utilizado como índice, serve apenas para repetir o for
        dados.append(random.randint(0, 100_000))
        
    return dados


def gerar_dados_grandes():
    # Gera uma lista com 15.000 números aleatórios (cenário n >= 10.000).

    random.seed(55)
    dados = []
    for x in range(15_000):
        dados.append(random.randint(0, 100_000))
    return dados


def gerar_dados_parcialmente_ordenados():
    """
    Gera uma lista de 0 a 4999 ja em ordem crescente e depois
    embaralha so uma pequena parte dela (10%), simulando uma
    lista parcialmente ordenada.
    """
    random.seed(55)
    n = 5000
    dados = list(range(n))   # lista ja ordenada: 0, 1, 2, ..., 4999

    qtd_trocas = int(n * 0.1)   # 10% do tamanho da lista
    for _ in range(qtd_trocas):
        pos1 = random.randint(0, n - 1)
        pos2 = random.randint(0, n - 1)
        dados[pos1], dados[pos2] = dados[pos2], dados[pos1]

    return dados


# 3. TESTE DE DESEMPENHO

def medir_tempo(funcao_ordenacao, dados_originais):
    """
    Mede quanto tempo 'funcao_ordenacao' leva para ordenar uma
    COPIA de 'dados_originais', e confere se o resultado está correto.

    Por que uma copia? Porque nao queremos alterar 'dados_originais',
    ele precisa continuar do jeito que estava para os outros testes.

    IMPORTANTE: o resultado de 'funcao_ordenacao(copia)' precisa ser
    guardado de volta em 'copia'. Isso e necessario porque nem toda
    funcao de ordenacao modifica a lista in-place (o quick_sort,
    por exemplo, retorna uma lista NOVA em vez de alterar a recebida).
    Sem isso, a checagem de "ordenou certo" ficaria errada para o
    quick_sort.
    """
    copia = list(dados_originais)

    inicio = time.process_time()
    copia = funcao_ordenacao(copia)
    fim = time.process_time()

    tempo_gasto = fim - inicio
    ordenou_certo = (copia == sorted(dados_originais))

    return tempo_gasto, ordenou_certo


def testar_cenario(nome, dados):
    # Roda os dois algoritmos sobre o mesmo conjunto de dados e imprime o resultado.
    print("-" * 60)
    print(f"CENARIO: {nome} (n = {len(dados)})\n")

    tempo_insertion, certo_insertion = medir_tempo(insertion_sort, dados)
    tempo_quick, certo_quick = medir_tempo(quick_sort, dados)

    print(f"Insertion Sort: {tempo_insertion:.6f} s  (correto: {certo_insertion})")
    print(f"Quick Sort:     {tempo_quick:.6f} s  (correto: {certo_quick})")
    print()   # linha em branco para separar do proximo cenario


def main():
    dados_pequenos = gerar_dados_pequenos()
    dados_grandes = gerar_dados_grandes()
    dados_parciais = gerar_dados_parcialmente_ordenados()

    testar_cenario("Dados pequenos", dados_pequenos)
    testar_cenario("Dados grandes", dados_grandes)
    testar_cenario("Dados parcialmente ordenados", dados_parciais)


if __name__ == "__main__":
    main()