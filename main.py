import streamlit as st
from docx import Document
from docx.shared import Inches
import io
from PIL import Image

st.set_page_config(page_title="Assistente Perito IA", layout="wide")
st.title("🛡️ Smart Assistant per Periti")
st.write("Obiettivo: Riduzione 40% tempi di redazione")

with st.expander("Dati Identificativi", expanded=True):
    col1, col2 = st.columns(2)
    n_pratica = col1.text_input("Numero Pratica")
    assicurato = col2.text_input("Nome Assicurato")

st.subheader("📸 Caricamento Foto Danni")
foto_files = st.file_uploader(
    "Trascina qui le foto del sopralluogo",
    accept_multiple_files=True,
    type=["jpg", "png", "jpeg"]
)

# Preview (facoltativa ma utile sul campo)
if foto_files:
    st.caption(f"Foto caricate: {len(foto_files)}")
    st.image(foto_files, width=250)

st.subheader("📝 Note dal Campo")
note_dettate = st.text_area(
    "Inserisci qui la trascrizione vocale o appunti rapidi:",
    placeholder="Es: Paraurti anteriore destro deformato, fari funzionanti..."
)

def safe_filename(s: str) -> str:
    return "".join(c for c in s if c.isalnum() or c in ("-", "_")).strip("_-") or "pratica"

if st.button("🚀 Genera Bozza Relazione Word"):
    if not n_pratica:
        st.error("Inserisci almeno il numero pratica.")
    else:
        doc = Document()
        doc.add_heading(f"Relazione Tecnica - Pratica {n_pratica}", 0)
        if assicurato:
            doc.add_paragraph(f"Assicurato: {assicurato}")

        doc.add_heading("Descrizione Danni", level=1)
        if note_dettate.strip():
            doc.add_paragraph(note_dettate.strip())
        else:
            doc.add_paragraph("—")

        if foto_files:
            doc.add_heading("Documentazione fotografica", level=1)
            for f in foto_files:
                # Ridimensionamento conservativo
                img = Image.open(f)
                img = img.convert("RGB")
                img.thumbnail((1600, 1600))

                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                buf.seek(0)

                doc.add_paragraph(f.name)
                doc.add_picture(buf, width=Inches(5.8))

        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)

        st.download_button(
            label="⬇️ Scarica Relazione .docx",
            data=bio,
            file_name=f"Perizia_{safe_filename(n_pratica)}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
