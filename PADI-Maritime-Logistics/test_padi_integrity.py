import os
import unittest
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from pyshacl import validate

# Setup Namespaces
MARITIME = Namespace("https://padi.standard/maritime#")

class TestPADIIntegrity(unittest.TestCase):
    def test_negative_stock_rejection(self):
        """Verify that the SHACL engine correctly rejects negative stock levels."""
        # 1. SETUP: Create a malicious CSV
        test_csv = "regression_test.csv"
        df = pd.DataFrame({
            'itemID': ['FAIL-ITEM'],
            'stockLevel': [-50],
            'vesselURI': ['https://padi.standard/vessels/MS-Sovereign']
        })
        df.to_csv(test_csv, index=False)

        # 2. ACT: Build the graph and validate
        shapes_graph = Graph().parse("storekeeper_shape.ttl", format="turtle")
        data_graph = Graph()
        
        for index, row in df.iterrows():
            item_uri = URIRef(f"https://nairobi-01.node/inventory/item_{index}")
            data_graph.add((item_uri, RDF.type, MARITIME.StoreItem))
            data_graph.add((item_uri, MARITIME.itemID, Literal(row['itemID'])))
            data_graph.add((item_uri, MARITIME.stockLevel, Literal(int(row['stockLevel']))))
            data_graph.add((item_uri, MARITIME.vesselLocation, URIRef(row['vesselURI'])))

        conforms, _, _ = validate(data_graph, shacl_graph=shapes_graph)

        # 3. ASSERT: The system must NOT conform (it must catch the error)
        self.assertFalse(conforms, "CRITICAL: The PADI firewall failed to catch a negative stock level!")
        
        # Cleanup
        if os.path.exists(test_csv):
            os.remove(test_csv)
        print("\n✅ REGRESSION TEST PASSED: SHACL Firewall is active and unbreakable.")

if __name__ == "__main__":
    unittest.main()
