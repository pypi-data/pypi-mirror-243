import networkx as nx


def complete(params):
    """
    Generates a complete network with n nodes.
    """
    try:
        n = params.values()
    except KeyError:
        raise ValueError("Invalid params for complete_graph.")
    return nx.complete_graph(n)
