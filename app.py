# Social Influence Simulation (Streamlit App)
# ---------------------------------------------------------
# This script implements a threshold-based cascade model
# for social influence diffusion in a random network.
# It is designed for educational and demonstration purposes.
# ---------------------------------------------------------

import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import time

# ---------------------------------------------------------
# Streamlit Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Viral Adoption Simulation", layout="wide")
st.title("Social Influence Simulation")

st.markdown(
    """
This interactive app demonstrates how behaviours, products, or ideas spread through a social network using a threshold-based game theory model.

### Core Concepts
- Thresholds: Each node adopts only if enough neighbors have already adopted.
- Network Structure: Determines who influences whom.
- Seed Node: Initial adopters who can trigger a cascade.
    """
)

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
st.sidebar.header("Simulation Parameters")
num_people = st.sidebar.slider("Number of people", 10, 100, 15)
p_connection = st.sidebar.slider("Connection probability", 0.1, 1.0, 0.2, 0.05)
num_seeds = st.sidebar.slider("Number of seed adopters", 1, 10, 3)
delay = st.sidebar.slider("Animation delay (seconds)", 0.1, 2.0, 0.5, 0.1)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def create_random_network(num_people, p_connection):
    """Generate an Erdős–Rényi random graph."""
    return nx.erdos_renyi_graph(n=num_people, p=p_connection)


def assign_random_thresholds(G, min_thresh=0.2, max_thresh=0.6):
    """Assign each node a random adoption threshold."""
    return {node: random.uniform(min_thresh, max_thresh) for node in G.nodes()}


def initialise_adoption(G, num_seeds):
    """Randomly select seed adopters."""
    adopted = {node: False for node in G.nodes()}
    seeds = random.sample(list(G.nodes()), num_seeds)
    for s in seeds:
        adopted[s] = True
    return adopted, seeds


def update_adoption(G, adopted, thresholds):
    """Update adoption based on neighbors' adoption states."""
    new_adopted = adopted.copy()

    for node in G.nodes():
        if adopted[node]:  # Already adopted
            continue

        neighbors = list(G.neighbors(node))
        if not neighbors:
            continue

        fraction = sum(adopted[n] for n in neighbors) / len(neighbors)

        if fraction >= thresholds[node]:
            new_adopted[node] = True

    return new_adopted


def visualise_network(G, adopted, title="Network Visualisation"):
    """Render the network with green = adopted, red = not adopted."""
    fig, ax = plt.subplots(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)
    node_colors = ["green" if adopted[node] else "red" for node in G.nodes()]

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


def animate_cascade_streamlit(G, adopted, thresholds, delay=0.5):
    """Animate the cascade one step at a time."""
    current_state = adopted.copy()
    step = 0

    st.markdown("---")
    st.markdown("### Cascade Animation")

    while True:
        fig = visualise_network(G, current_state, f"Cascade Step {step}")
        st.pyplot(fig)
        st.markdown(f"**Step {step}: {sum(current_state.values())}/{len(G.nodes())} adopted**")

        time.sleep(delay)
        new_state = update_adoption(G, current_state, thresholds)

        if new_state == current_state:
            st.markdown(f"**Cascade stopped at step {step}**")
            break

        current_state = new_state
        step += 1

    return current_state

# ---------------------------------------------------------
# Simulation Setup
# ---------------------------------------------------------
G = create_random_network(num_people, p_connection)
thresholds = assign_random_thresholds(G)
adopted, seeds = initialise_adoption(G, num_seeds)

st.subheader("Initial Network State")
st.markdown("Green nodes have adopted, red nodes have not.")
st.markdown(f"**Seed nodes:** {seeds}")

fig_init = visualise_network(G, adopted, "Initial State")
st.pyplot(fig_init)

st.markdown("---")

# ---------------------------------------------------------
# Run Simulation
# ---------------------------------------------------------
if st.button("Run Cascade"):
    final_state = animate_cascade_streamlit(G, adopted, thresholds, delay)

    st.subheader("Final Adoption State")
    st.markdown(
        f"Green nodes adopted, red nodes did not. Total adopted: "
        f"{sum(final_state.values())}/{num_people}"
    )

    fig_final = visualise_network(G, final_state, "Final Adoption State")
    st.pyplot(fig_final)

    st.markdown("---")
    st.markdown("### Commentary")
    st.markdown(
        """
The cascade demonstrates how a small set of initial adopters can trigger widespread adoption.

Key dynamics to observe:
- Seed placement dramatically affects spread.
- Higher thresholds slow or stop cascades.
- Dense networks spread influence more effectively.

Experiment with parameters yourself to see how behaviour changes!
        """
    )
