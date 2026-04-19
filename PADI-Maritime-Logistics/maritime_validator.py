import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from pyshacl import validate

# Define Namespaces
PADI = Namespace("https://padi.standard/schema#")
MARITIME = Namespace("https://padi.standard/maritime#")

def validate_inventory(csv_path, shape_path):
    print(f"--- PADI Liaison: Auditing {csv_path} ---")
    
    # 1. Load the SHACL Shape
    shapes_graph = Graph().parse(shape_path, format="turtle")
    
    # 2. Convert CSV to RDF Data Graph
    df = pd.read_csv(csv_path)
    data_graph = Graph()
    
    for index, row in df.iterrows():
        item_uri = URIRef(f"https://nairobi-01.node/inventory/item_{index}")
        data_graph.add((item_uri, RDF.type, MARITIME.StoreItem))
        data_graph.add((item_uri, MARITIME.itemID, Literal(row['itemID'])))
        data_graph.add((item_uri, MARITIME.stockLevel, Literal(int(row['stockLevel']))))
        data_graph.add((item_uri, MARITIME.vesselLocation, URIRef(row['vesselURI'])))

    # 3. RUN THE ENFORCEMENT
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference='rdfs'
    )

    if conforms:
        print("✅ SUCCESS: Data matches the Maritime Sovereign Shape.")
    else:
        print("❌ INTEGRITY ERROR: Invalid inventory detected.")
        print("\n--- SHACL REPORT ---")
        print(results_text)

if __name__ == "__main__":
    validate_inventory('vessel_manifest.csv', 'storekeeper_shape.ttl')
