from flask import Flask, request, jsonify
from flask_cors import CORS
from encoders import mark_invalid_ages_as_nan, to_lower, CustomLabelEncoder
import pandas as pd
import pyodbc
import jellyfish
import unidecode
from risk_scoring import predict_risk_coefficient_with_proba

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

def get_db_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-4UA2CF8H\\SQLEXPRESS;"
        "DATABASE=KYC-BHA-DEV;"
        "Trusted_Connection=yes;"
    )


@app.route('/api/risk-score', methods=['POST'])
def predict_risk():
    try:
        data = request.get_json()
        print("Received data:", data)
        predicted_risk, risk_percentages = predict_risk_coefficient_with_proba(data)

        risk_mapping = {'RE': 'Risque Élevé', 'RF': 'Risque Faible', 'RM': 'Risque Moyen'}

        response = {
            "predicted_risk": risk_mapping.get(predicted_risk, predicted_risk),
            "risk_percentages": {
                "RE": round(risk_percentages.get('RE', 0), 2),
                "RF": round(risk_percentages.get('RF', 0), 2),
                "RM": round(risk_percentages.get('RM', 0), 2),
            },
            "score_global": round(risk_percentages.get(predicted_risk, 0), 2)  # ici

        }
        return jsonify(response)
    except Exception as e:
        print(f"Erreur dans /api/risk-score : {e}")
        return jsonify({"error": str(e)}), 500 
#===== Similitude ===========
def nettoyer(val):
    return unidecode.unidecode(str(val).lower().strip()) if val else ""
# Liste simplifiée des correspondances multilinguesù

