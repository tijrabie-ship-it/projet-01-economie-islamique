from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# ==========================================
# 1. إعداد وتحميل نموذج الذكاء الاصطناعي (AraBERT)
# ==========================================
tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
model = AutoModelForSequenceClassification.from_pretrained("aubmindlab/bert-base-arabertv02", num_labels=3)


# ==========================================
# 2. دوال تحليل العقود والنصوص
# ==========================================
def analyze_contract_arabert_deep(contract_text):
    """
    تحليل نص العقد البنكي باستخدام القواعد النصية (الكلمات المفتاحية) أولاً،
    ثم استخدام نموذج AraBERT للتحليل العميق إذا لم تكن الشروط واضحة.
    """
    # أ. فحص الخصائص الربوية الصريحة (القواعد النصية)
    riba_explicit = ["فائدة منصوص عليها", "تكلفة ثابتة", "مكافأة ثابتة محددة مسبقاً", "زيادة رأس المال بشكل مستقل"]
    fadl_explicit = ["ذهب بذهب", "فضة بفضة", "مثلاً بمثل", "تبادل نفس الطبيعة مع زيادة"]
    
    for phrase in riba_explicit:
        if phrase in contract_text:
            return {
                "risk_level": "عالي جداً (حرام)",
                "finding": f"اكتشاف شرط ربوي صريح: ({phrase})",
                "explanation": "الربا يُعرّف بأنه فائدة منصوص عليها تعاقدياً وتكلفة ثابتة يتحملها المقترض."
            }
            
    for phrase in fadl_explicit:
        if phrase in contract_text:
            return {
                "risk_level": "عالي (ربا الفضل)",
                "finding": f"شبهة ربا الفضل: ({phrase})",
                "explanation": "يُشترط تكافؤ الكميات وتزامن التبادل لإتمام عملية بيع صحيحة للأشياء من نفس الطبيعة."
            }

    if "خسارة كلية" in contract_text or "تقاسم حقيقي" in contract_text or "حصص متغيرة" in contract_text:
        return {
            "risk_level": "منخفض (مباح/مشاركة)",
            "finding": "توافق مع نظام المشاركة (PLS)",
            "explanation": "هناك تقاسم حقيقي للمخاطر بين الشركاء وهو متوافق مع الشريعة."
        }

    # ب. التحليل العميق باستخدام الذكاء الاصطناعي (AraBERT) للحالات غير الواضحة
    inputs = tokenizer(contract_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    predicted_class = torch.argmax(outputs.logits, dim=-1).item()
    classes = ["عقد صحيح (سلم/استصناع)", "شبهة غرر مرتفعة", "معاملة محظورة (عينة/تورق/ربا)"]
    
    return {
        "risk_level": "تقييم الذكاء الاصطناعي",
        "finding": classes[predicted_class],
        "explanation": "تم تصنيف العقد بناءً على فهم النموذج العميق لسياق المعاملة المكتوبة."
    }


# ==========================================
# 3. دوال الاقتصاد الكلي والقيمة المضافة
# ==========================================
def calculate_value_added(transaction_type, Q, P1, P2):
    """
    حساب القيمة المضافة للاقتصاد الكلي بناءً على نوع العقد.
    """
    result = {"va": 0, "status": "", "message": ""}
    
    if transaction_type == "taqsit":
        va = 2 * Q * (P2 - P1)
        result["va"] = round(va, 2)
        result["status"] = "موجبة (محفزة للنمو)"
        result["message"] = "هذه المعاملة تخلق قيمة مضافة إيجابية للاقتصاد، مما يسهل التعامل التجاري."
        
    elif transaction_type == "eina":
        va = Q * (P2 - P1)
        result["va"] = round(va, 2)
        result["status"] = "سالبة (تدهور اقتصادي)"
        result["message"] = "معاملة محظورة لأنها تؤدي إلى تدهور وتراجع النمو الاقتصادي وتقتطع من القيمة المضافة."
        
    else:
        result["message"] = "نوع المعاملة غير معروف."
        
    return result

def calculate_riba_value_added(is_same_nature, q1, q2, p1, p2, is_delayed):
    """
    النمذجة الرياضية لاكتشاف الربا (الفضل والنسيئة) وحساب أثره على القيمة المضافة.
    """
    result = {"va": 0, "status": "", "type": "", "message": ""}
    
    # حالة ربا الفضل
    if is_same_nature and q1 != q2:
        va = -p1 * (q1 + q2)
        result["va"] = round(va, 2)
        result["status"] = "معاملة محظورة"
        result["type"] = "شبهة ربا الفضل"
        result["message"] = "تبادل شيئين من نفس الطبيعة بكميات مختلفة يقتطع قيماً من الاقتصاد."
        
    # حالة ربا النسيئة
    elif not is_same_nature and q1 == q2 and is_delayed:
        va = -q1 * (p1 + p2)
        result["va"] = round(va, 2)
        result["status"] = "معاملة محظورة"
        result["type"] = "شبهة ربا النسيئة"
        result["message"] = "زيادة الثمن مقابل الأجل دون مبرر حقيقي يطرح قيماً من الاقتصاد."
        
    # حالة القرض الحسن
    elif is_same_nature and q1 == q2 and is_delayed:
        va = 9 * q1
        result["va"] = round(va, 2)
        result["status"] = "معاملة مباحة"
        result["type"] = "قرض حسن (بدون فائدة)"
        result["message"] = "المعاملة تساهم في التكافل الاجتماعي وتضيف قيمة إيجابية غير مباشرة للاقتصاد."
        
    else:
        result["status"] = "يتطلب مراجعة"
        result["message"] = "المعاملة تتطلب معطيات إضافية لتصنيفها بدقة."
        
    return result


# ==========================================
# 4. دوال التكافل والزكاة
# ==========================================
def simulate_zakat_impact(total_wealth_rich, poor_count, years=5, growth_rate=0.05, zakat_rate=0.025):
    """
    محاكاة أثر الزكاة على الدخل الفردي للفقراء وتوزيع الثروة عبر عدة سنوات.
    """
    results = []
    current_wealth = total_wealth_rich
    
    if poor_count <= 0:
        return results # تجنب القسمة على صفر
        
    for year in range(1, years + 1):
        zakat_amount = current_wealth * zakat_rate
        individual_zakat_share = zakat_amount / poor_count
        
        results.append({
            "year": year,
            "rich_wealth": round(current_wealth, 2),
            "zakat_fund": round(zakat_amount, 2),
            "individual_share": round(individual_zakat_share, 2)
        })
        
        current_wealth = current_wealth * (1 + growth_rate)
        
    return results
# أضف هذا الكود إلى ملف models.py

def simulate_zakat_impact(initial_wealth, poor_count, initial_poor_income, growth_rate=0.05, zakat_rate=0.025, years=5):
    """
    نموذج يحاكي أثر الزكاة على الفقر وتحفيز الاقتصاد عبر عدة سنوات.
    يعتمد على معدل نمو سنوي ونسبة زكاة ثابتة[cite: 1].
    """
    results = []
    current_wealth = initial_wealth
    # إجمالي الدخل الأولي للفقراء قبل الزكاة
    base_poor_income_total = poor_count * initial_poor_income 
    
    for year in range(1, years + 1):
        # حساب مقدار الزكاة الواجبة[cite: 1]
        zakat_due = current_wealth * zakat_rate
        
        # حساب إجمالي دخل الفقراء بعد استلام الزكاة[cite: 1]
        total_poor_income_after = base_poor_income_total + zakat_due
        
        # متوسط دخل الفرد الفقير بعد الزكاة[cite: 1]
        avg_poor_income = total_poor_income_after / poor_count
        
        results.append({
            "year": year,
            "wealth": round(current_wealth, 2),
            "zakat_due": round(zakat_due, 2),
            "total_poor_income": round(total_poor_income_after, 2),
            "avg_poor_income": round(avg_poor_income, 2)
        })
        
        # تطبيق معدل النمو الاقتصادي للسنة القادمة على ثروة الأغنياء ودخل الفقراء الأساسي[cite: 1]
        current_wealth *= (1 + growth_rate)
        base_poor_income_total *= (1 + growth_rate)
        
    return results

def compare_financing_systems(P1, P2, revenue, cost, phi):
    """
    مقارنة بين نظام سعر الفائدة ونظام المشاركة (PLS)[cite: 1].
    """
    # نظام سعر الفائدة: إجمالي الربح = مبلغ السداد - مبلغ القرض[cite: 1]
    interest_profit = P2 - P1 
    
    # نظام المشاركة (PPP): دخل الفترة = نسبة المشاركة * (إجمالي الإيرادات - إجمالي التكاليف)[cite: 1]
    pls_profit = phi * (revenue - cost)
    
    return {
        "interest_profit": round(interest_profit, 2),
        "pls_profit": round(pls_profit, 2)
    }