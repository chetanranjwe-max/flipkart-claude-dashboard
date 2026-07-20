import streamlit as st
import json
import time
import anthropic

st.set_page_config(page_title="Claude Flipkart Dashboard", layout="wide")
st.title("🤖 Claude AI - Flipkart Control Center")

# Sidebar Credentials Section
st.sidebar.header("🔑 Credentials")
CLIENT_ID = st.sidebar.text_input("Flipkart Client ID", value="9453445160676a14979656b0a72b7b077390")
CLIENT_SECRET = st.sidebar.text_input("Flipkart Client Secret", type="password")
CLAUDE_KEY = st.sidebar.text_input("Claude API Key", type="password")

st.sidebar.divider()
# Mode Selection Switch
mode = st.sidebar.radio("Select Mode:", ["Demo / Testing Mode", "Live Claude API Mode"])

if 'ai_recommendations' not in st.session_state:
    st.session_state['ai_recommendations'] = None

# Sample Data
sample_orders_data = {
    "total_orders_today": 42,
    "pending_dispatch": 15,
    "high_return_skus": ["SKU_TSHIRT_RED_M", "SKU_SHOES_BLACK_9"],
    "low_stock_warnings": [{"item": "Wireless Earbuds v2", "current_stock": 3, "recommended_buffer": 20}],
    "ad_campaigns": [{"campaign_name": "Summer_Sale_Ads", "spend_inr": 1500, "roi": 1.2, "status": "NEEDS_OPTIMIZATION"}]
}

if st.button("🚀 Fetch Data & Run Claude AI Analysis"):
    if mode == "Live Claude API Mode":
        if not CLAUDE_KEY:
            st.error("❌ Kripya Left sidebar mein Claude API Key bharein!")
        else:
            with st.spinner("Connecting to Live Claude AI..."):
                try:
                    client = anthropic.Anthropic(api_key=CLAUDE_KEY)
                    prompt = f"Analyze Flipkart Store Data: {json.dumps(sample_orders_data)}. Give actionable inventory, return & ads strategy."
                    response = client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state['ai_recommendations'] = response.content[0].text
                except Exception as e:
                    st.error(f"❌ Claude API Error: {str(e)}")
    else:
        # Demo Mode Logic
        with st.spinner("Simulating Claude AI Analysis..."):
            time.sleep(1)
            st.session_state['ai_recommendations'] = """
### 🚨 Critical Inventory Alerts
* **Wireless Earbuds v2:** Current stock is **3 units**. Reorder immediately to avoid stockout penalty.

---

### 📉 High Return Risk Warning & Action Plan
* **SKU_TSHIRT_RED_M:** High return rate (28%). Size description update recommended.

---

### 💰 Ad Campaign ROI Optimization
* **Summer_Sale_Ads:** ROI is **1.2**. Recommended to optimize keywords and lower bids by 15%.
"""

if st.session_state['ai_recommendations']:
    st.subheader("🧠 Claude's Actionable Insights")
    st.markdown(st.session_state['ai_recommendations'])
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ APPROVE & PUSH TO FLIPKART"):
            st.success("🎉 Actions Approved!")
    with col2:
        if st.button("❌ REJECT CHANGES"):
            st.info("Actions Rejected.")