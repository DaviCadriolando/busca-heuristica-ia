class MotorBuscaHeuristica:

    def __init__(self, grafo, heuristicas, custos_g=None):
        self.grafo = grafo
        self.heuristicas = heuristicas
        self.custos_g = custos_g or {}

    def obter_hn(self, estado):
        return self.heuristicas.get(
            estado,
            float('inf')
        )

    def obter_custo_aresta(self, origem, destino):

        if (origem, destino) in self.custos_g:
            return self.custos_g[(origem, destino)]

        return self.grafo.get(
            origem,
            {}
        ).get(destino, 0)

    def selecionar_melhor_candidato(self, candidatos):

        return sorted(
            candidatos,
            key=lambda c: (
                self.obter_hn(c['estado']),
                c['g'],
                c['estado']
            )
        )[0]

    def expandir_vizinhos(
        self,
        no_atual,
        visitados
    ):

        novos_candidatos = []

        estado_atual = no_atual['estado']

        vizinhos = self.grafo.get(
            estado_atual,
            {}
        )

        for vizinho, custo_aresta in vizinhos.items():

            if vizinho not in visitados:

                g_acumulado = (
                    no_atual['g']
                    + custo_aresta
                )

                novos_candidatos.append({
                    'estado': vizinho,
                    'g': g_acumulado,
                    'pai': no_atual,
                    'caminho':
                        no_atual['caminho']
                        + [vizinho]
                })

        return novos_candidatos


# ============================================================
# GRAFO DO PROJETO
# ============================================================

grafo_mapa = {

    'Base de Atendimento': {
        'Shopping': 4,
        'Universidade': 1,
        'Terminal': 5
    },

    'Shopping': {
        'Base de Atendimento': 4,
        'Parque': 3,
        'Centro': 10
    },

    'Universidade': {
        'Base de Atendimento': 1,
        'Centro': 2
    },

    'Terminal': {
        'Base de Atendimento': 5,
        'Centro': 4,
        'Ponte': 3
    },

    'Parque': {
        'Shopping': 3,
        'Hospital Central': 3,
        'Centro': 2
    },

    'Centro': {
        'Shopping': 10,
        'Universidade': 2,
        'Terminal': 4,
        'Parque': 2,
        'Hospital Central': 4,
        'Rodoviária': 3,
        'Ponte': 4
    },

    'Ponte': {
        'Terminal': 3,
        'Centro': 4,
        'Rodoviária': 3,
        'Aeroporto': 6
    },

    'Hospital Central': {
        'Parque': 3,
        'Centro': 4,
        'Rodoviária': 2
    },

    'Rodoviária': {
        'Hospital Central': 2,
        'Centro': 3,
        'Ponte': 3
    },

    'Aeroporto': {}
}


heuristicas_originais = {

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