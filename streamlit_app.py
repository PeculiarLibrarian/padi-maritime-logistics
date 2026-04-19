import streamlit as st
import re

st.set_page_config(page_title="PADI N-1-NODE Auditor", page_icon="🚢")

# Professional Registry (Mock Database)
AUTHORIZED_REGISTRY = {
    "NB-01-NODE": {"vessel": "Nairobi Pioneer", "owner": "PADI Authority Bureau"},
    "AU-SYD-773": {"vessel": "Southern Star", "owner": "Global Logistics Group"},
    "KE-MAR-002": {"vessel": "Indian Ocean Express", "owner": "Nairobi Maritime"}
}

st.title("🚢 PADI Sovereign Bureau")
st.subheader("Deterministic Semantic Auditor")

# Identity Sidebar
st.sidebar.info("Verified Auditor Node")
st.sidebar.code("agent1qd9etuce86p36p2vgztssdxa2ccy3s8quezflqt9zsuqcp7dtt0uy3mw4m0")

# Input Section
st.markdown("### Execute Audit")
vessel_id = st.text_input("Enter Vessel ID for Verification:", placeholder="e.g., NB-01-NODE")

if st.button("Run Handshake"):
    # Level 1: Regex Pattern Validation (XX-00-NODE/TEXT)
    pattern = r'^[A-Z]{2}-\d{2}-[A-Z0-9]+$'
    
    if not re.match(pattern, vessel_id):
        st.error("❌ SCHEMA VIOLATION")
        st.warning(f"ID '{vessel_id}' does not meet PADI v3.0.1 naming standards.")
        st.info("Required Format: [CountryCode]-[Numeric]-[NodeID] (e.g., NB-01-NODE)")
    
    # Level 2: Registry Validation
    elif vessel_id in AUTHORIZED_REGISTRY:
        data = AUTHORIZED_REGISTRY[vessel_id]
        st.success(f"✅ HANDSHAKE SUCCESSFUL: {vessel_id}")
        st.balloons()
        st.json({
            "@context": "http://example.org/padi",
            "@type": "Vessel",
            "vesselID": vessel_id,
            "vesselName": data['vessel'],
            "registeredOwner": data['owner'],
            "auditTimestamp": "2026-04-19T18:30:00Z",
            "auditorNode": "Nairobi-01"
        })
    
    # Level 3: Unknown Identity
    else:
        st.error("❌ IDENTITY NOT FOUND")
        st.write(f"The ID '{vessel_id}' follows the correct format but is not registered in the Global Almanac.")

st.divider()
st.caption("PADI Technical Standard v3.0.1 | The Peculiar Librarian")
