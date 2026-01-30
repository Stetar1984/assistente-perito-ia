# assistente-perito-ia
Strumento IA per l'automazione della perizia assicurativa
import streamlit as st
from docx import Document
import io

st.set_page_config(page_title="Assistente Perito IA", layout="wide")

st.title("🛡️ Smart Assistant per Periti")
st.write("Obiettivo: Riduzione 40% tempi di redazione")

# --- SEZIONE 1: DATI SINISTRO ---
with st.expander("Dati Identificativi", expanded=True):
    col1, col2 = st.columns(2)
    n_pratica = col1.text_input("Numero Pratica")
    assicurato = col2.text_input("Nome Assicurato")

# --- SEZIONE 2: DOCUMENTAZIONE FOTOGRAFICA ---
st.subheader("📸 Caricamento Foto Danni")
foto_files = st.file_uploader("Trascina qui le foto del sopralluogo", accept_multiple_files=True, type=['jpg', 'png', 'jpeg'])

# --- SEZIONE 3: NOTE TECNICHE E VOCALI ---
st.subheader("📝 Note dal Campo")
note_dettate = st.text_area("Inserisci qui la trascrizione vocale o appunti rapidi:", 
                            placeholder="Es: Paraurti anteriore destro deformato, fari funzionanti...")

# --- SEZIONE 4: GENERAZIONE REPORT ---
if st.button("🚀 Genera Bozza Relazione Word"):
    if not n_pratica:
        st.error("Inserisci almeno il numero pratica.")
    else:
        doc = Document()
        doc.add_heading(f'Relazione Tecnica - Pratica {n_pratica}', 0)
        doc.add_paragraph(f"Assicurato: {assicurato}")
        doc.add_heading('Descrizione Danni', level=1)
        doc.add_paragraph(note_dettate)
        
        # Salvataggio in memoria per il download
        bio = io.BytesIO()
        doc.save(bio)
        st.download_button(
            label="⬇️ Scarica Relazione .docx",
            data=bio.getvalue(),
            file_name=f"Perizia_{n_pratica}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.success("Relazione generata con successo!")