EQUIVALENCES_FIXES = {

    "tunisie": ["tunisie", "tunisia", "tn", "تونس"],
    "france": ["france", "fr", "فرنسا"],
    "algérie": ["algérie", "algerie", "dz", "الجزائر"],
    "allemagne": ["allemagne", "germany", "de", "ألمانيا"],
    "italie": ["italie", "italy", "it", "إيطاليا"],
    "espagne": ["espagne", "spain", "es", "إسبانيا"],
    "canada": ["canada", "ca", "كندا"],
    "états-unis": ["états-unis", "usa", "united states", "us", "الولايات المتحدة"],
    "maroc": ["maroc", "morocco", "ma", "المغرب"],
    "suisse": ["suisse", "switzerland", "ch", "سويسرا"],
    "belgique": ["belgique", "belgium", "be", "بلجيكا"],
    "pays-bas": ["pays-bas", "netherlands", "nl", "هولندا"],
    "turquie": ["turquie", "turkey", "tr", "تركيا"],
    "chine": ["chine", "china", "cn", "الصين"],             
    "japon": ["japon", "japan", "jp", "اليابان"],
    "inde": ["inde", "india", "in", "الهند"],   
    "brésil": ["brésil", "brazil", "br", "البرازيل"],
    "argentine": ["argentine", "argentina", "ar", "الأرجنتين"], 
    "russie": ["russie", "russia", "ru", "روسيا"],
    "corée du sud": ["corée du sud", "south korea", "kr", "كوريا الجنوبية"],
    "corée du nord": ["corée du nord", "north korea", "kp", "كوريا الشمالية"],
    "mexique": ["mexique", "mexico", "mx", "المكسيك"],
    "sénégal": ["sénégal", "senegal", "sn", "السنغال"],
    "côte d'ivoire": ["côte d'ivoire", "ivory coast", "ci", "كوت ديفوار"],
    "cameroun": ["cameroun", "cameroon", "cm", "الكاميرون"],
    "ghana": ["ghana", "gh", "غانا"],       
    "nigeria": ["nigeria", "ng", "نيجيريا"],
    "afrique du sud": ["afrique du sud", "south africa", "za", "جنوب أفريقيا"],
    "égypte": ["égypte", "egypt", "eg", "مصر"],
    "liban": ["liban", "lebanon", "lb", "لبنان"],
    "irak": ["irak", "iraq", "iq", "العراق"],
    "iran": ["iran", "ir", "إيران"],    
    "arabie saoudite": ["arabie saoudite", "saudi arabia", "sa", "المملكة العربية السعودية"],
    "émirats arabes unis": ["émirats arabes unis", "united arab emirates", "ae", "الإمارات العربية المتحدة"],
    "pologne": ["pologne", "poland", "pl", "بولندا"],
    "suède": ["suède", "sweden", "se", "السويد"],
    "autriche": ["autriche", "austria", "at", "النمسا"],
    "portugal": ["portugal", "pt", "البرتغال"],
    "grèce": ["grèce", "greece", "gr", "اليونان"],
    "islande": ["islande", "iceland", "is", "أيسلندا"],
    "hongrie": ["hongrie", "hungary", "hu", "المجر"],
    "tchéquie": ["tchéquie", "czech republic", "cz", "التشيك"],
    "slovaquie": ["slovaquie", "slovakia", "sk", "سلوفاكيا"],
    "croatie": ["croatie", "croatia", "hr", "كرواتيا"],
    "serbie": ["serbie", "serbia", "rs", "صربيا"],
    "bulgarie": ["bulgarie", "bulgaria", "bg", "بلغاريا"],
    "roumanie": ["roumanie", "romania", "ro", "رومانيا"],
    "ukraine": ["ukraine", "ua", "أوكرانيا"],   
    "biélorussie": ["biélorussie", "belarus", "by", "بيلاروسيا"],
    "lettonie": ["lettonie", "latvia", "lv", "لاتفيا"],
    "lituanie": ["lituanie", "lithuania", "lt", "ليتوانيا"],
    "estonie": ["estonie", "estonia", "ee", "إستونيا"],
    "malaisie": ["malaisie", "malaysia", "my", "ماليزيا"],
    "indonésie": ["indonésie", "indonesia", "id", "إندونيسيا"],
    "thaïlande": ["thaïlande", "thailand", "th", "تايلاند"],
    "vietnam": ["vietnam", "vn", "فيتنام"],
    "philippines": ["philippines", "ph", "الفلبين"],
    "australie": ["australie", "australia", "au", "أستراليا"],
    "nouvelle-zélande": ["nouvelle-zélande", "new zealand", "nz", "نيوزيلندا"],
    "colombie": ["colombie", "colombia", "co", "كولومبيا"],
    "irlande": ["irlande", "ireland", "ie", "أيرلندا"],
    "chypre": ["chypre", "cyprus", "cy", "قبرص"],
    "malte": ["malte", "malta", "mt", "مالطا"],
    "slovénie": ["slovénie", "slovenia", "si", "سلوفينيا"],
    "bosnie-herzégovine": ["bosnie-herzégovine", "bosnia and herzegovina", "ba", "البوسنة والهرسك"],
    "macédoine du nord": ["macédoine du nord", "north macedonia", "mk", "مقدونيا الشمالية"],
    "monténégro": ["monténégro", "montenegro", "me", "الجبل الأسود"],
    "kosovo": ["kosovo", "xk", "كوسوفو"],
    "géorgie": ["géorgie", "georgia", "ge", "جورجيا"],
    "arménie": ["arménie", "armenia", "am", "أرمينيا"],
    "azerbaïdjan": ["azerbaïdjan", "azerbaijan", "az", "أذربيجان"],
    "maldives": ["maldives", "mv", "جزر المالديف"],
    "sri lanka": ["sri lanka", "lk", "سريلانكا"],
    "bangladesh": ["bangladesh", "bd", "بنغلاديش"], 
    "pakistan": ["pakistan", "pk", "باكستان"],
    "afghanistan": ["afghanistan", "af", "أفغانستان"],
    "syrie": ["syrie", "syria", "sy", "سوريا"],
    "libye": ["libye", "libya", "ly", "ليبيا"],
    "finlande": ["finlande", "finland", "fi", "فنلندا"],
    "norvège": ["norvège", "norway", "no", "النرويج"],
    "danemark": ["danemark", "denmark", "dk", "الدنمارك"],
    "royaume-uni": ["royaume-uni", "united kingdom", "uk", "gb", "المملكة المتحدة"],
    "angola": ["angola", "ao", "أنغولا"],
    "éthiopie": ["éthiopie", "ethiopia", "et", "إثيوبيا"],
    "kenya": ["kenya", "ke", "كينيا"],
    "rwanda": ["rwanda", "rw", "رواندا"],
    "tanzanie": ["tanzanie", "tanzania", "tz", "تنزانيا"],
    "ouganda": ["ouganda", "uganda", "ug", "أوغندا"],
    "zambie": ["zambie", "zambia", "zm", "زامبيا"],
    "zimbabwe": ["zimbabwe", "zw", "زيمبابوي"],
    "madagascar": ["madagascar", "mg", "مدغشقر"],
    "maurice": ["maurice", "mauritius", "mu", "موريشيوس"],
    "seychelles": ["seychelles", "sc", "سيشل"],
    "cuba": ["cuba", "cu", "كوبا"],
    "république dominicaine": ["république dominicaine", "dominican republic", "do", "جمهورية الدومينيكان"],
    "haiti": ["haiti", "ht", "هايتي"],
    "jamaïque": ["jamaïque", "jamaica", "jm", "جامايكا"],
    "bahreïn": ["bahreïn", "bahrain", "bh", "البحرين"],
    "qatar": ["qatar", "qa", "قطر"],
    "koweït": ["koweït", "kuwait", "kw", "الكويت"],
    "oman": ["oman", "om", "عمان"],
    "yémen": ["yémen", "yemen", "ye", "اليمن"],
    "jordanie": ["jordanie", "jordan", "jo", "الأردن"],
    "palestine": ["palestine", "ps", "فلسطين"],
    "israël": ["israël", "israel", "il", "إسرائيل"],
    "monaco": ["monaco", "mc", "موناكو"],
    "andorre": ["andorre", "andorra", "ad", "أندورا"],
    "liechtenstein": ["liechtenstein", "li", "ليختنشتاين"],
    "saint-marin": ["saint-marin", "san marino", "sm", "سان مارينو"],
    "vatican": ["vatican", "vatican city", "va", "الفاتيكان"],
    "népal": ["népal", "nepal", "np", "نيبال"],
    "bhoutan": ["bhoutan", "bhutan", "bt", "بوتان"],
    "mongolie": ["mongolie", "mongolia", "mn", "منغوليا"],
    "laos": ["laos", "la", "لاوس"],
    "cambodge": ["cambodge", "cambodia", "kh", "كمبوديا"],
    "myanmar": ["myanmar", "mm", "ميانمار"],
    "timor oriental": ["timor oriental", "east timor", "tl", "تيمور الشرقية"],
    "fidji": ["fidji", "fiji", "fj", "فيجي"],
    "vanuatu": ["vanuatu", "vu", "فانواتو"],
    "salomon": ["salomon", "solomon islands", "sb", "جزر سليمان"],
    "samoa": ["samoa", "ws", "ساموا"],
    "tonga": ["tonga", "to", "تونغا"],
    "kiribati": ["kiribati", "ki", "كيريباتي"],
    "nauru": ["nauru", "nr", "ناورو"],
    "tuvalu": ["tuvalu", "tv", "توفالو"],
    "paraguay": ["paraguay", "py", "باراغواي"],
    "uruguay": ["uruguay", "uy", "أوروغواي"],
    "panama": ["panama", "pa", "بنما"],
    "costa rica": ["costa rica", "cr", "كوستاريكا"],
    "nicaragua": ["nicaragua", "ni", "نيكاراغوا"],
    "honduras": ["honduras", "hn", "هندوراس"],
    "salvador": ["salvador", "el salvador", "sv", "السلفادور"],
    "guatemala": ["guatemala", "gt", "غواتيمالا"],
    "belize": ["belize", "bz", "بليز"],
    "guyana": ["guyana", "gy", "غيانا"],
    "suriname": ["suriname", "sr", "سورينام"],
    "équateur": ["équateur", "ecuador", "ec", "الإكوادور"],
    "pérou": ["pérou", "peru", "pe", "بيرو"],
    "bolivie": ["bolivie", "bolivia", "bo", "بوليفيا"],
    "chili": ["chili", "chile", "cl", "تشيلي"],
    "venezuela": ["venezuela", "ve", "فنزويلا"],
    "guyane française": ["guyane française", "french guiana", "gf", "غويانا الفرنسية"],
    "nouvelle-calédonie": ["nouvelle-calédonie", "new caledonia", "nc", "كاليدونيا الجديدة"],
    "polynésie française": ["polynésie française", "french polynesia", "pf", "بولينيزيا الفرنسية"],
    "réunion": ["réunion", "re", "لا ريونيون"],
    "mayotte": ["mayotte", "yt", "مايوت"],
    "comores": ["comores", "comoros", "km", "جزر القمر"],
    "sao tomé-et-principe": ["sao tomé-et-principe", "sao tome and principe", "st", "ساو تومي وبرينسيبي"],
    "cap-vert": ["cap-vert", "cape verde", "cv", "الرأس الأخضر"],
    "gambie": ["gambie", "gambia", "gm", "غامبيا"],
    "guinée": ["guinée", "guinea", "gn", "غينيا"],
    "guinée-bissau": ["guinée-bissau", "guinea-bissau", "gw", "غينيا بيساو"],
    "sierra leone": ["sierra leone", "sl", "سيراليون"],
    "libéria": ["libéria", "liberia", "lr", "ليبيريا"],
    "mali": ["mali", "ml", "مالي"],
    "burkina faso": ["burkina faso", "bf", "بوركينا فاسو"],
    "niger": ["niger", "ne", "النيجر"],
    "tchad": ["tchad", "chad", "td", "تشاد"],
    "soudan": ["soudan", "sudan", "sd", "السودان"],
    "soudan du sud": ["soudan du sud", "south sudan", "ss", "جنوب السودان"],
    "érythrée": ["érythrée", "eritrea", "er", "إريتريا"],
    "djibouti": ["djibouti", "dj", "جيبوتي"],
    "somali": ["somali", "somalia", "so", "الصومال"],
    "république centrafricaine": ["république centrafricaine", "central african republic", "cf", "جمهورية أفريقيا الوسطى"],
    "république démocratique du congo": ["république démocratique du congo", "democratic republic of the congo", "cd", "جمهورية الكونغو الديمقراطية"],
    "congo": ["congo", "cg", "جمهورية الكونغو"],
    "gabon": ["gabon", "ga", "الغابون"],
    "guinée équatoriale": ["guinée équatoriale", "equatorial guinea", "gq", "غينيا الاستوائية"],
    "burundi": ["burundi", "bi", "بوروندي"],
    "lesotho": ["lesotho", "ls", "ليسوتو"],
    "eswatini": ["eswatini", "swaziland", "sz", "إسواتيني"],
    "namibie": ["namibie", "namibia", "na", "ناميبيا"],
    "botswana": ["botswana", "bw", "بوتسوانا"],
    "mozambique": ["mozambique", "mz", "موزمبيق"],
    "malawi": ["malawi", "mw", "مالاوي"],
    "togo": ["togo", "tg", "توغو"],
    "bénin": ["bénin", "benin", "bj", "بنين"],
    "mauritanie": ["mauritanie", "mauritania", "mr", "موريتانيا"],
}

