import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime
import os

class FacturaPDF(FPDF):
    def header(self):
        # Datele tale conform modelului profesional
        self.set_font("helvetica", "B", 12)
        self.cell(0, 5, "Lucian Popit", ln=True)
        self.set_font("helvetica", "", 10)
        self.cell(0, 5, "cristi80cristi@yahoo.com", ln=True)
        self.cell(0, 5, "Orchard Avenue", ln=True)
        self.cell(0, 5, "Ashford, United Kingdom", ln=True)
        self.cell(0, 5, "VAT Number: 230", ln=True)
        
        self.set_y(10)
        self.set_font("helvetica", "B", 20)
        self.cell(0, 10, "INVOICE  ", align="R", ln=True)
        self.ln(20)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator Facturi Multi-Item")
        self.root.geometry("620x700")
        
        # Secțiune Date Client (Sus)
        frame_top = tk.Frame(root)
        frame_top.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_top, text="INV Number:").grid(row=0, column=0, sticky="w")
        self.entry_nr = tk.Entry(frame_top, width=10); self.entry_nr.insert(0, "31"); self.entry_nr.grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Label(frame_top, text="Date:").grid(row=0, column=2, sticky="w")
        self.entry_data = tk.Entry(frame_top, width=15); self.entry_data.insert(0, datetime.now().strftime("%d %b %Y")); self.entry_data.grid(row=0, column=3, sticky="w", padx=5)
        
        tk.Label(frame_top, text="Client Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_client = tk.Entry(frame_top, width=40); self.entry_client.grid(row=1, column=1, columnspan=3, sticky="w", padx=5)
        
        tk.Label(frame_top, text="Client Email:").grid(row=2, column=0, sticky="w")
        self.entry_email = tk.Entry(frame_top, width=40); self.entry_email.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

        # --- SECTIUNEA MODIFICATA: TABEL CU TITLURI ---
        self.items_label_frame = tk.LabelFrame(root, text="Items")
        self.items_label_frame.pack(pady=15, padx=10, fill="both", expand=True)

        # Headerul tabelului (Etichete deasupra coloanelor)
        self.header_frame = tk.Frame(self.items_label_frame)
        self.header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        tk.Label(self.header_frame, text="Item Description", width=34, anchor="w", font=("Arial", 9, "bold")).pack(side="left")
        tk.Label(self.header_frame, text="Qty", width=8, font=("Arial", 9, "bold")).pack(side="left")
        tk.Label(self.header_frame, text="Rate (GBP)", width=12, font=("Arial", 9, "bold")).pack(side="left")
import streamlit as st
from fpdf import FPDF
from datetime import datetime

class FacturaPDF(FPDF):
    def header(self):
        # Datele tale profesionale
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

# Sistem Multi-Item
if 'items' not in st.session_state:
    st.session_state.items = [{"desc": "50*20", "qty": 1.0, "rate": 1000.0}]

# Tabel cu titluri coloane
for i, item in enumerate(st.session_state.items):
    c1, c2, c3 = st.columns([3, 1, 1])
    item['desc'] = c1.text_input(f"Description {i+1}", value=item['desc'], key=f"d{i}")
    item['qty'] = c2.number_input(f"Qty", value=item['qty'], key=f"q{i}", step=1.0)
    item['rate'] = c3.number_input(f"Rate (£)", value=item['rate'], key=f"r{i}", step=0.01)

if st.button("➕ Add Row"):
    st.session_state.items.append({"desc": "", "qty": 1.0, "rate": 0.0})
    st.rerun()

# Generare PDF
if st.button("GENERATE & DOWNLOAD PDF", type="primary"):
    pdf = FacturaPDF()
    pdf.add_page()
    total_general = 0
    
    # Header Tabel PDF (Gri)
    pdf.set_y(80)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", "B", 9)
    pdf.cell(10, 8, "#", border="B", fill=True)
    pdf.cell(80, 8, "Item Description", border="B", fill=True)
    pdf.cell(30, 8, "Qty", border="B", fill=True, align="C")
    pdf.cell(30, 8, "Rate", border="B", fill=True, align="C")
    pdf.cell(40, 8, "Amount", border="B", fill=True, align="R")
    pdf.ln()

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

    # Totale
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(150, 10, "TOTAL", align="R")
    pdf.cell(40, 10, f"GBP {total_general:.2f}", align="R")
    
    # Datele bancare Loyds
    pdf.ln(15)
    pdf.cell(0, 5, "Payment Details", ln=True)
    pdf.set_font("helvetica", "", 9)
    pdf.cell(40, 5, "Bank Name:"); pdf.cell(0, 5, "Loyds", ln=True)
    pdf.cell(40, 5, "Account Name:"); pdf.cell(0, 5, "Lc Popit", ln=True)
    pdf.cell(40, 5, "Account Number:"); pdf.cell(0, 5, "011", ln=True)
    pdf.cell(40, 5, "SWIFT/BIC Code:"); pdf.cell(0, 5, "22233", ln=True)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 Download PDF", data=pdf_output, file_name=f"Factura_{inv_nr}.pdf")