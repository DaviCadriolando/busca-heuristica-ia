class MotorBuscaHeuristica:
    def __init__(self, grafo, heuristicas, custos_g=None):
        """
        Inicializa o motor de busca heurística.
        """
        self.grafo = grafo
        self.heuristicas = heuristicas
        self.custos_g = custos_g or {}

    def obter_hn(self, estado):
        """Retorna o valor heurístico h(n) do estado."""
        return self.heuristicas.get(estado, float('inf'))

    def selecionar_melhor_candidato(self, candidatos):
        """
        Critérios de Prioridade:
        1. Menor h(n) (Busca Gulosa)
        2. Menor g(n) (Desempate por custo acumulado real)
        3. Ordem alfabética do nome do estado (Desempate secundário)
        """
        return sorted(
            candidatos,
            key=lambda c: (
                self.obter_hn(c['estado']),
                c['g'],
                c['estado']
            )
        )[0]

    def expandir_vizinhos(self, no_atual, visitados):
        """
        Gera a lista de novos nós vizinhos adicionando o ponteiro 'pai' para reconstrução.
        """
        novos_candidatos = []
        estado_atual = no_atual['estado']
        vizinhos = self.grafo.get(estado_atual, [])

        for vizinho in vizinhos:
            if vizinho not in visitados:
                custo_aresta = self.custos_g.get((estado_atual, vizinho), 0)
                g_acumulado = no_atual['g'] + custo_aresta
                
                novos_candidatos.append({
                    'estado': vizinho,
                    'g': g_acumulado,
                    'pai': no_atual,  # Referência ao nó predecessor/pai
                    'caminho': no_atual['caminho'] + [vizinho]
                })

        return novos_candidatos

    def buscar(self, origem, destino, verbose=True):
        """
        Executa a busca heurística com relatório em tela e retorno estruturado de dados.
        """
        no_inicial = {
            'estado': origem,
            'g': 0,
            'pai': None,
            'caminho': [origem]
        }
        
        fronteira = [no_inicial]
        visitados = set()
        ordem_visita = []
        estados_expandidos = []
        etapa = 1

        no_atual = no_inicial

        while no_atual:
            estado_atual = no_atual['estado']
            
            # Registra visita
            visitados.add(estado_atual)
            ordem_visita.append(estado_atual)

            # Verificação de Objetivo
            if estado_atual == destino:
                if verbose:
                    print(f"=== ETAPA {etapa} ===")
                    print(f"Estado expandido: {estado_atual}")
                    print(f"\n🎯 OBJETIVO ATINGIDO: {estado_atual}")
                    print("=" * 45 + "\n")

                # Retorno completo de dados solicitados pelo professor
                return {
                    'caminho_encontrado': no_atual['caminho'],
                    'custo_total_g': no_atual['g'],
                    'ordem_visita': ordem_visita,
                    'estados_expandidos': estados_expandidos,
                    'qtd_visitados': len(ordem_visita),
                    'qtd_expandidos': len(estados_expandidos),
                    'no_final': no_atual
                }

            # Remove o nó atual da fronteira de candidatos
            fronteira = [c for c in fronteira if c['estado'] != estado_atual]

            # Registro de expansão e geração de vizinhos
            estados_expandidos.append(estado_atual)
            novos = self.expandir_vizinhos(no_atual, visitados)

            # Adiciona novos candidatos à fronteira sem duplicar estados já presentes
            for n in novos:
                if not any(c['estado'] == n['estado'] for c in fronteira):
                    fronteira.append(n)

            # Saída de histórico/logs para acompanhamento
            if verbose:
                print(f"=== ETAPA {etapa} ===")
                print(f"Estado expandido: {estado_atual}")
                
                print("\nNovos candidatos:")
                if novos:
                    for n in novos:
                        hn = self.obter_hn(n['estado'])
                        print(f"- {n['estado']} | h(n) = {hn}")
                else:
                    print("- Nenhum novo candidato gerado")

                print("\nCandidatos disponíveis:")
                fronteira_ordenada = sorted(
                    fronteira,
                    key=lambda c: (self.obter_hn(c['estado']), c['g'], c['estado'])
                )
                for c in fronteira_ordenada:
                    hn = self.obter_hn(c['estado'])
                    print(f"- {c['estado']} | h(n) = {hn}")

            # Seleção do próximo candidato pela fronteira
            if fronteira:
                proximo_no = self.selecionar_melhor_candidato(fronteira)
                if verbose:
                    print(f"\nPróximo escolhido: {proximo_no['estado']}\n")
                no_atual = proximo_no
            else:
                if verbose:
                    print("\nFronteira vazia. Nenhum caminho encontrado.\n")
                return None

            etapa += 1


            # Estrutura de Grafo esperada pelo seu código (Grafo com custos embutidos)
grafo_mapa = {
    'Base de Atendimento': {'Shopping': 4, 'Universidade': 1, 'Terminal': 5},
    'Shopping': {'Base de Atendimento': 4, 'Parque': 3, 'Centro': 10},
    'Universidade': {'Base de Atendimento': 1, 'Centro': 2},
    'Terminal': {'Base de Atendimento': 5, 'Centro': 4, 'Ponte': 3},
    'Parque': {'Shopping': 3, 'Hospital Central': 3, 'Centro': 2},
    'Centro': {'Shopping': 10, 'Universidade': 2, 'Terminal': 4, 'Parque': 2, 'Hospital Central': 4, 'Rodoviária': 3, 'Ponte': 4},
    'Ponte': {'Terminal': 3, 'Centro': 4, 'Rodoviária': 3, 'Aeroporto': 6},
    'Hospital Central': {'Parque': 3, 'Centro': 4, 'Rodoviária': 2},
    'Rodoviária': {'Hospital Central': 2, 'Centro': 3, 'Ponte': 3},
    'Aeroporto': {}
}

# Tabela de Heurísticas h(n) Original
heuristicas_original = {
    'Base de Atendimento': 5,
    'Shopping': 11,
    'Universidade': 15,
    'Terminal': 11,
    'Parque': 19,
    'Centro': 12,
    'Ponte': 14,
    'Hospital Central': 0,
    'Rodoviária': 29,
    'Aeroporto': 5
}

# Execução do Motor
motor = MotorBuscaHeuristica(grafo=grafo_mapa, heuristicas=heuristicas_original)
resultado = motor.buscar('Base de Atendimento', 'Hospital Central', verbose=True)