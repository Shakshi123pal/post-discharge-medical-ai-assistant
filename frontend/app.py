import streamlit as st, requests, os

API = os.environ.get("API_URL","http://localhost:8000")

st.title("🩺 Post-Discharge Medical AI Assistant")
st.caption("For educational use only. Always consult healthcare professionals.")

name = st.text_input("Your full name")
msg = st.text_area("Your message", height=120)

if st.button("Send"):
    r = requests.post(f"{API}/chat", json={"user_name": name or None, "user_message": msg})
    if r.ok:
        data = r.json()
        st.markdown("### Assistant")
        st.write(data["answer"])
        if data.get("from_source")=="web":
            st.info("Source: Web search (latest info)")
        elif data.get("from_source")=="reference":
            st.info("Source: Nephrology reference (RAG)")
        if data.get("citations"):
            with st.expander("Citations / Results"):
                for c in data["citations"]:
                    href = c.get("href")
                    if href: st.write(f"- {c.get('title')} — {href}")
                    else: st.write(f"- {c.get('source')} (chunk {c.get('page_hint')})")
