import streamlit as st
from docx import Document
from docx.shared import Inches
import io

st.set_page_config(page_title="Perito AI", layout="centered")

st.title("🛡️ Assistente Perito Professionale")

# 1. ANAGRAFICA (Risparmio tempo: inserimento unico)
with st.container():
    col1, col2 = st.columns(2)
    n_pratica = col1.text_input("Numero Pratica")
    assicurato = col2.text_input("Nome Assicurato")

# 2. NOTE (Risparmio tempo: dettatura vocale invece di scrittura)
st.subheader("📝 Descrizione Danni")
st.caption("Consiglio: usa l'icona del microfono sulla tastiera del telefono per dettare.")
note_tecniche = st.text_area("Inserisci i rilievi tecnici:", height=150)

# 3. FOTO (Risparmio tempo: impaginazione automatica)
st.subheader("📸 Allegati Fotografici")
foto_files = st.file_uploader("Carica o scatta foto", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

# 4. GENERAZIONE (Il risparmio del 40% avviene qui)
if st.button("🚀 Genera e Scarica Perizia Word"):
    if not n_pratica or not note_tecniche:
        st.error("Inserisci Numero Pratica e Descrizione per scaricare il file.")
    else:
        doc = Document()
        doc.add_heading(f"Perizia Tecnica - Pratica {n_pratica}", 0)
        doc.add_paragraph(f"Assicurato: {assicurato}")
        
        doc.add_heading('Rilievi Tecnici Riscontrati', level=1)
        doc.add_paragraph(note_tecniche)
        
        if foto_files:
            doc.add_heading('Documentazione Fotografica', level=1)
            for f in foto_files:
                img_stream = io.BytesIO(f.read())
                doc.add_paragraph(f"Allegato: {f.name}")
                doc.add_picture(img_stream, width=Inches(3.5)) # Impagina 2 foto per pagina circa
        
        # Generazione file in memoria
        buffer = io.BytesIO()
        doc.save(buffer)
        st.download_button(
            label="⬇️ Clicca qui per scaricare il Word",
            data=buffer.getvalue(),
            file_name=f"Perizia_{n_pratica}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.success("Documento pronto!")
