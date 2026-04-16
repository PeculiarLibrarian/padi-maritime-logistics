import os
import json
from pathlib import Path

# --- CONFIGURATION ---
# Point this to where your local PADI-related repos are stored
REPOS_ROOT = Path("C:/") # Adjust this to your actual projects folder
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "graph_data.json"

# The 1003 Cardinality Requirements
SOVEREIGN_PILLARS = ["README.md", "ontology", "LICENSE"]

def validate_integrity(repo_path):
    """Checks for the presence of the 1003 Cardinality pillars."""
    if not repo_path.exists():
        return "FAIL"
    
    found_pillars = 0
    for pillar in SOVEREIGN_PILLARS:
        # Check for file or directory presence
        if (repo_path / pillar).exists():
            found_pillars += 1
            
    if found_pillars == len(SOVEREIGN_PILLARS):
        return "PASS"
    elif found_pillars > 0:
        return "PARTIAL"
    else:
        return "FAIL"

def run_validation_cycle():
    if not DATA_PATH.exists():
        print("❌ Error: No graph data found. Run Liaison first.")
        return

    with open(DATA_PATH, 'r') as f:
        graph = json.load(f)

    print("🛡️ Validator: Initiating Technical Equity Scan...")
    
    # Update node colors based on validation
    for node in graph["nodes"]:
        if node["group"] == "Value": # These are our repositories
            repo_name = node["id"]
            repo_path = REPOS_ROOT / repo_name
            
            status = validate_integrity(repo_path)
            
            if status == "PASS":
                node["color"] = "#00FF00"  # Bright Green (Equity Achieved)
                node["label"] = f"✅ {repo_name}"
            elif status == "PARTIAL":
                node["color"] = "#FFA500"  # Orange (Warning)
                node["label"] = f"⚠️ {repo_name}"
            else:
                node["color"] = "#FF0000"  # Red (Equity Deficit)
                node["label"] = f"❌ {repo_name}"

    with open(DATA_PATH, 'w') as f:
        json.dump(graph, f, indent=4)
    
    print("✅ Validation complete. Integrity levels synchronized.")

if __name__ == "__main__":
    run_validation_cycle()
