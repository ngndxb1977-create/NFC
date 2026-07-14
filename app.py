import streamlit as st
import pandas as pd

# Page theme configuration
st.set_page_config(
    page_title="Automotive Finance Calculator Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. DATA CATALOGS ---
VEHICLE_CATALOG = {
    "Attrage G16 (MY-2025)": {"base_price": 40400, "year": "2025"},
    "Destinator PR (MY-2026)": {"base_price": 95900, "year": "2026"}
}

ADDONS_CATALOG = {
    "2025": [
        {"name": "FO Ceramic+ Intr&Extr CeramicGold WdwTnt", "default_price": 0.0, "checked": False},
        {"name": "FO Exterior ceramic All Cars SCOTCHGUARD", "default_price": 0.0, "checked": False},
        {"name": "Extended Warranty", "default_price": 0.0, "checked": False},
        {"name": "VRI", "default_price": 1590.58, "checked": True},
        {"name": "Vehicle Insurance", "default_price": 3625.00, "checked": True},
        {"name": "RMC-10-70KMS", "default_price": 5400.00, "checked": True}
    ],
    "2026": [
        {"name": "FO Ceramic+ Intr&Extr CeramicGold WdwTnt", "default_price": 2700.00, "checked": True},
        {"name": "FO Exterior ceramic All Cars SCOTCHGUARD", "default_price": 0.0, "checked": False},
        {"name": "Extended Warranty", "default_price": 2000.00, "checked": True},
        {"name": "VRI", "default_price": 3722.92, "checked": True},
        {"name": "Vehicle Insurance", "default_price": 4081.14, "checked": True},
        {"name": "RMC-10-70KMS", "default_price": 6600.00, "checked": True}
    ]
}

STANDARD_INTEREST_RATE = 0.0249
SUBVENTION_MULTIPLIERS = {1: 0.0000, 2: 0.0339, 3: 0.0339, 4: 0.0678, 5: 0.1017}


# --- 2. ADVANCED FINANCIAL ENGINE (UPDATED) ---
def calculate_deal_metrics(base_price, year, selected_addons, dp_percentage):

    # VAT
    vat_amount = base_price * 0.05
    vehicle_with_vat = base_price + vat_amount

    # Separate addons into categories
    insurance_rate = 0.0
    vri_rate = 0.0
    other_addons_total = 0.0

    for item in selected_addons:
        name = item["name"].lower()
        price = item["price"]

        if "vehicle insurance" in name:
            insurance_rate = price / (base_price + vat_amount + (sum(a["price"] for a in selected_addons) - price))
        elif "vri" in name:
            vri_rate = price / (base_price + vat_amount + (sum(a["price"] for a in selected_addons) - price))
        else:
            other_addons_total += price

    # Insurance base (EXCLUDING Insurance & VRI)
    insurance_base = base_price + vat_amount + other_addons_total

    # Correct recalculation
    insurance_amount = insurance_base * insurance_rate
    vri_amount = insurance_base * vri_rate

    # Full value (used for down payment)
    full_value = vehicle_with_vat + other_addons_total + insurance_amount + vri_amount

    # Down payment
    down_payment = full_value * (dp_percentage / 100)

    # Finance amount
    finance_amount = full_value - down_payment

    # EMI Matrix
    tenure_matrix = []
    for years in [1, 2, 3, 4, 5]:
        months = years * 12

        total_interest = finance_amount * STANDARD_INTEREST_RATE * years
        standard_emi = (finance_amount + total_interest) / months

        sub_factor = SUBVENTION_MULTIPLIERS[years]
        subvention_discount = finance_amount * sub_factor
        subvented_emi = (finance_amount - subvention_discount + total_interest) / months

        tenure_matrix.append({
            "years": years,
            "months": months,
            "standard_emi": round(standard_emi, 2),
            "subvented_emi": round(subvented_emi, 2),
            "subvention_discount": round(subvention_discount, 2)
        })

    return {
        "base_price": base_price,
        "vat_amount": vat_amount,
        "insurance_amount": round(insurance_amount, 2),
        "vri_amount": round(vri_amount, 2),
        "other_addons_total": round(other_addons_total, 2),
        "full_value": round(full_value, 2),
        "down_payment": round(down_payment, 2),
        "finance_amount": round(finance_amount, 2),
        "tenure_matrix": tenure_matrix
    }


# --- 3. STREAMLIT UI ---
st.title("Automotive Finance Calculator Dashboard")

vehicle_choice = st.selectbox("Select Vehicle", list(VEHICLE_CATALOG.keys()))
vehicle_info = VEHICLE_CATALOG[vehicle_choice]

base_price = vehicle_info["base_price"]
year = vehicle_info["year"]

st.subheader("Addons")
selected_addons = []

for addon in ADDONS_CATALOG[year]:
    checked = st.checkbox(addon["name"], value=addon["checked"])
    price = st.number_input(f"Price for {addon['name']}", value=float(addon["default_price"]))
    if checked:
        selected_addons.append({"name": addon["name"], "price": price})

dp_percentage = st.slider("Down Payment %", 0, 50, 20)

results = calculate_deal_metrics(base_price, year, selected_addons, dp_percentage)

st.subheader("Deal Summary")
st.write(results)

st.subheader("EMI Matrix")
emi_df = pd.DataFrame(results["tenure_matrix"])
st.dataframe(emi_df)
