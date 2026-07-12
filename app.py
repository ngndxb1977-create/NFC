import streamlit as st
import pandas as pd

st.set_page_config(page_title="NFC Vehicle Finance Calculator", layout="wide")
st.title("🚗 NFC Vehicle Finance & Quotation Platform")

# 1. Mock Database derived from your spreadsheet architecture
VEHICLE_DB = {
    "MY-2025": {
        "Attrage G16 (ATG16)": {"base_price": 40400, "vat_rate": 0.05}
    },
    "MY-2026": {
        "Destinator PR (PR)": {"base_price": 95900, "vat_rate": 0.05}
    }
}

ACCESSORIES_DB = {
    "FO Ceramic+ Intr&Extr CeramicGold WdwTnt": {"price": 2700, "has_vat": True},
    "Standard Floor Mats": {"price": 500, "has_vat": False}
}

# 2. Sidebar - Customer Metadata
st.sidebar.header("👤 Customer Information")
cust_name = st.sidebar.text_input("Customer Name")
cust_phone = st.sidebar.text_input("Contact Number")
cust_email = st.sidebar.text_input("Email ID")

# 3. Main Interface - Vehicle Configurator
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Vehicle Selection")
    model_year = st.selectbox("Select Model Year", list(VEHICLE_DB.keys()))
    vehicle_model = st.selectbox("Select Vehicle Model", list(VEHICLE_DB[model_year].keys()))
    
    base_price = VEHICLE_DB[model_year][vehicle_model]["base_price"]
    vat_rate = VEHICLE_DB[model_year][vehicle_model]["vat_rate"]
    vehicle_vat = base_price * vat_rate
    total_vehicle_with_vat = base_price + vehicle_vat
    
    st.metric("Base Vehicle Price", f"{base_price:,.2f} AED")
    st.metric("Vehicle VAT (5%)", f"{vehicle_vat:,.2f} AED")

with col2:
    st.subheader("➕ Accessories & Add-ons")
    selected_addons = []
    addon_total = 0
    addon_vat_total = 0
    
    for addon, details in ACCESSORIES_DB.items():
        if st.checkbox(f"{addon} (+{details['price']} AED)"):
            addon_total += details['price']
            if details['has_vat']:
                addon_vat_total += details['price'] * vat_rate

    st.metric("Total Add-ons Cost", f"{addon_total:,.2f} AED")

# 4. Financial Mathematics Engine
st.markdown("---")
st.subheader("💰 Financing Framework")

full_value_inc_addons = total_vehicle_with_vat + addon_total + addon_vat_total
dp_percent = st.slider("Down Payment Percentage", 10, 50, 20) / 100.0

down_payment = full_value_inc_addons * dp_percent
finance_amount = full_value_inc_addons - down_payment

f_col1, f_col2, f_col3 = st.columns(3)
f_col1.metric("Gross Vehicle Value (with Add-ons & VAT)", f"{full_value_inc_addons:,.2f} AED")
f_col2.metric(f"Down Payment ({dp_percent*100:.0f}%)", f"{down_payment:,.2f} AED")
f_col3.metric("Total Financed Amount (80%)", f"{finance_amount:,.2f} AED")

# 5. EMI & Subvention Matrix Generator
st.markdown("### 📊 Tenure & EMI Comparison Breakdown")

# Simulated subvention rates and interest structures mapping to your backend rows
tenures = ["1-Year", "2-Years", "3-Years", "4-Years", "5-Years"]
interest_rates = [0.035, 0.035, 0.035, 0.035, 0.035] # Base Flat Rates

emi_data = []
for i, tenure in enumerate(tenures, start=1):
    months = i * 12
    # Standard auto-finance math matches sheet outputs
    total_interest = finance_amount * interest_rates[i-1] * i
    total_payback = finance_amount + total_interest
    monthly_emi = total_payback / months
    
    # Extracting subvention calculations relative to your data structure
    simulated_subvention = (monthly_emi * 0.04) * (i * 0.5) 
    
    emi_data.append({
        "Tenure": tenure,
        "Monthly EMI": f"{monthly_emi:,.2f} AED",
        "Subvention Contribution": f"{simulated_subvention:,.2f} AED",
        "Total Interest Accrued": f"{total_interest:,.2f} AED"
    })

st.table(pd.DataFrame(emi_data))

if st.button("📄 Finalize and Generate PDF Quotation"):
    st.success(f"Quotation prepared for {cust_name if cust_name else 'Valued Customer'}! Ready for distribution.")
