import streamlit as st
from docx import Document

st.title("Assistente Perito IA - Generazione Report")

# Area di input per il perito
note_campo = st.text_area("Inserisci appunti o trascrizione vocale:")

if st.button("Genera Relazione Formale"):
    # Qui si collegherà l'API di OpenAI per trasformare il testo
    # Per ora creiamo una bozza strutturata
    doc = Document()
    doc.add_heading('Relazione Tecnica di Perizia', 0)
    doc.add_paragraph(f"Note rilevate: {note_campo}")
    
    nome_file = "perizia_bozza.docx"
    doc.save(nome_file)
    
    with open(nome_file, "rb") as file:
        st.download_button("Scarica Documento Word", file, file_name=nome_file)
