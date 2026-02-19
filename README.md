# Social Influence Simulation

This project is an fun interactive **Streamlit-based educational app** that demonstrates how behaviours, products and ideas can spread through a social network using a **threshold cascade model** grounded in game theory - a topic that I found very interesting in University. 

I made this intentionally simple, visual and exploratory.

---

## 1. Overview

The model represents a group of individuals (nodes) connected in a social network (edges). Each individual has:

* A **threshold**: the fraction of their neighbors who must adopt before they adopt.
* An **adoption state**: adopted (green) or not adopted (red).

The simulation begins with a small number of **seed adopters** and adoption spreads according to the threshold rule. The cascade continues until no further changes occur.

This project allows us to experiment with:

* Network size
* Network connection density
* Number of initial adopters
* Random adoption thresholds
* Cascade animations

---

## 2. Features

* **Interactive parameter selection** through the Streamlit sidebar
* **Random network generation** using Erdős–Rényi graphs
* **Random threshold assignment** between configurable bounds
* **Seed selection** from random nodes
* **Step-by-step cascade animation** with configurable delay
* **Final visualisation** of adoption outcome
* **Educational commentary** explaining model behaviour

---

## 3. How to Run Locally

### Prerequisites

Ensure you have Python 3.8+ installed.

Install required packages:

```bash
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

This will launch the application in your browser at:

```
http://localhost:8501
```

---

## 4. File Structure

```
📦 social-influence-simulation
 ┣ 📜 app.py               # Streamlit application
 ┣ 📜 README.md            # Project documentation
 ┗ 📜 requirements.txt     # Python dependencies
```

---

## 5. The Model in Brief

This simulation uses a **linear threshold model** where each node adopts when:

```
(adopting neighbors / total neighbors) ≥ threshold
```

This represents many real-world processes:

* Product adoption
* Social movements
* Technology diffusion
* Viral content spreading
* Behavioural norm formation

The model highlights how:

* Network density
* Threshold distribution
* Seed placement
  can dramatically affect diffusion outcomes.

---

## 6. Example Visualisation

**Nodes:** individuals
**Edges:** influence relationships
**Colours:**

* Green = adopted
* Red = not adopted

The simulation displays the network at each step until adoption stabilises.

---

## 7. Deployment

You can deploy this app for free on **Streamlit Community Cloud**.

1. Push the repository to GitHub
2. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Select your repository
4. Choose `app.py` as the entrypoint
5. Deploy

The app will be accessible online with a public URL.

---

## 8. Future Enhancements

The project is designed to be extendable. Potential features include:

* Slider-controlled cascade slideshow
* Support for additional network types (Watts–Strogatz, Barabási–Albert)
* Deterministic or clustered seed selection strategies
* Customisable threshold distributions

---

## 9. License

This project is released under the MIT License.

---

## 10. Acknowledgements

This project is inspired by foundational work in:

* Game Theory
* Network Science
* Social Influence Modelling

It is intended as an accessible, hands-on tool for learning and experimentation (and gets me keep practising coding).
