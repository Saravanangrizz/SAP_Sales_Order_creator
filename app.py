from flask import Flask, request, jsonify, render_template, session
import os
import pandas as pd
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = 'Gokul_Saro'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)

USERNAME = 'ODATAUSER'
PASSWORD = 'QrN{jkZRGuKBLpVaTcdTtBTaFSjxHoBUguG8UivG'
GET_URL = "https://my404092-api.s4hana.cloud.sap:443/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder('904')?$expand=to_BillingPlan,to_Item,to_Partner,to_PaymentPlanItemDetails,to_PrecedingProcFlowDoc,to_PricingElement,to_RelatedObject,to_SubsequentProcFlowDoc,to_Text"
POST_URL = "https://my404092-api.s4hana.cloud.sap:443/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-csrf-token', methods=['GET'])
def get_csrf_token():
    session_requests = requests.Session()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-csrf-token": "fetch"
    }
    response = session_requests.get(GET_URL, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    csrf_token = response.headers.get("x-csrf-token", "")
    session['csrf_token'] = csrf_token
    session['cookies'] = requests.utils.dict_from_cookiejar(session_requests.cookies)
    return jsonify({"csrf_token": csrf_token})

@app.route('/create-sales-order', methods=['POST'])
def create_sales_order():
    try:
        data = request.get_json()
        csrf_token = session.get('csrf_token', '')
        cookies = session.get('cookies', {})

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-csrf-token": csrf_token
        }

        response = requests.post(
            POST_URL,
            headers=headers,
            cookies=cookies,
            json=data,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            verify=False
        )
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        xl = pd.ExcelFile(path)
        header_df = xl.parse(xl.sheet_names[0])
        item_df = xl.parse(xl.sheet_names[1])
        pricing_df = xl.parse(xl.sheet_names[2]) if len(xl.sheet_names) > 2 else pd.DataFrame()

        return jsonify({
            "header": header_df.to_dict(orient='records'),
            "items": item_df.to_dict(orient='records'),
            "pricing": pricing_df.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
