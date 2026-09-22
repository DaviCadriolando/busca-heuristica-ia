from main import MotorBuscaHeuristica


class GestorDeEstados(MotorBuscaHeuristica):

    def __init__(self, grafo, heuristicas):
        super().__init__(grafo, heuristicas)

        self.visitados = set()
        self.expandidos = []
        self.predecessor = {}

    # =========================================================
    # CONTROLE DE VISITADOS ;
    # =========================================================

    def ja_visitado(self, estado):
        return estado in self.visitados

    # =========================================================
    # REGISTRO DO PREDECESSOR
    # =========================================================

    def registrar_predecessor(self, estado, origem_estado):

        if estado not in self.predecessor:
            self.predecessor[estado] = origem_estado

    # =========================================================
    # RECONSTRUÇÃO DO CAMINHO
    # =========================================================

    def reconstruir_caminho(self, origem, destino):

        if destino not in self.predecessor and destino != origem:
            return None

        caminho = [destino]
        atual = destino

        while atual != origem:

            atual = self.predecessor.get(atual)

            if atual is None:
                return None

            caminho.append(atual)

        caminho.reverse()

        return caminho

    # =========================================================
    # BUSCA COM GESTÃO DE ESTADOS
    # =========================================================

    def buscar_com_gestao(
        self,
        origem,
        destino,
        verbose=True
    ):

        # Estado inicial
        no_inicial = {
            'estado': origem,
            'g': 0,
            'pai': None,
            'caminho': [origem]
        }

        # Fronteira
        fronteira = [no_inicial]

        # Ordem dos estados escolhidos
        ordem_visita = []

        while fronteira:

            # -------------------------------------------------
            # Escolhe o melhor candidato
            # -------------------------------------------------

            no_atual = self.selecionar_melhor_candidato(
                fronteira
            )

            fronteira.remove(no_atual)

            estado_atual = no_atual['estado']

            # -------------------------------------------------
            # Verifica se já foi visitado
            # -------------------------------------------------

            if self.ja_visitado(estado_atual):
                continue

            # Registra como visitado
            self.visitados.add(estado_atual)

            ordem_visita.append(estado_atual)

            # -------------------------------------------------
            # Exibe estado escolhido
            # -------------------------------------------------

            if verbose:

                print(
                    f"\n=== Estado escolhido: "
                    f"{estado_atual} ==="
                )

                print(
                    f"h(n) = "
                    f"{self.obter_hn(estado_atual)}"
                )

                print(
                    f"g(n) = "
                    f"{no_atual['g']}"
                )

            # -------------------------------------------------
            # Verifica objetivo
            # -------------------------------------------------

            if estado_atual == destino:

                caminho_final = self.reconstruir_caminho(
                    origem,
                    destino
                )

                if verbose:

                    print(
                        "\n OBJETIVO ATINGIDO!"
                    )

                    print(
                        "\nOrdem de visita:"
                    )

                    print(
                        " -> ".join(ordem_visita)
                    )

                    print(
                        "\nEstados expandidos:"
                    )

                    print(
                        " -> ".join(self.expandidos)
                    )

                    print(
                        "\nCaminho final:"
                    )

                    print(
                        " -> ".join(caminho_final)
                    )

                return {
                    'ordem_visita': ordem_visita,
                    'expandidos': self.expandidos,
                    'caminho_final': caminho_final,
                    'qtd_visitados': len(
                        self.visitados
                    ),
                    'qtd_expandidos': len(
                        self.expandidos
                    ),
                    'custo_total': no_atual['g']
                }

            # -------------------------------------------------
            # Expande o estado atual
            # -------------------------------------------------

            self.expandidos.append(
                estado_atual
            )

            novos = self.expandir_vizinhos(
                no_atual,
                self.visitados
            )

            candidatos_novos = []

            # -------------------------------------------------
            # Processa os novos candidatos
            # -------------------------------------------------

            for candidato in novos:

                vizinho = candidato['estado']

                # Ignora estados já visitados
                if self.ja_visitado(vizinho):
                    continue

                # Registra predecessor
                self.registrar_predecessor(
                    vizinho,
                    estado_atual
                )

                # Evita duplicação na fronteira
                if not any(
                    c['estado'] == vizinho
                    for c in fronteira
                ):

                    fronteira.append(
                        candidato
                    )

                    candidatos_novos.append(
                        candidato
                    )

            # -------------------------------------------------
            # Exibe novos candidatos
            # -------------------------------------------------

            if verbose:

                print(
                    "\nNovos candidatos:"
                )

                if candidatos_novos:

                    for candidato in candidatos_novos:

                        estado = candidato['estado']

                        print(
                            f"- {estado} | "
                            f"h(n) = "
                            f"{self.obter_hn(estado)} | "
                            f"g(n) = "
                            f"{candidato['g']}"
                        )

                else:

                    print(
                        "- Nenhum novo candidato"
                    )

                # ---------------------------------------------
                # Candidatos disponíveis
                # ---------------------------------------------

                print(
                    "\nCandidatos disponíveis:"
                )

                candidatos_ordenados = sorted(
                    fronteira,
                    key=lambda c: (
                        self.obter_hn(
                            c['estado']
                        ),
                        c['g'],
                        c['estado']
                    )
                )

                for candidato in candidatos_ordenados:

                    estado = candidato['estado']

                    print(
                        f"- {estado} | "
                        f"h(n) = "
                        f"{self.obter_hn(estado)} | "
                        f"g(n) = "
                        f"{candidato['g']}"
                    )

        # -----------------------------------------------------
        # Fronteira vazia
        # -----------------------------------------------------

        if verbose:

            print(
                "\nFronteira vazia."
            )

            print(
                "Destino inalcançável."
            )

        return None
