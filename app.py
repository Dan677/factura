import streamlit as st
from fpdf import FPDF
from datetime import datetime

# 1. INIȚIALIZARE SESSION STATE
if 'rows' not in st.session_state:
    st.session_state.rows = [{"desc": "50*20", "qty": 1.0, "rate": 1000.0}]

# 2. CLASA PDF
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

# 3. CONFIGURARE PAGINĂ STREAMLIT
st.set_page_config(page_title="Generator Facturi", page_icon="📄")
st.title("📄 Pro Invoice Mobile")

# 4. DATE PRINCIPALE
col1, col2 = st.columns(2)
inv_nr = col1.text_input("INV Number", "31")
date_val = col2.text_input("Date", datetime.now().strftime("%d %b %Y"))
client_name = col1.text_input("Client Name", "Guest Express")
client_email = col2.text_input("Client Email", "info@guestex.com")

st.markdown("### Produse")

# 5. TABEL PRODUSE
for i, item in enumerate(st.session_state.rows):
    c1, c2, c3 = st.columns([3, 1, 1])
    st.session_state.rows[i]['desc'] = c1.text_input(f"Description {i+1}", value=item['desc'], key=f"d{i}")
    st.session_state.rows[i]['qty'] = c2.number_input(f"Qty {i+1}", value=float(item['qty']), key=f"q{i}")
    st.session_state.rows[i]['rate'] = c3.number_input(f"Rate £ {i+1}", value=float(item['rate']), key=f"r{i}")

if st.button("➕ Add Row"):
    st.session_state.rows.append({"desc": "", "qty": 1.0, "rate": 0.0})
    st.rerun()

# 6. GENERARE ȘI DESCARCARE PDF
if st.button("GENERATE PDF", type="primary"):
    try:
        pdf = FacturaPDF()
        pdf.add_page()
        total_general = 0
        
        # Detalii Bill To
        pdf.set_y(40)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 5, f"BILL TO: {client_name}", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 5, f"Email: {client_email}", ln=True)
        pdf.cell(0, 5, f"Invoice Nr: {inv_nr}", ln=True)
        pdf.cell(0, 5, f"Date: {date_val}", ln=True)

        # Tabel Produse
        pdf.set_y(80)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("helvetica", "B", 9)
        pdf.cell(10, 8, "#", border="B", fill=True)
        pdf.cell(80, 8, "Item Description", border="B", fill=True)
        pdf.cell(30, 8, "Qty", border="B", fill=True, align="C")
        pdf.cell(30, 8, "Rate", border="B", fill=True, align="C")
        pdf.cell(40, 8, "Amount", border="B", fill=True, align="R")
        pdf.ln()

        for idx, item in enumerate(st.session_state.rows, 1):
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
        pdf.cell(150, 10, "TOTAL GBP ", align="R")
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

        # --- SOLUȚIA PENTRU EROAREA DE BINARY DATA ---
        # Output sub formă de bytes direct
        pdf_raw = pdf.output(dest='S')
        
        # Conversie forțată în obiectul 'bytes' pe care Streamlit îl adoră
        final_pdf = bytes(pdf_raw)

        st.success("PDF generat! Click mai jos pentru salvare:")
        st.download_button(
            label="📥 Download PDF Now", 
            data=final_pdf, 
            file_name=f"Factura_{inv_nr}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Eroare critică: {e}")
