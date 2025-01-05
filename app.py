from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Data Film Recommendation
film_recommendation = {
    "aksi": ["Mad Max: Fury Road", "John Wick", "The Dark Knight"],
    "komedi": ["The Hangover", "Superbad", "Jumanji: Welcome to the Jungle"],
    "romantis": ["The Notebook", "La La Land", "Crazy Rich Asians"],
    "horor": ["The Conjuring", "A Quiet Place", "It"],
    "kartun": ["Toy Story", "Spider-Man: Into the Spider-Verse", "Coco"],
}

# Data Penyakit dan Gejalanya
deseaseDB = {
    "flu": [
        "demam", "pusing", "sakit kepala", "menggigil", "batuk", "sakit tenggorokan",
        "hidung tersumbat", "kelelahan", "nyeri otot", "selera makan berkurang", 
        "pusing ringan", "mual", "sakit tubuh", "meriang"
    ],
    "sakit kepala tegang": [
        "sakit kepala", "pusing", "kelelahan", "tekanan di kepala", "nyeri di leher",
        "sensitivitas terhadap cahaya", "telinga berdenging", "tekanan mata", "mual"
    ],
    "flu biasa": [
        "batuk", "sakit tenggorokan", "hidung tersumbat", "demam", "pusing", "kelelahan", 
        "mual", "nyeri otot", "selera makan berkurang", "keluar cairan dari hidung", 
        "sakit badan", "meriang"
    ],
    "diare": [
        "perut kembung", "mulas", "buang air besar", "muntah", "demam", "dehidrasi",
        "lemas", "nyeri perut"
    ],
    "tuberkulosis": [
        "batuk berkepanjangan", "demam", "berkeringat malam", "penurunan berat badan",
        "mengi", "lemas", "mual", "sakit dada"
    ]
}

# Data Obat untuk Penyakit
medicine = {
    "flu": [
        "Paracetamol", "Sirup Batuk", "Dekongestan", "Antihistamin", "Obat penurun demam", 
        "Obat penghilang nyeri", "Vitamin C", "Obat pereda nyeri otot", "Antibiotik (jika ada infeksi sekunder)"
    ],
    "sakit kepala tegang": [
        "Obat penghilang rasa sakit", "Teknik relaksasi", "Antidepresan", "Obat pengurang stres",
        "Obat penghilang ketegangan otot", "Obat tidur"
    ],
    "flu biasa": [
        "Sirup batuk", "Obat penghilang rasa sakit", "Vitamin C", "Dekongestan", "Obat antihistamin",
        "Antibiotik (jika infeksi sekunder)", "Antiinflamasi nonsteroid (NSAID)"
    ],
    "diare": [
        "Obat antidiare", "Obat pengganti cairan", "Antibiotik (jika infeksi bakteri)", 
        "Probiotik", "Obat pereda nyeri perut", "Suplemen elektrolit"
    ],
    "tuberkulosis": [
        "Obat antituberkulosis", "Antibiotik untuk tuberkulosis", "Obat pereda batuk",
        "Obat penghilang rasa sakit", "Vitamin untuk mendukung pemulihan", "Obat pereda demam"
    ]
}

# Tips Pemulihan
recovery_tips = {
    "flu": [
        "Tetap terhidrasi", "Cukup tidur", "Gunakan penurun demam", "Konsumsi makanan bergizi", 
        "Hindari paparan dingin", "Minum teh hangat", "Gunakan masker jika batuk", "Berkumur dengan air garam"
    ],
    "sakit kepala tegang": [
        "Tetap terhidrasi", "Istirahat", "Gunakan kompres dingin", "Lakukan teknik relaksasi",
        "Hindari stres", "Tidur cukup", "Perhatikan postur tubuh", "Kurangi kafein"
    ],
    "flu biasa": [
        "Istirahat dan tidur yang cukup", "Minum cairan hangat", "Hindari aktivitas berat", 
        "Konsumsi vitamin dan suplemen", "Tetap hangat", "Makan makanan bergizi", "Hindari alkohol dan rokok"
    ],
    "diare": [
        "Perbanyak cairan tubuh", "Konsumsi makanan mudah dicerna", "Hindari makanan pedas", "Jaga kebersihan",
        "Minum oralit atau elektrolit", "Cek berat badan dan hidrasi secara rutin"
    ],
    "tuberkulosis": [
        "Konsumsi obat antituberkulosis secara teratur", "Istirahat total", "Perbanyak cairan tubuh", 
        "Hindari kontak dengan orang lain yang rentan", "Pantau berat badan dan nafsu makan", "Vaksinasi sesuai petunjuk dokter"
    ]
}

