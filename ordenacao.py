"""
Análise de Desempenho: Insertion Sort x Quick Sort

Cenários testados:
    1. Dados pequenos      (n <= 100)
    2. Dados grandes       (n >= 10.000)
    3. Dados parcialmente ordenados (tamanho livre)

- O módulo time é utilizado para a Análise de Complexidade Empírica;
- O módulo random é utilizado para gerar listas de valores aleatórios dentro de um intervalo;
- O módulo copy é utilizado para que os dois algoritmos recebam a MESMA lista como parâmetro,
  pois os dois métodos de ordenação não retornam novas listas, mas ordenam a lista que receberam.
"""

import time
import random
import copy

# DECLARAÇÃO DO INSERTION SORT
def insertion_sort(lista):

    n = len(lista)

    for i in range(1, n):
        chave = lista[i]
        j = i - 1

        # deslocar os elementos maiores que 'chave' uma posição à frente
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1

        lista[j + 1] = chave
    return lista

# DECLARAÇÃO DO QUICK SORT
def quick_sort(lista):
    """
    Quick Sort — retorna uma NOVA lista ordenada (não altera 'arr').
    Usa particionamento com pivô escolhido no meio da lista (reduz o
    risco do pior caso em dados já ordenados, comparado ao pivô fixo).

    Complexidade teórica:
        Melhor/médio caso: O(n log n)
        Pior caso:          O(n^2)   -> partições sempre desbalanceadas
                                         (ex.: pivô sempre o menor/maior elemento)
        Espaço:             O(log n) em média (pilha de recursão);
                             aqui a implementação recursiva com listas
                             novas usa O(n) de espaço auxiliar.
        Estável:            Não (nesta implementação)
    """
    if len(lista) <= 1:
        return lista

    pivo = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivo]
    iguais = [x for x in lista if x == pivo]
    maiores = [x for x in lista if x > pivo]

    return quick_sort(menores) + iguais + quick_sort(maiores)


# 2. FUNÇÕES DE GERAÇÃO DE DADOS ALEATÓRIOS

def gerar_dados_aleatorios(n, limite_inf=0, limite_sup=1_000_000):
    return [random.randint(limite_inf, limite_sup) for _ in range(n)]


def gerar_dados_parcialmente_ordenados(n, fracao_embaralhada=0.1):
    """
    Gera uma lista ordenada de 0..n-1 e embaralha apenas uma fração
    dos elementos (troca pares aleatórios de posição), simulando dados
    'quase ordenados'.
    """
    dados = list(range(n))
    qtd_trocas = max(1, int(n * fracao_embaralhada))
    for _ in range(qtd_trocas):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        dados[i], dados[j] = dados[j], dados[i]
    return dados


# 3. FUNÇÃO DE MEDIÇÃO DE TEMPO

def medir_tempo(func, dados):
    """
    Mede o tempo de execução de 'func' aplicada sobre uma CÓPIA de 'dados',
    para que os dois algoritmos sempre recebam o mesmo conjunto original.
    """
    dados_copia = copy.deepcopy(dados)
    inicio = time.perf_counter()
    resultado = func(dados_copia)
    fim = time.perf_counter()
    tempo_execucao = fim - inicio

    # valida se realmente ordenou corretamente
    ordenado_corretamente = resultado == sorted(dados)
    return tempo_execucao, ordenado_corretamente


# =========================================================
# 4. EXECUÇÃO DOS CENÁRIOS DE TESTE
# =========================================================

def rodar_cenario(nome_cenario, dados):
    print(f"\n{'=' * 60}")
    print(f"CENÁRIO: {nome_cenario}  (n = {len(dados)})")
    print(f"{'=' * 60}")

    tempo_insertion, ok_insertion = medir_tempo(insertion_sort, dados)
    tempo_quick, ok_quick = medir_tempo(quick_sort, dados)

    print(f"Insertion Sort -> tempo: {tempo_insertion:.6f}s | correto: {ok_insertion}")
    print(f"Quick Sort     -> tempo: {tempo_quick:.6f}s | correto: {ok_quick}")

    if tempo_quick > 0:
        proporcao = tempo_insertion / tempo_quick
        print(f"Insertion Sort foi {proporcao:.2f}x mais lento que o Quick Sort"
              if proporcao >= 1 else
              f"Insertion Sort foi {1/proporcao:.2f}x mais rápido que o Quick Sort")

    return tempo_insertion, tempo_quick


