import networkx as nx


def small_world(n, params, seed=None):
    """
    Generates a small world network with n nodes.
    """
    try:
        k, p, omega_range, links_range = params.values()
    except KeyError:
        raise ValueError("Invalid params for connected_watts_strogatz_graph.")

    sufficient = False
    while not sufficient:
        graph = nx.connected_watts_strogatz_graph(n, k, p, tries=100, seed=seed)
        omega = nx.smallworld.omega(graph)
        print(f"Value of omega: {omega}")

        if min(omega_range) <= omega <= max(omega_range):
            print(f"Ideal topology found with omega between {omega_range}")
            sufficient = True

    return graph
