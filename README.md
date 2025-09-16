# 📦 Sales Order Creator (SAP Integrated)

A web-based tool that allows users to create SAP Sales Orders using either an Excel file upload or a dynamic manual form. Built with Flask (Python) and SAP S/4HANA OData integration, the app handles CSRF token management, order line items, pricing elements, and JSON payload submission to SAP.

---

## 🚀 Features

- 📥 Upload Excel file (Header, Items, Pricing)
- ✍️ Manual entry for Sales Order Header, Items, and Pricing
- 🧠 JSON preview before submission
- 🔐 Secure CSRF token management with session cookies
- 📤 Sends POST request to SAP OData API
- ✅ Auto-validation and submission alerts

---

## 🧱 Tech Stack

- Python 3.10+
- Flask
- JavaScript (vanilla)
- HTML + CSS
- XLSX.js (client-side Excel parsing)
- SAP S/4HANA OData v2.0 API

---

## 🗂️ Folder Structure

sales-order-creator/
├── app.py # Flask backend
├── templates/
│ └── index.html # Web interface
├── static/ (optional) # For CSS/JS
├── requirements.txt
├── README.md



---

## 🔧 Setup Instructions

1. Install dependencies:
    ```
    pip install requirements.txt
    ```

2. Run the Flask app:
    ```
    python app.py
    ```

3. Visit:
    ```
    http://localhost:5000
    ```

---

## 📤 API Endpoints

| Method | Endpoint             | Description                         |
|--------|----------------------|-------------------------------------|
| GET    | /get-sales-order     | Fetch CSRF token & sample order     |
| POST   | /create-sales-order  | Submit JSON sales order to SAP      |
| GET    | /get-csrf-token      | Fetch CSRF token (frontend only)    |

---

## 📁 Excel Format

Upload a .xlsx file with 3 sheets:

- Header
  - SalesOrderType, SalesOrganization, DistributionChannel, etc.
- Items
  - SalesOrderItem, Material, Quantity, Unit, etc.
- Pricing
  - SalesOrderItem, ConditionType, RateValue, Currency, etc.

📝 Auto-populates form fields on upload.

---

## 📄 Example JSON Payload

```json
{
  "SalesOrderType": "OR",
  "SalesOrganization": "1710",
  "DistributionChannel": "10",
  "OrganizationDivision": "00",
  "SoldToParty": "1000586",
  "PurchaseOrderByCustomer": "ABC123",
  "to_Item": {
    "results": [
      {
        "SalesOrderItem": "10",
        "Material": "MAT001",
        "RequestedQuantity": "5",
        "RequestedQuantityUnit": "EA",
        "to_PricingElement": {
          "results": [
            {
              "ConditionType": "PR00",
              "ConditionRateValue": "100",
              "ConditionCurrency": "USD"
            }
          ]
        }
      }
    ]
  }
}
