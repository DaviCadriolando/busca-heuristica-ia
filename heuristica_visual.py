import tkinter as tk

# Layout fixo no canvas, no mesmo esquema do mapa do grupo
# (Base à esquerda, Hospital à direita, Aeroporto embaixo).
POSICOES_PADRAO = {
    "Base de Atendimento": (60, 260),
    "Shopping": (250, 100),
    "Universidade": (250, 260),
    "Terminal": (250, 420),
    "Centro": (450, 260),
    "Parque": (650, 100),
    "Ponte": (450, 420),
    "Rodoviária": (650, 420),
    "Hospital Central": (740, 260),
    "Aeroporto": (650, 530),
}


class ReplayHeuristica:
    def __init__(self, janela, grafo, heuristicas, origem, destino, resultado, posicoes=None):
        self.grafo = grafo
        self.heuristicas = heuristicas
        self.origem = origem
        self.destino = destino
        self.posicoes = posicoes or POSICOES_PADRAO

        self.ordem_visita = resultado["ordem_visita"]
        self.expandidos = set(resultado["expandidos"])
        self.caminho_final = resultado["caminho_final"]
        self.custo_total = resultado["custo_total"]

        self.indice = 0
        self.revelados = []
        self.atual = None
        self.finalizado = False

        self.janela = janela
        self.janela.title("Busca Heurística - Visualização do resultado")

        self.canvas = tk.Canvas(janela, width=800, height=580, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=8, padx=20, pady=20)

        tk.Label(
            janela, text="Busca Heurística",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=1, sticky="w", padx=10)

        self.lbl_passo = tk.Label(janela, text="Passo: 0", font=("Arial", 12, "bold"))
        self.lbl_passo.grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(janela, text="Estado atual:", font=("Arial", 11, "bold")).grid(
            row=2, column=1, sticky="w", padx=10)
        self.lbl_atual = tk.Label(janela, text="-", font=("Arial", 11))
        self.lbl_atual.grid(row=2, column=1, sticky="e", padx=10)

        tk.Label(janela, text="Explicação:", font=("Arial", 11, "bold")).grid(
            row=3, column=1, sticky="nw", padx=10)
        self.lbl_explicacao = tk.Label(
            janela, text="Clique em 'Próximo passo' para reproduzir a busca.",
            justify="left", wraplength=280, font=("Arial", 11)
        )
        self.lbl_explicacao.grid(row=4, column=1, sticky="nw", padx=10)

        tk.Label(janela, text="Caminho final:", font=("Arial", 11, "bold")).grid(
            row=5, column=1, sticky="nw", padx=10)
        self.lbl_caminho = tk.Label(
            janela, text="-", justify="left", wraplength=280, font=("Arial", 11)
        )
        self.lbl_caminho.grid(row=6, column=1, sticky="nw", padx=10)

        botoes = tk.Frame(janela)
        botoes.grid(row=7, column=1, pady=15, sticky="w")
        tk.Button(
            botoes, text="Próximo passo", command=self.proximo_passo,
            font=("Arial", 11, "bold"), width=14
        ).pack(side="left", padx=5)
        tk.Button(
            botoes, text="Ver tudo", command=self.executar_tudo,
            font=("Arial", 11), width=10
        ).pack(side="left", padx=5)
        tk.Button(
            botoes, text="Reiniciar", command=self.reiniciar,
            font=("Arial", 11), width=10
        ).pack(side="left", padx=5)

        self.desenhar()

    def reiniciar(self):
        self.indice = 0
        self.revelados = []
        self.atual = None
        self.finalizado = False
        self.lbl_explicacao.config(text="Clique em 'Próximo passo' para reproduzir a busca.")
        self.lbl_caminho.config(text="-")
        self.lbl_passo.config(text="Passo: 0")
        self.lbl_atual.config(text="-")
        self.desenhar()

    def executar_tudo(self):
        while not self.finalizado:
            self.proximo_passo()

    def proximo_passo(self):
        if self.finalizado or self.indice >= len(self.ordem_visita):
            self.finalizado = True
            return

        estado = self.ordem_visita[self.indice]
        self.indice += 1
        self.revelados.append(estado)
        self.atual = estado
        self.lbl_passo.config(text=f"Passo: {self.indice}")
        self.lbl_atual.config(text=f"{estado} (h={self.heuristicas.get(estado)})")

        if estado == self.destino:
            self.lbl_explicacao.config(text=f"{estado} foi alcançado. Objetivo atingido!")
            self.lbl_caminho.config(
                text=f"{' -> '.join(self.caminho_final)}\nCusto total: {self.custo_total}"
            )
            self.finalizado = True
        elif estado in self.expandidos:
            self.lbl_explicacao.config(text=f"{estado} foi expandido pela busca.")
        else:
            self.lbl_explicacao.config(text=f"{estado} foi visitado.")

        self.desenhar()

    def desenhar(self):
        self.canvas.delete("all")

        feitas = set()
        for no, vizinhos in self.grafo.items():
            if no not in self.posicoes:
                continue
            x1, y1 = self.posicoes[no]
            for vizinho, custo in vizinhos.items():
                if vizinho not in self.posicoes:
                    continue
                par = tuple(sorted([no, vizinho]))
                if par in feitas:
                    continue
                feitas.add(par)
                x2, y2 = self.posicoes[vizinho]
                self.canvas.create_line(x1, y1, x2, y2, width=2, fill="gray")
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_rectangle(
                    mx - 14, my - 9, mx + 14, my + 9, fill="white", outline=""
                )
                self.canvas.create_text(mx, my, text=f"{custo}km", font=("Arial", 8))

        if self.finalizado:
            for a, b in zip(self.caminho_final, self.caminho_final[1:]):
                x1, y1 = self.posicoes[a]
                x2, y2 = self.posicoes[b]
                self.canvas.create_line(x1, y1, x2, y2, width=4, fill="green")

        raio = 34
        for no, (x, y) in self.posicoes.items():
            if self.finalizado and no in self.caminho_final:
                cor = "lightgreen"
            elif no == self.atual:
                cor = "orange"
            elif no in self.revelados:
                cor = "lightgray"
            else:
                cor = "white"

            if no == self.origem and not self.revelados:
                cor = "#5dade2"
            if no == self.destino and cor == "white":
                cor = "#e57373"

            self.canvas.create_oval(
                x - raio, y - raio, x + raio, y + raio,
                fill=cor, outline="black", width=2
            )
            nome = no.replace(" de ", "\nde ") if "de" in no else no
            self.canvas.create_text(
                x, y - 8, text=nome, font=("Arial", 9, "bold"), justify="center"
            )
            self.canvas.create_text(
                x, y + 14, text=f"h={self.heuristicas.get(no)}", font=("Arial", 9)
            )

        self.canvas.create_text(
            15, 565, anchor="w",
            text=("Azul=início | Vermelho=destino | Laranja=atual | "
                  "Cinza=já visitado | Verde=rota final"),
            font=("Arial", 9)
        )


def exibir_heuristica_resultado(grafo, heuristicas, origem, destino, resultado, posicoes=None):

    janela = tk.Tk()
    ReplayHeuristica(janela, grafo, heuristicas, origem, destino, resultado, posicoes)
    janela.mainloop()
