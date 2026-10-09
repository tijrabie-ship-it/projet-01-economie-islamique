# app.py

from flask import Flask, render_template, request
import PyPDF2
from docx import Document

# استدعاء جميع الدوال من ملف models.py
from models import (
    calculate_value_added, 
    analyze_contract_arabert_deep, 
    calculate_riba_value_added,
    simulate_zakat_impact,
    compare_financing_systems
)

app = Flask(__name__)

def extract_text_from_file(file):
    """دالة مساعدة لاستخراج النص من ملفات PDF و Word"""
    text = ""
    filename = file.filename.lower()
    try:
        if filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"حدث خطأ أثناء قراءة الملف: {e}")
    return text

# ==========================================
# مسارات النموذج الأول (العقود، القيمة المضافة، الربا)
# ==========================================

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate_va', methods=['POST'])
def calculate_va():
    try:
        t_type = request.form.get('transaction_type')
        q = float(request.form.get('quantity', 0))
        p1 = float(request.form.get('price_1', 0))
        p2 = float(request.form.get('price_2', 0))
        va_result = calculate_value_added(t_type, q, p1, p2)
    except ValueError:
        va_result = {"va": 0, "status": "خطأ", "message": "الرجاء إدخال أرقام صحيحة."}
    return render_template('index.html', va_result=va_result)

@app.route('/analyze_nlp', methods=['POST'])
def analyze_nlp():
    contract_text = request.form.get('contract_text', '')
    file = request.files.get('contract_file')
    
    if file and file.filename != '':
        extracted_text = extract_text_from_file(file)
        contract_text = extracted_text + "\n\n" + contract_text
        
    if contract_text.strip():
        nlp_result = analyze_contract_arabert_deep(contract_text)
    else:
        nlp_result = {
            "risk_level": "تنبيه", 
            "finding": "لم يتم إدخال بيانات", 
            "explanation": "الرجاء رفع ملف العقد أو كتابة النص للتحليل."
        }
    return render_template('index.html', nlp_result=nlp_result)

@app.route('/calculate_riba', methods=['POST'])
def calculate_riba():
    try:
        is_same_nature = request.form.get('is_same_nature') == 'yes'
        is_delayed = request.form.get('is_delayed') == 'yes'
        q1 = float(request.form.get('quantity_1', 0))
        q2 = float(request.form.get('quantity_2', 0))
        p1 = float(request.form.get('price_1', 0))
        p2 = float(request.form.get('price_2', 0))
        riba_result = calculate_riba_value_added(is_same_nature, q1, q2, p1, p2, is_delayed)
    except ValueError:
        riba_result = {"va": 0, "status": "خطأ", "type": "", "message": "الرجاء إدخال أرقام صحيحة."}
    return render_template('index.html', riba_result=riba_result)

# ==========================================
# مسارات النموذج الثاني (الزكاة والمشاركة PLS)
# ==========================================

@app.route('/zakat_pls_dashboard', methods=['GET', 'POST'])
def zakat_pls_dashboard():
    zakat_results = None
    finance_results = None
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'zakat':
            try:
                wealth = float(request.form.get('wealth', 300000))
                poor_count = int(request.form.get('poor_count', 70))
                poor_income = float(request.form.get('poor_income', 2500))
                zakat_results = simulate_zakat_impact(wealth, poor_count, poor_income)
            except ValueError:
                pass # يمكن إضافة معالجة للأخطاء هنا
                
        elif form_type == 'finance':
            try:
                p1 = float(request.form.get('p1', 10000))
                p2 = float(request.form.get('p2', 12000))
                revenue = float(request.form.get('revenue', 50000))
                cost = float(request.form.get('cost', 30000))
                phi = float(request.form.get('phi', 0.4))
                finance_results = compare_financing_systems(p1, p2, revenue, cost, phi)
            except ValueError:
                pass
                
    return render_template('zakat_pls.html', zakat_results=zakat_results, finance_results=finance_results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)