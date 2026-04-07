import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FedGNN-Explain: Nigeria Fraud Defense",
    page_icon="🇳🇬",
    layout="wide"
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🏦 FedGNN-Explain Dashboard")
st.subheader("Federated Graph Intelligence for Cross-Bank Fraud Detection")
st.info("🔒 NDPR Compliant: Raw transaction data remains localized at OPay/GTB/PalmPay firewalls.")

# --- SIDEBAR: INVESTIGATION TOOLS ---
st.sidebar.header("🔍 Transaction Search")
target_tx = st.sidebar.text_input("Enter Transaction ID", value="TX_OPAY_88271")
risk_threshold = st.sidebar.slider("Sensitivity Threshold (Alpha)", 0.0, 1.0, 0.75)

st.sidebar.divider()
st.sidebar.write("**Institution:** OPay Digital Services")
st.sidebar.write("**Federated Status:** Synchronized (Round 5)")

# --- MOCK DATA LOGIC ---
# In a real app, this would be: model.predict(transaction_graph)
fraud_prob = 0.942 
is_fraud = fraud_prob > risk_threshold

# --- MAIN DISPLAY ---
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### 📊 Risk Analysis")
    if is_fraud:
        st.error("🚩 HIGH RISK DETECTED")
    else:
        st.success("✅ LEGITIMATE")

    st.metric(label="Fraud Probability Score", value=f"{fraud_prob*100:.1f}%")
    
    st.write("**Topological Red Flags:**")
    st.write("- High-velocity 'Smurfing' patterns")
    st.write("- Connection to known GTBank exit node")
    st.write("- Unusual 3-hop layering path")

    if st.button("Generate CBN/EFCC Report"):
        st.download_button("Download STR PDF", "Sample Report Data", file_name="STR_Report.pdf")

with col2:
    st.write("### 🕸️ Explainable AI: Fraud Ring Subgraph")
    st.caption("Attention-weighted visualization of the 2-hop neighborhood.")

    # Generate a sample fraud ring graph
    G = nx.DiGraph()
    # Add nodes (Origin, Mules, Exit)
    nodes = ["Sender", "Mule_1", "Mule_2", "Mule_3", "GTB_Exit_Node", "Utility_Pay"]
    G.add_nodes_from(nodes)
    G.add_edges_from([
        ("Sender", "Mule_1"), ("Sender", "Mule_2"), ("Sender", "Mule_3"),
        ("Mule_1", "GTB_Exit_Node"), ("Mule_2", "GTB_Exit_Node"), ("Mule_3", "GTB_Exit_Node"),
        ("Sender", "Utility_Pay") # Legitimate path to ignore
    ])

    # Color logic based on "Attention"
    color_map = []
    for node in G:
        if "Mule" in node or "Exit" in node or "Sender" in node:
            color_map.append('#ff4b4b') # Red for fraud ring
        else:
            color_map.append('#9eaec0') # Grey for legitimate

    fig, ax = plt.subplots(figsize=(8, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=color_map, 
            node_size=2000, font_size=10, font_weight="bold", 
            edge_color='gray', arrows=True, ax=ax)
    
    st.pyplot(fig)

st.divider()
st.caption("FedGNN-Explain Prototype © 2026 | Developed for Miva Open University")
