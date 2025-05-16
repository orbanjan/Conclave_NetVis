# 085_Conclave_NetVis  
📊 Visualizing the 2025 Papal Conclave: A Network Analysis Approach with Python & Gephi

Over the past few days, I developed a data-driven network analysis project focused on the upcoming 2025 Papal Conclave. Using Python and Gephi, I explored how relationships among cardinals can be mapped based on shared characteristics — revealing potential influence hubs and regional patterns.

🔍 Project Goals
The aim was to:

Clean and enrich the cardinals dataset from Kaggle

Construct a weighted similarity network based on attributes like:

Age

Country & Continent

Papal appointment (Pope & Date)

Religious Order (special emphasis on CB = Cardinal Bishops)

Export the resulting graph structure for visual exploration in Gephi

🛠️ How it Works (Core Steps in Python):
Data Cleaning

Removed annotation artifacts in country names

Mapped countries to continents manually

Feature Engineering

Encoded multiple similarity dimensions between cardinals

Used logic to prioritize under-70 members and Cardinal Bishops

Edge Construction

For every pair of cardinals, computed a Weight based on:

Same Pope (+1)

Same Date (+1)

Both under 70 (+2), one under 70 (+1)

Same Country or Continent (+1 each)

Shared CB order (+2), one CB (+1)

Node Strength Calculation

Calculated total connection strength per cardinal using edge weights

Gephi Export

edges.csv: Source, Target, Weight

nodes.csv: Id, Age, Country, Order, Continent, Weight

🧠 Why It Matters
This kind of network-based insight goes beyond simple rankings — it reveals clusters, influence bridges, and isolated figures. Such analysis can help journalists, historians, and data scientists anticipate voting dynamics or visualize institutional structures.

