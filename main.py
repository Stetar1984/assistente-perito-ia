import io
from datetime import date

import streamlit as st
from PIL import Image, ImageOps
from docx import Document
from docx.shared import Inches

# ======================================================
# CONFIGURAZIONE APP
# ======================================================
st.set_page_config(
    page_title="PERITIUM",
    layout="wide"
)

st.title("PERITIUM")
st.caption("Redazione assistita del verbale di sopralluogo")

# ======================================================
# FUNZIONI DI SUPPORTO
# ======================================================
def safe_filename(s: str) -> str:
    s = (s or "").strip()
    cleaned = "".join(c for c in s if c.isalnum() or c in ("-", "_"))
    return cleaned.strip("_-") or "pratica"

def normalize_image(uploaded_file, max_side=1600, quality=85) -> io.BytesIO:
    """
    - Correzione orientamento EXIF
    - Ridimensionamento
    - Conversione in JPEG
    """
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.thumbnail((max_side, max_side))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    buf.seek(0)
    return buf

def build_docx(
    n_pratica: str,
    assicurato: str,
    data_sopralluogo: str,
    note: str,
    photos: list
) -> io.BytesIO:

    doc = Document()
    doc.add_heading(f"Verbale di Sopralluogo - Pratica {n_pratica}", level=0)
    doc.add_paragraph(f"Assicurato: {assicurato or '—'}")
    doc.add_paragraph(f"Data sopralluogo: {data_sopralluogo}")

    doc.add_heading("Note tecniche", level=1)
    doc.add_paragraph(note.strip() if note and note.strip() else "—")

    if photos:
        doc.add_heading("Documentazione fotografica", level=1)
        table = doc.add_table(rows=1, cols=2)
        hdr = table.rows[0].cells
        hdr[0].text = "Foto"
        hdr[1].text = "Didascalia"

        for p in photos:
            row = table.add_row().cells
            run = row[0].paragraphs[0].add_run()
            p["img_bytesio"].seek(0)
            run.add_picture(p["img_bytesio"], width=Inches(2.7))
            row[1].text = p["caption"] or p["name"] or "—"

    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out

# ======================================================
# INTERFACCIA UTENTE
# ======================================================
with st.expander("Dati identificativi", expanded=True):
    c1, c2, c3 = st.columns(3)
    n_pratica = c1.text_input("Numero pratica *")
    assicurato = c2.text_input("Assicurato")
    data_sopralluogo = c3.date_input(
        "Data sopralluogo",
        value=date.today()
    ).isoformat()

st.subheader("Note tecniche")
note = st.text_area(
    "Trascrizione vocale / appunti",
    height=140,
    placeholder="Es: Paraurti anteriore dx deformato, fari funzionanti..."
)

st.subheader("Foto danni (con didascalie)")
foto_files = st.file_uploader(
    "Carica foto (JPG / PNG)",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png"]
)

photo_items = []

if foto_files:
    st.caption(f"Foto caricate: {len(foto_files)}")

    for idx, f in enumerate(foto_files, start=1):
        with st.container(border=True):
            colA, colB = st.columns([1, 2])

            colA.image(f, width=220, caption=f.name)

            order = colB.number_input(
                f"Ordine per {f.name}",
                min_value=1,
                max_value=999,
                value=idx,
                step=1,
                key=f"ord_{idx}_{f.name}"
            )

            caption = colB.text_input(
                f"Didascalia per {f.name}",
                key=f"cap_{idx}_{f.name}"
            )

            try:
                img_buf = normalize_image(f)
            except Exception as e:
                st.warning(f"Errore elaborazione {f.name}: {e}")
                continue

            photo_items.append({
                "order": int(order),
                "name": f.name,
                "caption": caption,
                "img_bytesio": img_buf
            })

    photo_items.sort(key=lambda x: x["order"])
else:
    st.info("Carica almeno una foto per abilitare didascalie e ordinamento.")

st.divider()

# ======================================================
# GENERAZIONE DOCX
# ======================================================
if st.button("Genera verbale .docx"):
    if not n_pratica.strip():
        st.error("Il numero pratica è obbligatorio.")
    else:
        docx_bytes = build_docx(
            n_pratica=n_pratica.strip(),
            assicurato=assicurato.strip(),
            data_sopralluogo=data_sopralluogo,
            note=note,
            photos=photo_items
        )

        st.download_button(
            label="Scarica verbale .docx",
            data=docx_bytes,
            file_name=f"PERITIUM_{safe_filename(n_pratica)}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
