"""
Social Influence Simulation (Streamlit App)
===========================================

This module implements an interactive Streamlit application that simulates
social influence diffusion using a threshold-based cascade model on a random
network.

The model demonstrates how behaviors, ideas, or products spread through
a population when individuals adopt only after a sufficient proportion
of their neighbors have adopted.

Key Features
------------
- Erdős–Rényi random network generation
- Individual adoption thresholds
- Seed-based cascade initiation
- Step-by-step animated diffusion visualization
- Interactive parameter controls via Streamlit

This project is intended for educational, analytical, and demonstration
purposes, particularly in social networks, game theory, and computational
social science.
"""

import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st


# ---------------------------------------------------------------------
# Streamlit Configuration
# ---------------------------------------------------------------------
st.set_page_config(page_title="Viral Adoption Simulation", layout="wide")
st.title("Social Influence Simulation")

st.markdown(
    """
This interactive app demonstrates how behaviours, products, or ideas spread
through a social network using a threshold-based game theory model.

### Core Concepts
- **Thresholds**: Each node adopts only if enough neighbors have adopted.
- **Network Structure**: Determines who influences whom.
- **Seed Nodes**: Initial adopters that may trigger a cascade.
"""
)


# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("Simulation Parameters")

num_people = st.sidebar.slider(
    "Number of people", min_value=10, max_value=100, value=15
)
p_connection = st.sidebar.slider(
    "Connection probability", min_value=0.1, max_value=1.0, value=0.2, step=0.05
)
num_seeds = st.sidebar.slider(
    "Number of seed adopters", min_value=1, max_value=10, value=3
)
delay = st.sidebar.slider(
    "Animation delay (seconds)", min_value=0.1, max_value=2.0, value=0.5, step=0.1
)


# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------
def create_random_network(num_people: int, p_connection: float) -> nx.Graph:
    """
    Generate a random social network using the Erdős–Rényi model.

    Args:
        num_people (int): Number of nodes (individuals) in the network.
        p_connection (float): Probability that an edge exists between any
            two nodes.

    Returns:
        networkx.Graph: Generated random graph.
    """
    return nx.erdos_renyi_graph(n=num_people, p=p_connection)


def assign_random_thresholds(
    G: nx.Graph, min_thresh: float = 0.2, max_thresh: float = 0.6
) -> dict:
    """
    Assign a random adoption threshold to each node in the network.

    The threshold represents the minimum fraction of neighbors that must
    adopt before the node adopts.

    Args:
        G (networkx.Graph): Social network graph.
        min_thresh (float, optional): Minimum threshold value.
        max_thresh (float, optional): Maximum threshold value.

    Returns:
        dict: Mapping of node -> adoption threshold.
    """
    return {node: random.uniform(min_thresh, max_thresh) for node in G.nodes()}


def initialise_adoption(G: nx.Graph, num_seeds: int) -> tuple:
    """
    Initialize the adoption state by selecting seed adopters.

    Args:
        G (networkx.Graph): Social network graph.
        num_seeds (int): Number of initial adopters.

    Returns:
        tuple:
            - dict: Mapping of node -> adoption state (True/False)
            - list: List of seed nodes
    """
    adopted = {node: False for node in G.nodes()}
    seeds = random.sample(list(G.nodes()), num_seeds)

    for node in seeds:
        adopted[node] = True

    return adopted, seeds


def update_adoption(
    G: nx.Graph, adopted: dict, thresholds: dict
) -> dict:
    """
    Update adoption states based on neighbors' adoption levels.

    A node adopts if the fraction of its neighbors that have adopted
    meets or exceeds its threshold.

    Args:
        G (networkx.Graph): Social network graph.
        adopted (dict): Current adoption states.
        thresholds (dict): Node adoption thresholds.

    Returns:
        dict: Updated adoption states.
    """
    new_adopted = adopted.copy()

    for node in G.nodes():
        if adopted[node]:
            continue

        neighbors = list(G.neighbors(node))
        if not neighbors:
            continue

        fraction_adopted = sum(adopted[n] for n in neighbors) / len(neighbors)

        if fraction_adopted >= thresholds[node]:
            new_adopted[node] = True

    return new_adopted


def visualise_network(
    G: nx.Graph, adopted: dict, title: str = "Network Visualisation"
) -> plt.Figure:
    """
    Visualize the social network with adoption states.

    Adopted nodes are colored green, non-adopted nodes red.

    Args:
        G (networkx.Graph): Social network graph.
        adopted (dict): Adoption states.
        title (str, optional): Plot title.

    Returns:
        matplotlib.figure.Figure: Rendered network visualization.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)

    node_colors = [
        "green" if adopted[node] else "red" for node in G.nodes()
    ]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=500,
        font_size=10,
        ax=ax,
    )

    ax.set_title(title)
    return fig


def animate_cascade_streamlit(
    G: nx.Graph, adopted: dict, thresholds: dict, delay: float = 0.5
) -> dict:
    """
    Animate the adoption cascade step-by-step in Streamlit.

    The animation stops when no further adoptions occur.

    Args:
        G (networkx.Graph): Social network graph.
        adopted (dict): Initial adoption states.
        thresholds (dict): Adoption thresholds.
        delay (float, optional): Pause between steps in seconds.

    Returns:
        dict: Final adoption state after cascade completion.
    """
    current_state = adopted.copy()
    step = 0

    st.markdown("---")
    st.markdown("### Cascade Animation")

    while True:
        fig = visualise_network(G, current_state, f"Cascade Step {step}")
        st.pyplot(fig)

        st.markdown(
            f"**Step {step}: "
            f"{sum(current_state.values())}/{len(G.nodes())} adopted**"
        )

        time.sleep(delay)
        new_state = update_adoption(G, current_state, thresholds)

        if new_state == current_state:
            st.markdown(f"**Cascade stopped at step {step}**")
            break

        current_state = new_state
        step += 1

    return current_state


# ---------------------------------------------------------------------
# Simulation Setup
# ---------------------------------------------------------------------
G = create_random_network(num_people, p_connection)
thresholds = assign_random_thresholds(G)
adopted, seeds = initialise_adoption(G, num_seeds)

st.subheader("Initial Network State")
st.markdown("Green nodes have adopted, red nodes have not.")
st.markdown(f"**Seed nodes:** {seeds}")

fig_init = visualise_network(G, adopted, "Initial State")
st.pyplot(fig_init)

st.markdown("---")


# ---------------------------------------------------------------------
# Run Simulation
# ---------------------------------------------------------------------
if st.button("Run Cascade"):
    final_state = animate_cascade_streamlit(G, adopted, thresholds, delay)

    st.subheader("Final Adoption State")
    st.markdown(
        f"Total adopted: {sum(final_state.values())}/{num_people}"
    )

    fig_final = visualise_network(G, final_state, "Final Adoption State")
    st.pyplot(fig_final)

    st.markdown("---")
    st.markdown("### Commentary")
    st.markdown(
        """
This simulation illustrates how local decision rules can produce
large-scale diffusion patterns.

Key observations:
- Seed selection strongly influences cascade size.
- Higher thresholds inhibit spread.
- Denser networks facilitate faster adoption.

The model highlights the interaction between individual incentives
and network structure in social diffusion processes.
"""
    )
