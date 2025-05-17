# Import necessary libraries
import pandas as pd
import re
import pycountry
import pycountry_convert as pc
from itertools import combinations

def get_continent(country_name):
    try:
        # Handle special cases
        if country_name == "Jerusalem":
            return "Asia"
        if country_name == "China\n(Hong Kong)":
            return "Asia"
            
        # Get country code
        country = pycountry.countries.get(name=country_name)
        if not country:
            # Try with common_name
            country = pycountry.countries.get(common_name=country_name)
        if not country:
            # Try with alpha_2
            country = pycountry.countries.get(alpha_2=country_name)
            
        if country:
            # Get continent code
            continent_code = pc.country_alpha2_to_continent_code(country.alpha_2)
            # Convert continent code to full name
            continent_names = {
                'NA': 'North America',
                'SA': 'South America',
                'AS': 'Asia',
                'OC': 'Oceania',
                'AF': 'Africa',
                'EU': 'Europe'
            }
            return continent_names[continent_code]
    except:
        pass
    return None

def generate_network():
    # Load the dataset
    df = pd.read_csv(r'data/cardinals.csv', encoding="utf-8")
    
    # Remove annotations from country names
    df["Country"] = df["Country"].apply(lambda x: re.sub(r"\[.*?\]", "", x).strip())
    
    # Add continent information
    df["Continent"] = df["Country"].apply(get_continent)
    
    # Initialize list to store edges
    edges = []
    
    # Iterate over all unique pairs of cardinals
    for i, j in combinations(df.index, 2):
        card1 = df.loc[i]
        card2 = df.loc[j]
        
        weight = 0
        
        # +1 if appointed by same pope
        if card1["Pope_of_consistory"] == card2["Pope_of_consistory"]:
            weight += 1
        
        # +1 if appointed on the same date
        if card1["Date_of_consistory"] == card2["Date_of_consistory"]:
            weight += 1

        # Age-based weighting: prioritize under 70
        age1_under70 = card1["Age"] < 70
        age2_under70 = card2["Age"] < 70
        if age1_under70 and age2_under70:
            weight += 2
        elif age1_under70 or age2_under70:
            weight += 1

        # +1 if from the same country
        if card1["Country"] == card2["Country"]:
            weight += 1

        # +1 if from the same continent
        if card1["Continent"] == card2["Continent"]:
            weight += 1

        # Order-based weighting: emphasize "CB"
        order1_cb = card1["Order"] == "CB"
        order2_cb = card2["Order"] == "CB"
        if order1_cb and order2_cb:
            weight += 2
        elif order1_cb or order2_cb:
            weight += 1

        # Add edge if there's any similarity
        if weight > 0:
            edges.append({
                "Source": card1["Name"],
                "Target": card2["Name"],
                "Weight": weight
            })

    # Create edges DataFrame
    edges_df = pd.DataFrame(edges)
    
    # Sum weights where each node appears as Source or Target
    node_strength = (
        edges_df.groupby("Source")["Weight"].sum()
        .add(edges_df.groupby("Target")["Weight"].sum(), fill_value=0)
        .reset_index()
        .rename(columns={0: "Weight", "index": "Name"})
    )

    # Merge with all cardinal names to ensure all nodes are included
    all_nodes = df[["Name"]].copy()
    nodes_df = all_nodes.merge(node_strength, on="Name", how="left").fillna(0)
    
    # Export edges.csv for Gephi
    edges_df.to_csv("edges.csv", index=False)

    # Export nodes.csv for Gephi (Id, Label, Weight + optional attributes)
    nodes_export = df[["Name", "Country", "Continent", "Order", "Age"]].copy()
    nodes_export = nodes_export.merge(nodes_df[["Name", "Weight"]], on="Name", how="left")

    # Rename columns to fit Gephi's expected format
    nodes_export.rename(columns={
        "Name": "Id",
        "Country": "Country",
        "Order": "Order",
        "Age": "Age",
        "Weight": "Weight",
        "Continent": "Continent"
    }, inplace=True)

    # Save nodes.csv
    nodes_export.to_csv("nodes.csv", index=False)
    
    print("Network generation complete!")
    print(f"Generated {len(edges_df)} edges and {len(nodes_df)} nodes")
    print("Files saved: edges.csv and nodes.csv")

if __name__ == "__main__":
    generate_network() 