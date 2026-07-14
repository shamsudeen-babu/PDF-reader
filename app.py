import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv(override=True)

st.set_page_config(page_title="Chat with your PDF")
st.title("Chat with your PDF")
st.write("Upload ONE PDF file and ask it any question!")
st.info("Upload only one PDF at a time. PDF must contain text, not scanned images.")


@st.cache_resource
def load_embedding_model():

    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

pdf = st.file_uploader("Upload your PDF here", type="pdf", accept_multiple_files=False)

if pdf is not None:
    try:
        with st.spinner("Reading your PDF... please wait"):
            reader = PdfReader(pdf)
            text = ""
            for page in reader.pages:
                try:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted
                except Exception:
                    continue

        if not text.strip():
            st.error("Could not read text from this PDF. Please try a different PDF that contains actual text.")
            st.stop()

        word_count = len(text.split())
        st.success("PDF loaded! Found " + str(word_count) + " words. Ask me anything!")


        pdf_fingerprint = str(word_count) + text[:50]

        if "pdf_fingerprint" not in st.session_state or st.session_state.pdf_fingerprint != pdf_fingerprint:
            with st.spinner("Indexing your PDF for smart search... this happens once per file"):
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                chunks = splitter.split_text(text)


                vector_store = FAISS.from_texts(chunks, embedding_model)

                st.session_state.vector_store = vector_store
                st.session_state.pdf_fingerprint = pdf_fingerprint

        question = st.text_input("Type your question here and press Enter:")

        if question:
            with st.spinner("Finding your answer..."):

                relevant_chunks = st.session_state.vector_store.similarity_search(question, k=3)
                context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
                context = context[:6000]  # Hard cap: ~1500 tokens, well under 8000 TPM limit

                try:
                    llm = ChatGroq(
                        model="openai/gpt-oss-20b",
                        temperature=0,
                        api_key=os.environ.get("GROQ_API_KEY")
                    )
                    prompt = ChatPromptTemplate.from_template(
                        "You are a helpful assistant. Use the document below to answer the question.\n"
                        "If the answer is not in the document, say I could not find that in the PDF.\n\n"
                        "Document:\n{context}\n\n"
                        "Question: {question}\n\n"
                        "Answer:"
                    )
                    chain = prompt | llm | StrOutputParser()
                    answer = chain.invoke({"context": context, "question": question})

                    st.write("### Answer:")
                    st.write(answer)

                
                    with st.expander("See which parts of the PDF were used to answer this"):
                        for i, chunk in enumerate(relevant_chunks):
                            st.write(f"*Chunk {i+1}:*")
                            st.write(chunk.page_content[:300] + "...")
                            st.write("---")

                    st.write("---")
                    st.caption("Ask another question in the box above!")
                except Exception as e:
                    st.error("AI error. Please try again in a few seconds.")
                    st.error(f"DEBUG - actual error: {e}")
    except Exception as e:
        st.error("Could not read this PDF. Please try a different file.")