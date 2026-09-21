import heapq




def reconstruir_caminho(pais, origem, destino):
    """
    Reconstrói o caminho final usando o dicionário de predecessores.
    """
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = pais.get(atual)

    caminho.reverse()

    # Verifica se realmente chegou à origem
    if not caminho or caminho[0] != origem:
        return None

    return caminho


def testar_reconstrucao():
    """
    Teste da reconstrução da rota.
    """

    pais = {
        "Base de Atendimento": None,
        "Shopping": "Base de Atendimento",
        "Parque": "Shopping",
        "Hospital Central": "Parque"
    }

    origem = "Base de Atendimento"
    destino = "Hospital Central"

    caminho = reconstruir_caminho(
        pais,
        origem,
        destino
    )

    print("=== TESTE DE RECONSTRUÇÃO ===")

    if caminho:
        print("Caminho reconstruído:")
        print(" -> ".join(caminho))
        print("TESTE PASSOU!")
    else:
        print("Não foi possível reconstruir o caminho.")
        print("TESTE FALHOU!")


def testar_visitados():
    """
    Teste do controle de estados visitados.
    """

    visitados = set()

    estados = [
        "Base de Atendimento",
        "Shopping",
        "Parque",
        "Shopping",
        "Hospital Central"
    ]

    print("\n=== TESTE DE ESTADOS VISITADOS ===")

    for estado in estados:

        if estado in visitados:
            print(f"{estado}: já visitado -> ignorado")
        else:
            visitados.add(estado)
            print(f"{estado}: novo estado -> adicionado")

    print("\nEstados visitados:")
    print(visitados)


def testar_ciclo():
    """
    Teste para verificar se um estado repetido
    é impedido de ser processado novamente.
    """

    visitados = set()

    print("\n=== TESTE DE PREVENÇÃO DE CICLO ===")

    sequencia = [
        "Base de Atendimento",
        "Shopping",
        "Parque",
        "Shopping",
        "Base de Atendimento"
    ]

    for estado in sequencia:

        if estado in visitados:
            print(
                f"{estado}: ciclo/repetição detectado -> não processar"
            )
        else:
            visitados.add(estado)
            print(
                f"{estado}: processado pela primeira vez"
            )


# =========================
# EXECUÇÃO DOS TESTES
# =========================

testar_reconstrucao()
testar_visitados()
testar_ciclo()

def motor_de_busca_heuristica(grafo, heuristica, origem, destino):
    """
    Motor central da Busca Heurística (A*).
    Seleciona o melhor candidato e processa a expansão de vizinhos.
    """
    # A fronteira é uma Min-Heap que armazena tuplos: (f(n), g(n), nome_estado)
    # 1. f(n): Prioridade principal (Pode ser apenas h(n) numa Busca Gulosa)
    # 2. g(n): 1º Critério de desempate (custo acumulado em km)[cite: 1]
    # 3. nome_estado: 2º Critério de desempate (ordem alfabética automática)
    fronteira = []
    
    # f(n) inicial é apenas a heurística da origem (já que g(n) é 0)
    heapq.heappush(fronteira, (heuristica[origem], 0, origem))
    
    # Dicionário de custos g(n) acumulados conhecidos
    custo_g = {origem: 0}
    
    # Integração com a Tarefa 4 (Gestão de Estados)
    visitados = set()
    pais = {origem: None}
    
    while fronteira:
        # 1. Seleção: Remove o candidato com menor f(n) (e resolve empates)
        f_atual, g_atual, atual = heapq.heappop(fronteira)
        
        # Ignora estados já totalmente explorados (prevenção de ciclos da Tarefa 4)
        if atual in visitados:
            continue
            
        visitados.add(atual)
        
        # Teste de objetivo
        if atual == destino:
            print(f"Destino {destino} alcançado com custo {g_atual} km!")
            return pais, g_atual # Retorna a árvore de pais para a Tarefa 4 reconstruir
            
        # 2. Expansão de Vizinhos
        # Itera sobre os caminhos disponíveis no garfo para o estado atual[cite: 1, 2]
        vizinhos_disponiveis = grafo.get(atual, {})
        
        for vizinho, distancia in vizinhos_disponiveis.items():
            # Estado sem saída (ex: Aeroporto) terá um dicionário vazio e não entra no loop[cite: 1, 2]
            novo_custo_g = g_atual + distancia
            
            # Só adiciona à fronteira se for um caminho mais barato ou se o vizinho for novo
            if vizinho not in custo_g or novo_custo_g < custo_g[vizinho]:
                custo_g[vizinho] = novo_custo_g
                
                # Cálculo da heurística + custo real (A*)
                h_vizinho = heuristica.get(vizinho, float('inf'))
                f_vizinho = novo_custo_g + h_vizinho
                
                # Gravação do predecessor (Tarefa 4)
                pais[vizinho] = atual
                
                # Insere na fila de prioridade aplicando as regras de desempate
                heapq.heappush(fronteira, (f_vizinho, novo_custo_g, vizinho))
                
    return None, float('inf') # Caso não haja solução