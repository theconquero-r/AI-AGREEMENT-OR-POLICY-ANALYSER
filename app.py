import streamlit as st
import tempfile
from main import AgreementAnalyzer

st.set_page_config(page_title="Agreement Analyzer", layout="wide")

# ---------------- INIT ----------------
@st.cache_resource
def load_analyzer():
    return AgreementAnalyzer()

analyzer = load_analyzer()

# ---------------- UI ----------------
st.title("📄⚖️ Agreement Analyzer AI")
st.markdown("Upload a legal document and chat with it like ChatGPT 🤖")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Agreement (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name
        file_name = uploaded_file.name

    st.success("✅ File uploaded successfully!")

    # Process button
    if st.button("🚀 Analyze Document"):
        with st.spinner("Processing document..."):

            chunks = analyzer.process_file(file_path,file_name)

            summary = analyzer.generate_summary()

            st.session_state["processed"] = True
            st.session_state["summary"] = summary

            # Reset chat
            st.session_state["messages"] = []

        st.success("✅ Analysis Complete!")

# ---------------- SHOW SUMMARY ----------------
if "processed" in st.session_state and st.session_state["processed"]:

    st.subheader("📄 Summary")
    st.write(st.session_state["summary"])

    st.divider()

    # ---------------- CHAT UI ----------------
    st.subheader("💬 Chat with Agreement")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Show chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input box
    if prompt := st.chat_input("Ask something about the agreement..."):

        # Save user message
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                query_embedding = analyzer.vectorizer.model.encode(prompt)

                results = analyzer.faiss_db.search(query_embedding, top_k=5)

                answer = analyzer.llm.generate_answer(prompt, results)

                st.markdown(answer)

        # Save response
        st.session_state["messages"].append({"role": "assistant", "content": answer})