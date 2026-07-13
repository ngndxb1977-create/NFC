// --- VEHICLE MODELS (example subset, extend as needed) ---
const vehicleModels = [
  { code: "MOP61", name: "Montero P61", year: 2025, basePrice: 0 }, // fill basePrice
  { code: "P61", name: "Montero P61", year: 2026, basePrice: 0 },
  { code: "XPHL", name: "Xpander HL", year: 2026, basePrice: 0 },
  // ...add all from "Combined 2025-2026" sheet
];

// --- BANK ROI TABLE (from Bank Details sheet) ---
const bankInterestTable = [
  {
    bank: "DIB Local GVH",
    brackets: [
      { min: 5000, max: 9999, roi: 0.0325 },
      { min: 10000, max: 14999, roi: 0.03 },
      { min: 15000, max: 24999, roi: 0.0225 },
      { min: 25000, max: 34999, roi: 0.0215 },
      { min: 35000, max: 99999, roi: 0.0199 },
    ],
  },
  {
    bank: "SIB STL-Local",
    brackets: [
      { min: 5000, max: 9999, roi: 0.0249 },
      { min: 10000, max: 19999, roi: 0.0219 },
      { min: 20000, max: 34999, roi: 0.0209 },
      { min: 35000, max: 49999, roi: 0.0189 },
      { min: 50000, max: 99999, roi: 0.0179 },
    ],
  },
  // ...add all banks from your Bank Details sheet
];

// --- RMC TABLE (example subset, from RMC sheet) ---
const rmcTable = [
  {
    code: "MOP61",
    rmc10_40: 4300,
    rmc10_60: 5200,
    rmc10_70: 5900,
    rmc10_100: 9300,
  },
  {
    code: "XPHL",
    rmc10_40: 4500,
    rmc10_60: 5400,
    rmc10_70: 6100,
    rmc10_100: 9700,
  },
  // ...add all rows
];

// --- EMI FACTORS (from MY-2025 / MY-2026 sheets) ---
// These are sample factors; adjust to match your exact Excel row.
const emiFactors = {
  "2YRS": 0.0339,
  "3YRS": 0.0678,
  "4YRS": 0.1017,
  "5YRS": 0.0, // fill if available
};
