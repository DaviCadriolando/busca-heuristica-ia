from gestor_estados import GestorDeEstados
from main import grafo_mapa, heuristicas_originais
from heuristica_visual import exibir_heuristica_resultado

def executar_busca(
    nome_experimento,
    grafo,
    heuristicas,
    origem,
    destino
):

    print("\n")
    print("=" * 70)
    print(nome_experimento)
    print("=" * 70)

    gestor = GestorDeEstados(
        grafo,
        heuristicas
    )

    resultado = gestor.buscar_com_gestao(
        origem,
        destino,
        verbose=True
    )

    if resultado is None:

        print(
            "\nNão foi possível encontrar "
            "um caminho."
        )

        return None

    print("\n")
    print("=" * 70)
    print("PAINEL DE RESULTADOS")
    print("=" * 70)

    print(
        f"Origem: {origem}"
    )

    print(
        f"Destino: {destino}"
    )

    print(
        "\nOrdem de visita:"
    )

    print(
        " -> ".join(
            resultado['ordem_visita']
        )
    )

    print(
        "\nOrdem de expansão:"
    )

    print(
        " -> ".join(
            resultado['expandidos']
        )
    )

    print(
        "\nCaminho encontrado:"
    )

    print(
        " -> ".join(
            resultado['caminho_final']
        )
    )

    print(
        f"\nCusto total: "
        f"{resultado['custo_total']}"
    )

    print(
        f"Total de estados visitados: "
        f"{resultado['qtd_visitados']}"
    )

    print(
        f"Total de estados expandidos: "
        f"{resultado['qtd_expandidos']}"
    )

    print("=" * 70)

    return resultado


if __name__ == "__main__":

    origem = "Base de Atendimento"

    destino = "Hospital Central"

    resultado = executar_busca(
        nome_experimento="EXPERIMENTO 1 - HEURÍSTICA ORIGINAL",
        grafo=grafo_mapa,
        heuristicas=heuristicas_originais,
        origem=origem,
        destino=destino
    )

    if resultado is not None:
        exibir_heuristica_resultado(
            grafo = grafo_mapa,
            heuristicas = heuristicas_originais,
            origem = origem,
            destino = destino, 
            resultado = resultado
        )