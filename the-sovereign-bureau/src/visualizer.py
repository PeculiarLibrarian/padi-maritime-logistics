import os
import json
import streamlit as st
from pathlib import Path
from streamlit_agraph import agraph, Node, Edge, Config

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PADI Sovereign Bureau", layout="wide")

# Custom CSS to match the "Peculiar Librarian" aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMarkdown h1, h3 {
        color: #1E90FF;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ The Sovereign Bureau | Nairobi-01 Node")
st.markdown("### Living Library of Access | PADI Technical Standard v2.1")

# --- MULTI-SECTOR PATH DISCOVERY ---
current_dir = Path(__file__).resolve().parent
possible_paths = [
    current_dir.parent / "data" / "graph_data.json", # Relative to src
    Path("the-sovereign-bureau/data/graph_data.json"), # Relative to repo root
    Path("data/graph_data.json"),                      # Direct relative
]

data_path = None
for p in possible_paths:
    if p.exists():
        data_path = p
        break

# --- DATA LOADING & RENDERING ---
if data_path:
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # 1. SIDEBAR CONTROLS
    st.sidebar.header("Bureau Controls")
    show_labels = st.sidebar.toggle("Show Connection Labels", value=True)
    
    st.sidebar.divider()
    st.sidebar.subheader("Integrity Legend")
    st.sidebar.write("🟢 **Green**: 1003 Compliant")
    st.sidebar.write("🟠 **Orange**: Partial Equity")
    st.sidebar.write("🔴 **Red**: Equity Deficit")
    st.sidebar.write("🔵 **Blue**: Structural Anchor")

    # 2. THE SOVEREIGN PALETTE
    # Note: Validator.py overrides colors for "Value" nodes, 
    # but we keep the map for structural "Subject" and "Object" nodes.
    color_map = {
        "Subject": "#1E90FF",  # Dodger Blue
        "Object": "#32CD32",   # Lime Green
    }

    # 3. NODE & EDGE PREPARATION
    nodes = []
    for n in data["nodes"]:
        # If the node has a color assigned by validator.py, use it. 
        # Otherwise, fall back to our sovereign palette.
        node_color = n.get("color", color_map.get(n.get("group"), "#CCCCCC"))
        
        nodes.append(Node(
            id=n["id"], 
            label=n.get("label", n["id"]), 
            size=25, 
            color=node_color,
            shape="dot"
        ))

    edges = [
        Edge(
            source=e["source"], 
            target=e["target"], 
            label=e["label"] if show_labels else ""
        ) 
        for e in data["links"]
    ]

    # 4. CONFIGURATION (Dynamic Future-Proof Physics)
    config = Config(
        width=1100, 
        height=800, 
        directed=True,
        nodeHighlightBehavior=True, 
        highlightColor="#F7A7A7", 
        collapsible=False,
        physics=True,
        d3={
            "linkStrength": 0.3,         # Balanced bond strength
            "gravity": -600,             # Strong repulsion for clarity
            "linkDistance": 200,         # Space for labels
            "centralGravity": 0.15,      # Prevents horizontal/vertical drift
            "friction": 0.9,             # Smooth movement
            "velocityDecay": 0.05        # Quick settling of nodes
        }
    )

    # 5. RENDER THE GRAPH
    agraph(nodes=nodes, edges=edges, config=config)

else:
    st.error("Sovereign Protocol Failure: graph_data.json not found.")
    st.info(f"Scanning Root: {os.getcwd()}")
    st.info(f"Visible Sectors: {os.listdir('.')}")