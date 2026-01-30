import streamlit as st
from docx import Document
from docx.shared import Inches
import io

st.set_page_config(page_title="Perito AI Assistant", layout="centered")

st.title("🛡️ Assistente Perito: Report Veloce")
st.write("Compila i campi e scatta le foto per generare il Word istantaneamente.")

# Sezione Dati - Elimina la necessità di formattare l'intestazione a mano
with st.container():
    col1, col2 = st.columns(2)
    n_pratica = col1.text_input("N. Pratica")
    assicurato = col2.text_input("Nome Assicurato")

# Sezione Note - Qui il perito risparmia tempo con la dettatura vocale
st.subheader("📝 Descrizione Danni")
note_tecniche = st.text_area("Usa il microfono della tastiera per dettare i rilievi:", height=150)

# Sezione Foto - Elimina il caricamento e ridimensionamento manuale su PC
st.subheader("📸 Allegati Fotografici")
foto_files = st.file_uploader("Carica o scatta foto dei danni", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if st.button("🚀 Genera e Scarica Report Word"):
    if not n_pratica or not note_tecniche:
        st.error("Inserire almeno N. Pratica e Descrizione Danni.")
    else:
        doc = Document()
        doc.add_heading(f"Perizia Tecnica - Pratica {n_pratica}", 0)
        doc.add_paragraph(f"Assicurato: {assicurato}")
        
        doc.add_heading('Dettaglio Rilievi', level=1)
        doc.add_paragraph(note_tecniche)
        
        if foto_files:
            doc.add_heading('Documentazione Fotografica', level=1)
            for f in foto_files:
                img_stream = io.BytesIO(f.read())
                doc.add_paragraph(f"Foto allegata: {f.name}")
                # Ridimensionamento automatico per risparmiare tempo in Word
                doc.add_picture(img_stream, width=Inches(3.5))
        
        buffer = io.BytesIO()
        doc.save(buffer)
        st.download_button(
            label="⬇️ Scarica File Word",
            data=buffer.getvalue(),
            file_name=f"Perizia_{n_pratica}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.success("Documento pronto per l'invio!")
