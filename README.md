# 🌍 PopGen Ancestry Map
**PopGen Ancestry Map** is an interactive web application for visualizing population ancestry data. Users can upload their own dataset, and the app generates a map with pie chart popups showing ancestry breakdowns for each population.

## 🔍 Why use this tool?
Who wants to manually analyse large tables of population data? I'm guessing not you (since you end up in this repository). This app helps users quickly identify patterns of population ancestries around the globe. Useful for population genetics studies.

## ⚙️ Installation and Setup
### 1. Clone the repository
```bash
git clone https://github.com/annacastellet/popgen-ancestry-map.git
cd popgen-ancestry-map
```

### 2. Install dependencies
You can install the required dependencies using Conda.
```bash
conda env create -f popgen_environment.yml
conda activate popgen
```

### 3. Run the App
In your terminal, with the Conda environment activated, run:
```bash
streamlit run popgen_ancestry_app.py
```
Streamlit will open the app in your favourite browser, where you'll be prompted to upload your data.

## 📊 Input data format
Your data (in Excel ``.xlsx`` format) should follow this structure:

| Pop   | Lat   | Long   | Continent    | Ancestry_1 | Ancestry_2 | Ancestry_3 | ... |
|-------|-------|--------|--------------|------------|------------|------------|-----|
| PopA  | 34.05 | -118.24| North America| 0.50       | 0.30       | 0.20       | ... |
| PopB  | 51.51 | -0.12  | Europe       | 0.70       | 0.20       | 0.10       | ... |

This repository includes a test dataset (``data/modern_ancestry_in_populations.xlsx``) that you can use to see how the application works.

### Want to use your own data?
Make sure the data set contains the following columns (with the corresponding headers):
* ``Pop`` column for population names
* ``Lat`` and ``Long`` columns for geographic coordinates
* ``Continent`` column
* One or more ancestry columns (can have any name), each containing proportions (values from 0 to 1) of different ancestries
  
## 💡 How it works?
1. Upload your dataset
2. Preview the first few rows to verify data format
3. The app extracts ancestry columns and processes the data
4. A Folium map is generated, plotting populations
5. Pie charts appear in popups when you click a marker
6. A draggable legend highlights dominant ancestries

## 
If you encounter any issues or have suggestions for improvement, feel free to reach out!
📩 annacastellet.5@gmail.com