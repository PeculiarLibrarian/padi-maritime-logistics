# The-Maritime-Inventory-Shape
This shape ensures that no "ghost inventory" can exist on a ship. Every item MUST have a location and a verified timestamp.

## Test Results: April 2026
- **Status:** PASS (Integrity Firewall Active)
- **Engine:** SHACL (Shapes Constraint Language)
- **Validation Event:** Successfully caught and rejected a negative stock level (-15) in a simulated vessel manifest upload.
- **Node:** Nairobi-01-Node