# Tips Kesehatan
healty_advice = {
    "flu": "Hindari aktivitas berat, istirahat cukup, dan jaga kebersihan diri.",
    "sakit kepala tegang": "Relaksasi tubuh, hindari stres, jaga pola tidur, perhatikan postur tubuh.",
    "malaria": "Hindari gigitan nyamuk, tetap dalam ruangan saat nyamuk aktif, gunakan kelambu tidur.",
    "flu biasa": "Tetap hangat, hindari paparan dingin, dan pastikan cukup tidur serta konsumsi cairan.",
    "diare": "Hindari makanan pedas dan berat, pastikan cukup cairan untuk mencegah dehidrasi.",
    "tuberkulosis": "Konsumsi obat secara rutin, jaga kebersihan diri, dan hindari kontak dekat dengan orang lain."
}

# Fungsi untuk menyarankan aktivitas saat bosan
def suggest_activities_when_bored():
    activities = [
        "Baca buku", "Nonton film", "Main game board", "Jogging", "Bersepeda", "Piknik", 
        "Meditasi", "Masak resep baru", "Coba hobi baru", "Cek sosmed", "Lakukan yoga", "Berkebun", 
        "Mendengarkan musik", "Menulis di jurnal", "Belajar hal baru", "Melakukan DIY project", 
        "Menonton dokumenter", "Bermain video game", "Mencoba puzzle"
    ]
    return random.choice(activities)

# Fungsi untuk mencocokkan penyakit berdasarkan input
def find_disease(keywords):
    user_input = " ".join(keywords).lower()

    for disease, symptoms in deseaseDB.items():
        if any(symptom in user_input for symptom in symptoms):
            return disease
    return None

# Entertainment recommendation based on genre
def recommend_film(user_input):
    user_input = user_input.lower()

    # Check if the user is asking for movie suggestions
    if "nonton" in user_input or "menonton" in user_input:
        genre_keywords = {
            "aksi": ["aksi", "perkelahian", "petualangan", "kejar-kejaran"],
            "komedi": ["komedi", "lucunya", "tawa", "humor", "kocak"],
            "romantis": ["romantis", "cinta", "pasangan", "jodoh"],
            "horor": ["horor", "seram", "menakutkan", "mencekam"],
            "kartun": ["kartun", "animasi", "kartun lucu", "film anak-anak"]
        }

        # Match input to the genre
        for genre, keywords in genre_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                return random.choice(film_recommendation[genre])

    return None

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").lower()
        if not user_input:
            return jsonify({"message": "Please enter a valid message."})

        response = {}

        # Greeting response
        if user_input in ["hi", "hello", "hai"]:
            response["message"] = "Hi! How can I help you today?"
            return jsonify(response)

        # Check for disease in user input
        keywords = user_input.split()
        disease = find_disease(keywords)
        if disease:
            response.update({
                "disease": disease,
                "medicine": medicine.get(disease, []),
                "recovery_tips": recovery_tips.get(disease, []),
                "health_reminder": healty_advice.get(disease, "Stay healthy!"),
            })

        # Check boredom-related input
        if "bosan" in user_input:
            response["activity_suggestion"] = suggest_activities_when_bored()

        # Check if the user is asking for a film recommendation
        if "film" in user_input or "nonton" in user_input or "menonton" in user_input:
            genre_keywords = {
                "aksi": ["aksi", "perkelahian", "petualangan", "kejar-kejaran"],
                "komedi": ["komedi", "lucunya", "tawa", "humor", "kocak"],
                "romantis": ["romantis", "cinta", "pasangan", "jodoh"],
                "horor": ["horor", "seram", "menakutkan", "mencekam"],
                "kartun": ["kartun", "animasi", "kartun lucu", "film anak-anak"]
            }

            # Check if any genre is mentioned in the user input
            for genre, keywords in genre_keywords.items():
                if any(keyword in user_input for keyword in keywords):
                    response["entertainment_recommendation"] = random.choice(film_recommendation[genre])
                    break
            else:
                # If no specific genre found, recommend a random film
                response["entertainment_recommendation"] = random.choice([film for films in film_recommendation.values() for film in films])

        if not response:
            response["message"] = "Maaf, saya tidak memahami maksud Anda. Bisa tolong diulang?"

        return jsonify(response)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"message": "Sorry, something went wrong. Please try again later."})


if __name__ == "__main__":
    app.run(debug=True)