def normaliser_valeur(val):
    val_nettoyee = nettoyer(val)
    for valeur_normalisee, variantes in EQUIVALENCES_FIXES.items():
        if val_nettoyee in [nettoyer(v) for v in variantes]:
            return valeur_normalisee
    return val_nettoyee

def comparer(val1, val2, method="jw"):
    if method == "jw":
        return jellyfish.jaro_winkler_similarity(nettoyer(val1), nettoyer(val2))
    elif method == "egal":
        return 1.0 if normaliser_valeur(val1) == normaliser_valeur(val2) else 0.0
    return 0.0


def interprete_score(score):
    if score >= 90:
        return "Très fort"
    elif score >= 70:
        return "Fort"
    elif score >= 50:
        return "Modéré"
    else:
        return "Faible"

def calculer_score(client, suspect, regle):
    total_coef = (
        regle['coef_nom'] + regle['coef_prenom'] +
        regle['coef_date_naissance'] + regle['coef_nationalite'] +
        regle['coef_residence']
    )
    score = (
        regle['coef_nom'] * comparer(client['nom'], suspect['nom']) +
        regle['coef_prenom'] * comparer(client['prenom'], suspect['prenom']) +
        regle['coef_date_naissance'] * comparer(client['date_naissance'], suspect['date_naissance'], "egal") +
        regle['coef_nationalite'] * comparer(client['nationalite'], suspect['nationalite'], "egal") +
        regle['coef_residence'] * comparer(client['residence'], suspect['residence'], "egal")
    )
    return (score / total_coef) * 100

