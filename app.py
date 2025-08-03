# app.py
import streamlit as st
import numpy as np
from itertools import product
from scipy.optimize import linprog

st.set_page_config(page_title="Real-Time Game Theory Simulator", layout="wide")

st.title("🎯 Real-Time Game Theory Simulator")
st.write("An interactive platform covering Game Theory concepts from your syllabus.")

menu = st.sidebar.selectbox(
    "Select Game Mode",
    ["Zero-Sum Game Solver", "Nash Equilibrium Finder", "Bargaining Game"]
)

# ====================================================
# Zero-Sum Game Solver
# ====================================================
if menu == "Zero-Sum Game Solver":
    st.subheader("🎮 Zero-Sum Game Solver")
    rows = st.number_input("Number of Player 1 strategies", min_value=2, max_value=5, value=3)
    cols = st.number_input("Number of Player 2 strategies", min_value=2, max_value=5, value=3)

    payoff_matrix = []
    st.write("Enter payoff matrix for Player 1 (comma separated values per row):")
    for i in range(rows):
        row = st.text_input(f"Row {i+1}", ",".join(["0"] * cols))
        payoff_matrix.append(list(map(float, row.split(","))))

    if st.button("Solve Zero-Sum Game"):
        payoff_matrix = np.array(payoff_matrix)

        # Linear programming solution
        c = np.ones(rows)
        A_ub = -payoff_matrix.T
        b_ub = -np.ones(cols)
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, method='highs')

        if res.success:
            strategy = res.x / sum(res.x)
            st.success("Optimal Strategy for Player 1: " + str(strategy))
            st.info(f"Game Value: {1 / sum(res.x):.3f}")
        else:
            st.error("Failed to solve game. Check your input matrix.")

# ====================================================
# Nash Equilibrium Finder
# ====================================================
elif menu == "Nash Equilibrium Finder":
    st.subheader("🔍 Nash Equilibrium Finder (Pure Strategies)")
    rows = st.number_input("Number of strategies for Player 1", min_value=2, max_value=5, value=2)
    cols = st.number_input("Number of strategies for Player 2", min_value=2, max_value=5, value=2)

    A, B = [], []
    st.write("Enter payoff matrix for Player 1 (A):")
    for i in range(rows):
        A.append(list(map(float, st.text_input(f"A Row {i+1}", ",".join(["0"] * cols)).split(","))))

    st.write("Enter payoff matrix for Player 2 (B):")
    for i in range(rows):
        B.append(list(map(float, st.text_input(f"B Row {i+1}", ",".join(["0"] * cols)).split(","))))

    if st.button("Find Nash Equilibria"):
        A, B = np.array(A), np.array(B)
        equilibria = []

        for i, j in product(range(rows), range(cols)):
            if all(A[i, j] >= A[k, j] for k in range(rows)) and \
               all(B[i, j] >= B[i, l] for l in range(cols)):
                equilibria.append(((i, j), (A[i, j], B[i, j])))

        if equilibria:
            st.success(f"Nash Equilibria: {equilibria}")
        else:
            st.warning("No pure strategy Nash equilibrium found.")

# ====================================================
# Bargaining Game (Rubinstein Model)
# ====================================================
elif menu == "Bargaining Game":
    st.subheader("🤝 Bargaining Game Simulator (Rubinstein Model)")
    total_pie = st.number_input("Total amount to split", min_value=1.0, value=100.0)
    discount_A = st.slider("Discount factor for Player A", 0.0, 1.0, 0.9, 0.01)
    discount_B = st.slider("Discount factor for Player B", 0.0, 1.0, 0.9, 0.01)

    if st.button("Simulate Bargaining"):
        share_A = total_pie * (1 - discount_B) / (1 - discount_A * discount_B)
        share_B = total_pie - share_A
        st.success(f"Player A gets: {share_A:.2f}")
        st.success(f"Player B gets: {share_B:.2f}")
        st.info("This is the subgame perfect equilibrium outcome for the Rubinstein bargaining game.")
