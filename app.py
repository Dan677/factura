import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Clasa pentru PDF
class FacturaPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 12)
        self.cell(0, 5, "Lucian Popit", ln=True)
        self.set_font("helvetica", "", 10)
        self.cell(0, 5, "cristi80cristi@yahoo.com", ln=True)
        self.cell(0, 5, "Orchard Avenue, Ashford, UK", ln=True)
        self.cell(0, 5, "VAT Number: 230", ln=True)
        self.set_y(10)
        self.set_font("helvetica", "B", 20)
        self.cell(0, 10, "INVOICE  ", align="R", ln=True)

st.set_page_config(page_title="Generator Facturi", layout="centered")
st.title("📄 Pro Invoice Mobile")

# Date principale
col1, col2 = st.columns(2)
inv_nr = col1.text_input("INV Number", "31")
date_val = col2.text_input("Date", datetime.now().strftime("%d %b %Y"))
client_name = col1.text_input("Client Name", "Guest Express")
client_email = col2.text_input("Client Email", "info@guestex.com")

st.markdown("### Items")

# Inițializare listă items dacă nu există
if 'items' not in st.session_state:
    st.session_state.items = [{"desc": "50*20", "qty": 1.0, "rate": 1000.0}]

# Tabel coloane
for i, item in enumerate(st.session_state.items):
    c1, c2, c3 = st.columns([2, 1, 1])
    st.session_state.items[i]['desc'] = c1.text_input(f"Description", value=item['desc'], key=f"d{i}")
    st.session_state.items[i]['qty'] = c2.number_input(f"Qty", value=float(item['qty']), key=f"q{i}")
    st.session_state.items[i]['rate'] = c3.number_input(f"Rate (£)", value=float(item['rate']), key=f"r{i}")

col_btns = st.columns(2)
if col_btns[0].button("➕ Add Row"):
    st.session_state.items.append({"desc": "", "qty": 1.0, "rate": 0.0})
    st.rerun()

if col_btns[1].button("🗑️ Clear All"):
    st.session_state.items = [{"desc": "", "qty": 1.0, "rate": 0.0}]
    st.rerun()

st.divider()

# Generare PDF
if st.button("GENERATE PDF", type="primary", use_container_width=True):
    pdf = FacturaPDF()
    pdf.add_page()
    
    # Detalii Client în PDF
    pdf.set_y(40)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5, f"BILL TO: {client_name}", ln=True)
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, f"Email: {client_email}", ln=True)
    pdf.cell(0, 5, f"Invoice Nr: {inv_nr}", ln=True)
    pdf.cell(0, 5, f"Date: {date_val}", ln=True)
    
    # Header Tabel PDF
    pdf.set_y(70)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", "B", 9)
    pdf.cell(10, 8, "#", border="B", fill=True)
    pdf.cell(80, 8, "Item Description", border="B", fill=True)
    pdf.cell(30, 8, "Qty", border="B", fill=True, align="C")
    pdf.cell(30, 8, "Rate", border="B", fill=True, align="C")
    pdf.cell(40, 8, "Amount", border="B", fill=True, align="R")
    pdf.ln()

    total_general = 0
    for idx, item in enumerate(st.session_state.items, 1):
        amount = item['qty'] * item['rate']
        total_general += amount
        pdf.set_font("helvetica", "", 9)
        pdf.cell(10, 10, str(idx), border="B")
        pdf.cell(80, 10, item['desc'], border="B")
        pdf.cell(30, 10, f"{item['qty']:g}", border="B", align="C")
        pdf.cell(30, 10, f"GBP {item['rate']:.2f}", border="B", align="C")
        pdf.cell(40, 10, f"GBP {amount:.2f}", border="B", align="R")
        pdf.ln()

    pdf.set_font("helvetica", "B", 10)
    pdf.cell(150, 10, "TOTAL GBP", align="R")
    pdf.cell(40, 10, f"{total_general:.2f}", align="R")
    
    # Date bancare
    pdf.ln(15)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5, "Payment Details", ln=True)
    pdf.set_font("helvetica", "", 9)
    pdf.cell(40, 5, "Bank Name:"); pdf.cell(0, 5, "Loyds", ln=True)
    pdf.cell(40, 5, "Account Name:"); pdf.cell(0, 5, "Lc Popit", ln=True)
    pdf.cell(40, 5, "Account Number:"); pdf.cell(0, 5, "011", ln=True)
    pdf.cell(40, 5, "SWIFT/BIC Code:"); pdf.cell(0, 5, "22233", ln=True)

    # Output ca bytes pentru Streamlit
    pdf_bytes = pdf.output() 
    
    st.success("✅ Factura a fost generată!")
    st.download_button(
        label="📥 Download PDF Now",
        data=pdf_bytes,
        file_name=f"Factura_{inv_nr}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