# === ROUTES API ===
@app.route('/api/regles/<int:id>/status', methods=['PUT'])
def set_regle_status(id):
    data = request.get_json()
    new_status = data.get('active')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Désactiver toutes les règles avant d'activer celle-ci
        cursor.execute("UPDATE rules SET active = 0 WHERE ID_RULE != ?", (id,))
        cursor.execute("UPDATE rules SET active = ? WHERE ID_RULE = ?", (int(new_status), id))
        conn.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Erreur lors de la mise à jour du statut : {e}")
        return jsonify({'error': 'Erreur interne'}), 500



@app.route("/api/regles", methods=["GET"])
def get_regles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RULES")
    rows = cursor.fetchall()
    conn.close()
    regles = [{
        "id": row.ID_RULE,
        "nom": row.NAME_RULE,
        "type": row.TYPE_RULE,
        "coef_nom": row.COEF_NOM,
        "coef_prenom": row.COEF_PRENOM,
        "coef_date_naissance": row.COEF_DOB,
        "coef_nationalite": row.COEF_NATIONALITE,
        "coef_residence": row.COEF_RESIDENCE,
        "seuil_similitude": row.Similarity_Score,
        "active": row.Active
    } for row in rows]
    return jsonify(regles)

@app.route("/api/regles", methods=["POST"])
def add_regle():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO RULES 
        (NAME_RULE, TYPE_RULE, COEF_NOM, COEF_PRENOM, COEF_DOB, 
         COEF_NATIONALITE, COEF_RESIDENCE, Similarity_Score, Active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["nom"], data["type"], data["coef_nom"], data["coef_prenom"],
        data["coef_date_naissance"], data["coef_nationalite"],
        data["coef_residence"], data["seuil_similitude"], 1
    ))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Règle ajoutée"}), 201



@app.route("/api/similarite", methods=["POST"])
def similarite():
    req = request.json
    client = req["client"]
    regle = req["regle"]

   # print("📥 Client reçu :", client)
    # print("⚙️ Règle utilisée :", regle)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lastName, firstName, dob, placeOfBirth, citizenship FROM Pep")
    rows = cursor.fetchall()
    conn.close()

    suspects = [{
        "nom": row.lastName,
        "prenom": row.firstName,
        "date_naissance": row.dob.strftime("%Y-%m-%d") if row.dob else "",
        "nationalite": row.placeOfBirth,
        "residence": row.citizenship
    } for row in rows]

    results = []
    for suspect in suspects:
        score = calculer_score(client, suspect, regle)
       # print(f"🔎 Comparaison avec {suspect['nom']} {suspect['prenom']} ➜ Score: {score:.2f}")

        if score >= regle["seuil_similitude"]:
            results.append({
                "nom": suspect["nom"],
                "prenom": suspect["prenom"],
                "score": round(score, 2),
                "niveau": interprete_score(score),
                "alerte": True
            })

    results.sort(key=lambda r: r["score"], reverse=True)

    print("✅ Résultats renvoyés :", results)
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
   

