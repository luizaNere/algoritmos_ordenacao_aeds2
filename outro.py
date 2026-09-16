"""
texto
"""

import time
import random


# 1. ALGORITMOS DE ORDENACAO
"""
Insertion Sort:
    Faz ordenação in-place (modifica a propria lista recebida).
    Ideia: a cada passo, pega o elemento da posicao i e "insere"
    ele na posicao correta dentro da parte ja ordenada (posicoes
    0 ate i-1), empurrando os elementos maiores uma casa para a direita.
"""
def insertion_sort(lista):
    
    n = len(lista)

    for i in range(1, n):
        chave = lista[i]      # elemento que vamos posicionar corretamente
        j = i - 1

        # enquanto houver elemento anterior maior que 'chave',
        # empurra ele uma posicao para a direita
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j = j - 1

        # posicao correta encontrada para 'chave'
        arr[j + 1] = chave

    return arr


def particionar(arr, inicio, fim):
    """
    Funcao auxiliar do quick_sort.

    Escolhe o ultimo elemento do intervalo [inicio, fim] como pivo
    e reorganiza a lista de forma que:
        - a esquerda do pivo fiquem so elementos menores ou iguais a ele
        - a direita fiquem so elementos maiores que ele

    Retorna a posicao final do pivo (ja ordenado corretamente).
    """
    pivo = arr[fim]
    i = inicio - 1   # marca o limite da regiao "menores que o pivo"

    for j in range(inicio, fim):
        if arr[j] <= pivo:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]   # troca de posicao

    # coloca o pivo na posicao correta (entre menores e maiores)
    arr[i + 1], arr[fim] = arr[fim], arr[i + 1]

    return i + 1   # posicao final do pivo


def quick_sort(arr, inicio=0, fim=None):
    """
    Ordena a lista 'arr' in-place, usando o metodo "dividir para conquistar".

    Passo a passo:
        1. Escolhe um pivo e particiona a lista em torno dele
           (funcao 'particionar' acima).
        2. Chama quick_sort recursivamente para a parte da esquerda do pivo.
        3. Chama quick_sort recursivamente para a parte da direita do pivo.
    """
    # na primeira chamada, 'fim' ainda nao foi definido
    if fim is None:
        fim = len(arr) - 1

    if inicio < fim:
        pos_pivo = particionar(arr, inicio, fim)

        quick_sort(arr, inicio, pos_pivo - 1)   # ordena a parte da esquerda
        quick_sort(arr, pos_pivo + 1, fim)      # ordena a parte da direita

    return arr


# =========================================================
# 2. DADOS DE TESTE
# =========================================================

def gerar_dados_pequenos():
    """Gera uma lista com 100 numeros aleatorios (cenario n <= 100)."""
    random.seed(42)  # sempre gera os mesmos numeros, para poder repetir o teste
    dados = []
    for _ in range(100):
        dados.append(random.randint(0, 100_000))
    return dados


def gerar_dados_grandes():
    """Gera uma lista com 15.000 numeros aleatorios (cenario n >= 10.000)."""
    random.seed(42)
    dados = []
    for _ in range(15_000):
        dados.append(random.randint(0, 100_000))
    return dados


def gerar_dados_parcialmente_ordenados():
    """
    Gera uma lista de 0 a 4999 ja em ordem crescente e depois
    embaralha so uma pequena parte dela (5%), simulando uma
    lista "quase pronta".
    """
    random.seed(42)
    n = 5000
    dados = list(range(n))   # lista ja ordenada: 0, 1, 2, ..., 4999

    qtd_trocas = int(n * 0.05)   # 5% do tamanho da lista
    for _ in range(qtd_trocas):
        pos1 = random.randint(0, n - 1)
        pos2 = random.randint(0, n - 1)
        dados[pos1], dados[pos2] = dados[pos2], dados[pos1]

    return dados


# =========================================================
# 3. TESTE DE DESEMPENHO
# =========================================================

def medir_tempo(funcao_ordenacao, dados_originais):
    """
    Mede quanto tempo 'funcao_ordenacao' leva para ordenar uma
    COPIA de 'dados_originais'.

    Por que uma copia? Porque insertion_sort e quick_sort alteram
    a propria lista que recebem (in-place). Se nao copiassemos,
    o primeiro algoritmo testado deixaria a lista ja ordenada,
    e o segundo algoritmo testaria em cima de dados errados
    (nao seria uma comparacao justa).

    'dados_originais[:]' cria uma copia simples da lista
    (equivalente a list(dados_originais)).
    """
    copia = dados_originais[:]

    inicio = time.time()
    funcao_ordenacao(copia)
    fim = time.time()

    tempo_gasto = fim - inicio
    ordenou_certo = (copia == sorted(dados_originais))

    return tempo_gasto, ordenou_certo


def rodar_cenario(nome, dados):
    print("\n" + "=" * 55)
    print(f"CENARIO: {nome} (n = {len(dados)})")
    print("=" * 55)

    tempo_insertion, certo_insertion = medir_tempo(insertion_sort, dados)
    tempo_quick, certo_quick = medir_tempo(quick_sort, dados)

    print(f"Insertion Sort: {tempo_insertion:.6f} s  (correto: {certo_insertion})")
    print(f"Quick Sort:     {tempo_quick:.6f} s  (correto: {certo_quick})")


def main():
    dados_pequenos = gerar_dados_pequenos()
    dados_grandes = gerar_dados_grandes()
    dados_parciais = gerar_dados_parcialmente_ordenados()

    rodar_cenario("Dados pequenos", dados_pequenos)
    rodar_cenario("Dados grandes", dados_grandes)
    rodar_cenario("Dados parcialmente ordenados", dados_parciais)


if __name__ == "__main__":
    main()
