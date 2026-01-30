import streamlit as st
from docx import Document
from docx.shared import Inches
import io

st.set_page_config(page_title="Perito Digital Assistant", layout="centered")

st.title("🛡️ Assistente Peritale Pro")
st.subheader("Automazione Report Post-Sopralluogo")

# --- SEZIONE 1: ANAGRAFICA ---
with st.container():
    n_pratica = st.text_input("Numero Pratica / Sinistro")
    assicurato = st.text_input("Nome Assicurato")

# --- SEZIONE 2: NOTE E DESCRIZIONE ---
st.info("💡 Usa la dettatura vocale dello smartphone per compilare il campo sotto.")
note_tecniche = st.text_area("Descrizione Danni e Rilievi:", height=200)

# --- SEZIONE 3: FOTO ---
st.subheader("📸 Documentazione Fotografica")
foto_caricate = st.file_uploader("Seleziona o scatta le foto", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

# --- SEZIONE 4: GENERAZIONE E DOWNLOAD ---
if st.button("🚀 Genera Report Completo"):
    if not n_pratica or not note_tecniche:
        st.error("Inserire Numero Pratica e Descrizione Danni per procedere.")
    else:
        doc = Document()
        doc.add_heading(f"Relazione Tecnica - Pratica {n_pratica}", 0)
        
        # Tabella Anagrafica
        table = doc.add_table(rows=1, cols=2)
        table.cell(0, 0).text = f"Assicurato: {assicurato}"
        table.cell(0, 1).text = f"Pratica: {n_pratica}"
        
        doc.add_heading('Descrizione Tecnica dei Danni', level=1)
        doc.add_paragraph(note_tecniche)
        
        # Inserimento Immagini
        if foto_caricate:
            doc.add_heading('Allegato Fotografico', level=1)
            for foto in foto_caricate:
                # Converte l'upload in un flusso leggibile da docx
                image_stream = io.BytesIO(foto.read())
                doc.add_paragraph(f"Foto: {foto.name}")
                doc.add_picture(image_stream, width=Inches(4)) # Ridimensiona auto a 4 pollici
        
        # Preparazione file per download
        target_stream = io.BytesIO()
        doc.save(target_stream)
        
        st.success("✅ Report generato con successo!")
        st.download_button(
            label="⬇️ Scarica File Word",
            data=target_stream.getvalue(),
            file_name=f"Perizia_{n_pratica}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
