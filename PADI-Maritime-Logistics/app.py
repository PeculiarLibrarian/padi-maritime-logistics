import streamlit as st
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from pyshacl import validate
import io

# Setup Namespaces
MARITIME = Namespace("https://padi.standard/maritime#")

st.set_page_config(page_title="PADI Liaison Dashboard", page_icon="⚓")

st.title("⚓ PADI Liaison Dashboard")
st.subheader("Sovereign Integrity Verification for Maritime Logistics")

st.markdown("""
Upload your vessel manifest (CSV) to verify it against the **PADI Maritime Standard**. 
This node uses **SHACL** to enforce deterministic stock integrity.
""")

uploaded_file = st.file_uploader("Choose a CSV manifest", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Previewing Manifest Data", df)
    
    if st.button("Run PADI Integrity Audit"):
        with st.spinner('Enforcing Sovereign Constraints...'):
            # 1. Load the SHACL Shape
            shapes_graph = Graph().parse("storekeeper_shape.ttl", format="turtle")
            
            # 2. Convert CSV to RDF
            data_graph = Graph()
            for index, row in df.iterrows():
                item_uri = URIRef(f"https://nairobi-01.node/inventory/item_{index}")
                data_graph.add((item_uri, RDF.type, MARITIME.StoreItem))
                data_graph.add((item_uri, MARITIME.itemID, Literal(row['itemID'])))
                data_graph.add((item_uri, MARITIME.stockLevel, Literal(int(row['stockLevel']))))
                data_graph.add((item_uri, MARITIME.vesselLocation, URIRef(row['vesselURI'])))

            # 3. Validate
            conforms, results_graph, results_text = validate(data_graph, shacl_graph=shapes_graph)

            if conforms:
                st.success("✅ INTEGRITY VERIFIED: All records comply with the Sovereign Standard.")
                st.balloons()
            else:
                st.error("❌ INTEGRITY BREACH: Non-compliant data detected.")
                st.text_area("SHACL Violation Report", results_text, height=300)
