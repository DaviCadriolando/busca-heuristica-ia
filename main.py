class MotorBuscaHeuristica:
    def __init__(self, grafo, heuristicas):
        self.grafo = grafo
        self.heuristicas = heuristicas

    def obter_hn(self, estado):
        return self.heuristicas.get(estado, float('inf'))

    def selecionar_melhor_candidato(self, candidatos):
        """
        Seleciona o candidato com menor h(n).

        Desempate:
        1. menor h(n)
        2. menor g(n)
        3. ordem alfabética
        """
        return min(
            candidatos,
            key=lambda candidato: (
                self.obter_hn(candidato['estado']),
                candidato['g'],
                candidato['estado']
            )
        )

    def expandir_vizinhos(self, no_atual):
        """
        Gera os candidatos vizinhos do estado atual.
        """
        novos_candidatos = []

        estado_atual = no_atual['estado']

        for vizinho, custo in self.grafo.get(
            estado_atual, {}
        ).items():

            novo_g = no_atual['g'] + custo

            novos_candidatos.append({
                'estado': vizinho,
                'g': novo_g
            })

        return novos_candidatos

    def buscar(self, origem, destino, verbose=True):

        no_inicial = {
            'estado': origem,
            'g': 0
        }

        fronteira = [no_inicial]
        ordem_selecao = []

        while fronteira:

            # Escolhe o menor h(n)
            no_atual = self.selecionar_melhor_candidato(
                fronteira
            )

            # Remove da fronteira
            fronteira.remove(no_atual)

            estado_atual = no_atual['estado']

            ordem_selecao.append(estado_atual)

            if verbose:
                print(f"\n=== ESTADO ATUAL ===")
                print(f"Estado: {estado_atual}")
                print(f"h(n): {self.obter_hn(estado_atual)}")
                print(f"g(n): {no_atual['g']}")

            # Verifica objetivo
            if estado_atual == destino:

                if verbose:
                    print("\n🎯 OBJETIVO ATINGIDO!")
                    print(f"Destino: {destino}")

                return {
                    'ordem_selecao': ordem_selecao,
                    'no_final': no_atual
                }

            # Expande vizinhos
            novos = self.expandir_vizinhos(no_atual)

            if verbose:
                print("\nNovos candidatos:")

                for candidato in novos:
                    print(
                        f"- {candidato['estado']} | "
                        f"h(n) = "
                        f"{self.obter_hn(candidato['estado'])} | "
                        f"g(n) = {candidato['g']}"
                    )

            # Adiciona candidatos à fronteira
            for candidato in novos:

                if not any(
                    c['estado'] == candidato['estado']
                    for c in fronteira
                ):
                    fronteira.append(candidato)

            # Mostra TODOS os candidatos disponíveis
            if verbose:
                print("\nCandidatos disponíveis:")

                candidatos_ordenados = sorted(
                    fronteira,
                    key=lambda candidato: (
                        self.obter_hn(candidato['estado']),
                        candidato['g'],
                        candidato['estado']
                    )
                )

                for candidato in candidatos_ordenados:
                    print(
                        f"- {candidato['estado']} | "
                        f"h(n) = "
                        f"{self.obter_hn(candidato['estado'])} | "
                        f"g(n) = {candidato['g']}"
                    )

            if not fronteira:
                print("\nFronteira vazia.")
                return None

            proximo = self.selecionar_melhor_candidato(
                fronteira
            )

            if verbose:
                print(
                    f"\nPróximo escolhido: "
                    f"{proximo['estado']}"
                )

        return None