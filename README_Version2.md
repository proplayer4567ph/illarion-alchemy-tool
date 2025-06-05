# Illarion Alchemy Recipe Simulator

This Streamlit app helps you simulate and plan alchemy recipes for the game Illarion.  
You can set target values for each substance, select herbs to add, track state, avoid explosions, and export your recipe as a CSV.

## Usage

1. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```
2. **Run the app**  
   ```
   streamlit run illarion_alchemy_app.py
   ```

3. **Set your desired target values** in the sidebar.
4. **Select herbs** step by step to reach your target, using Rotten Tree Bark as needed.
5. **Export your recipe** as a CSV file.

## Features

- Input any target values within [-4, 4] for each substance.
- Visualize current state after each step.
- Prevents out-of-bounds values ("explosions").
- Includes full herb list and effects.
- Downloadable CSV output.
- Easily reset and try again.

---

Enjoy experimenting!