def main():
    random.seed(42)  # reprodutibilidade dos testes

    resultados = {}

    # ---- Cenário 1: dados pequenos (n <= 100) ----
    dados_pequenos = gerar_dados_aleatorios(100)
    resultados["Pequeno (n=100)"] = rodar_cenario(
        "Dados pequenos (n <= 100)", dados_pequenos
    )

    # ---- Cenário 2: dados grandes (n >= 10.000) ----
    dados_grandes = gerar_dados_aleatorios(15_000)
    resultados["Grande (n=15000)"] = rodar_cenario(
        "Dados grandes (n >= 10.000)", dados_grandes
    )

    # ---- Cenário 3: dados parcialmente ordenados (tamanho livre) ----
    dados_parciais = gerar_dados_parcialmente_ordenados(5_000, fracao_embaralhada=0.05)
    resultados["Parcialmente ordenado (n=5000)"] = rodar_cenario(
        "Dados parcialmente ordenados (95% já em ordem)", dados_parciais
    )

    # =========================================================
    # 5. RESUMO E ANÁLISE TEÓRICA
    # =========================================================
    print(f"\n{'=' * 60}")
    print("RESUMO DOS TEMPOS (segundos)")
    print(f"{'=' * 60}")
    print(f"{'Cenário':35s}{'Insertion':>12s}{'Quick':>12s}")
    for cenario, (t_ins, t_qs) in resultados.items():
        print(f"{cenario:35s}{t_ins:12.6f}{t_qs:12.6f}")

    print(f"""
{'=' * 60}
ANÁLISE TEÓRICA DE COMPLEXIDADE
{'=' * 60}
Insertion Sort:
    - Melhor caso: O(n)     -> ocorre com dados já ordenados, pois o
      laço interno praticamente não desloca elementos.
    - Caso médio/pior caso: O(n^2) -> cada um dos n elementos pode
      precisar ser comparado/deslocado por até n posições.
    - Por isso é MUITO eficiente em listas pequenas ou quase
      ordenadas (baixo overhead, sem recursão), mas se degrada
      rapidamente quando n cresce.

Quick Sort:
    - Melhor/caso médio: O(n log n) -> a cada partição, o problema é
      dividido em subproblemas de tamanho aproximadamente n/2.
    - Pior caso: O(n^2) -> ocorre quando o pivô escolhido gera
      partições muito desbalanceadas repetidamente (ex.: pivô sempre
      o menor ou maior elemento). Usar o pivô do meio, como nesta
      implementação, reduz bastante essa chance em dados ordenados.
    - Overhead maior que o Insertion Sort para n pequeno (recursão,
      criação de novas listas), mas essa desvantagem desaparece
      rapidamente conforme n cresce.

Conclusão esperada dos testes:
    - n pequeno (n <= 100): a diferença tende a ser mínima, podendo
      o Insertion Sort até vencer, pois o overhead do Quick Sort
      (recursão) pesa mais que o ganho assintótico de O(n log n).
    - n grande (n >= 10.000): o Quick Sort deve vencer com folga,
      já que O(n log n) cresce muito mais devagar que O(n^2).
    - Dados parcialmente ordenados: o Insertion Sort tende a se
      aproximar do seu melhor caso O(n) e pode ser competitivo ou
      até superar o Quick Sort, dependendo do grau de desordem,
      já que o Quick Sort não tem um "atalho" natural para dados
      quase ordenados (a menos que se use uma estratégia adaptativa
      de escolha de pivô).
""")


if __name__ == "__main__":
    main()
