import streamlit as st
import pandas as pd

st.title("Illarion Alchemy Recipe Simulator")

# Substances and their abbreviations
substances = [
    ("A", "Adrazin"),
    ("I", "Illidrium"),
    ("C", "Caprazin"),
    ("H", "Hyperborlium"),
    ("E", "Echolon"),
    ("D", "Dracolin"),
    ("O", "Orcanol"),
    ("F", "Fenolin"),
]

# Herb list (herb: (effect1, effect2))
herbs = {
    "Anger berry":      [("A", 1), ("F", -1)],
    "Berries":          [("I", 1), ("O", -1)],
    "Birth mushroom":   [("H", 1), ("F", -1)],
    "Blackberry":       [("E", 1), ("A", -1)],
    "Black thistle":    [("C", 1), ("E", -1)],
    "Blue birdberry":   [("D", 1), ("A", -1)],
    "Bulbsponge mushroom": [("I", 1), ("F", -1)],
    "Champignon":       [("O", 1), ("I", -1)],
    "Donf blade":       [("F", 1), ("H", -1)],
    "Finris blossom":   [("E", 1), ("C", -1)],
    "Fir tree seedling": [("H", 1), ("E", -1)],
    "Flamegoblet blossom": [("E", 1), ("I", -1)],
    "Fourleafed Oneberry": [("F", 1), ("I", -1)],
    "Footleaf":         [("F", 1), ("C", -1)],
    "Grapes":           [("C", 1), ("F", -1)],
    "Heath flower":     [("H", 1), ("O", -1)],
    "Herder's mushroom": [("O", 1), ("H", -1)],
    "Mandrake":         [("O", 1), ("C", -1)],
    "Marsh flower":     [("D", 1), ("C", -1)],
    "Nuts":             [("D", 1), ("I", -1)],
    "Red Elder":        [("I", 1), ("D", -1)],
    "Red Head":         [("A", 1), ("E", -1)],
    "Sibanac leaf":     [("I", 1), ("E", -1)],
    "Strawberry":       [("C", 1), ("D", -1)],
    "Sandberry":        [("H", 1), ("D", -1)],
    "Sun herb":         [("A", 1), ("O", -1)],
    "Steppe fern":      [("O", 1), ("A", -1)],
    "Tangerine":        [("C", 1), ("O", -1)],
    "Toadstool":        [("D", 1), ("H", -1)],
    "Yellow weed":      [("F", 1), ("A", -1)],
    "Virgins weed":     [("A", 1), ("D", -1)],
    "Water blossom":    [("E", 1), ("H", -1)],
    "Rotten Tree Bark": "special"
}

# Target values (user-inputtable)
st.sidebar.header("Set Target Values")
target = {}
for abbr, full in substances:
    target[abbr] = st.sidebar.number_input(f"{full} ({abbr})", value=4 if abbr in ["A", "E"] else 0, min_value=-4, max_value=4)

st.markdown("### Herb List and Effects")
herb_df = []
for herb, effect in herbs.items():
    if effect == "special":
        desc = "Resets: -1 to positive, +1 to negative, unchanged to zero."
    else:
        desc = f"{effect[0][1]:+d} {dict(substances)[effect[0][0]]}, {effect[1][1]:+d} {dict(substances)[effect[1][0]]}"
    herb_df.append([herb, desc])
st.dataframe(pd.DataFrame(herb_df, columns=["Herb", "Effect"]))

# State
if "history" not in st.session_state:
    st.session_state.history = [{
        "Step": 0,
        "Herb": "",
        "Effect": "",
        **{abbr: 0 for abbr, _ in substances}
    }]

def apply_herb(state, herb):
    if herb == "Rotten Tree Bark":
        effect = []
        new_state = state.copy()
        for abbr, _ in substances:
            if new_state[abbr] > 0: new_state[abbr] -= 1; effect.append(f"{abbr} -1")
            elif new_state[abbr] < 0: new_state[abbr] += 1; effect.append(f"{abbr} +1")
        return new_state, ", ".join(effect) if effect else "No effect"
    else:
        effect = herbs[herb]
        new_state = state.copy()
        a1, v1 = effect[0]
        a2, v2 = effect[1]
        new_state[a1] += v1
        new_state[a2] += v2
        return new_state, f"{v1:+d} {a1}, {v2:+d} {a2}"

def check_bounds(state):
    return all(-4 <= v <= 4 for k, v in state.items() if k in dict(substances))

st.markdown("### Step-by-Step Recipe")
step = len(st.session_state.history)
herb_choice = st.selectbox("Choose herb to add:", list(herbs.keys()))
if st.button("Add Herb"):
    last = st.session_state.history[-1]
    new_state, effect = apply_herb(last, herb_choice)
    if not check_bounds(new_state):
        st.error("Explosion! Substance value out of bounds (-4 to +4). Revert and try a different herb or use Rotten Tree Bark.")
    else:
        st.session_state.history.append({
            "Step": step,
            "Herb": herb_choice,
            "Effect": effect,
            **{abbr: new_state[abbr] for abbr, _ in substances}
        })

# History Table
df = pd.DataFrame(st.session_state.history)
st.dataframe(df)

# Output CSV
csv = df.to_csv(index=False)
st.download_button("Download Recipe as CSV", csv, "illarion_recipe.csv", "text/csv")

# Check for target
last_state = st.session_state.history[-1]
if all(last_state[abbr] == target[abbr] for abbr in dict(substances)):
    st.success("Congratulations! You reached the target values. You may now optimize your recipe for efficiency.")

# Reset option
if st.button("Reset"):
    st.session_state.history = [{
        "Step": 0,
        "Herb": "",
        "Effect": "",
        **{abbr: 0 for abbr, _ in substances}
    }]