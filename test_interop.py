import rdflib
import json

# 1. Load the Turtle data (The Librarian's Language)
g = rdflib.Graph()
try:
    g.parse("PADI-Maritime-Logistics/vessel_data.ttl", format="turtle")
    
    # 2. Serialize to JSON-LD (The Agent's Language)
    # This proves the data is "Interoperable"
    json_ld_data = g.serialize(format='json-ld')
    
    print("\n✅ SEMANTIC HANDSHAKE SUCCESSFUL")
    print("-" * 40)
    print("Agent-Readable JSON-LD Output:")
    print(json.dumps(json.loads(json_ld_data), indent=2))
    
except Exception as e:
    print(f"⚠️ Interop Error: {e}")
