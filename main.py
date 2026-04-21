from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json, os

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=base_dir, static_folder=base_dir, static_url_path='/static')
app.secret_key = "emaus_secret_key"
CONFIG_FILE = os.path.join(base_dir, "config.json")
UPLOAD_FOLDER = os.path.join(base_dir, 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"username": "Usuario", "theme": "light", "font_size": 16, "profile_pic": ""}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    config = load_config()
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "EMAUS123":
            session['logged_in'] = True
            return redirect(url_for('index'))
        error = "Contraseña incorrecta"
    return render_template('login.html', config=config, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/prayer')
def prayer():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    config = load_config()
    return render_template('prayer.html', config=config)

@app.route('/guide')
def guide():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    config = load_config()
    return render_template('guide.html', config=config)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    config = load_config()

    if request.method == 'POST':
        config['username'] = request.form.get('username')
        config['theme'] = request.form.get('theme')
        
        # Manejo de la imagen desde la galería
        file = request.files.get('profile_pic_file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            config['profile_pic'] = '/static/uploads/' + filename

        save_config(config)
        return redirect(url_for('index'))
    return render_template('settings.html', config=config)


@app.route('/ocr')
def ocr():
    rosario_data = {
        "introduccion": {
            "titulo": "ORACIÓN INTRODUCTORIA",
            "texto": "Padre Celestial, envía sobre mí al Espíritu Santo para que mi corazón se abra a Tu presencia. Jesús, camina a mi lado como con los discípulos de Emaús; escucha mis lamentos y revélate a mí. Que pueda reconocer Tu Palabra y abrirme al encuentro contigo. Amén.",
            "imagen": "/static/Jesus.jpg"
        },
        "misterios": [
            {
                "titulo": "PRIMER MISTERIO",
                "subtitulo": "JESÚS SE ACERCÓ A ELLOS",
                "lectura": "Jesús en persona se les acercó y se puso a caminar con ellos, pero algo impedía que sus ojos lo reconocieran. (Lc 24, 13-16)",
                "reflexion": "Gracias Jesús por no haber rechazado a los discípulos. Tú eres el viajero con los viajeros, Tú los entiendes y te unes a ellos. Haz que, de ahora en adelante, Tú seas el tema de mi conversación, mi camino y mi fe.",
                "imagen": "/static/misterio1.jpg"
            },
            {
                "titulo": "SEGUNDO MISTERIO",
                "subtitulo": "SE DETUVIERON ENTRISTECIDOS",
                "lectura": "Se detuvieron, y parecían muy entristecidos. Jesús les preguntó: ¿De qué van discutiendo por el camino? (Lc 24, 17-19)",
                "reflexion": "Jesús, Tú quieres desaparecer la tristeza y la desilusión y deseas convertirlas en nueva esperanza. Abre mis ojos para reconocer los momentos en que deba ayudar a otros en Tu nombre.",
                "imagen": "/static/misterio2.jpg"
            },
            {
                "titulo": "TERCER MISTERIO",
                "subtitulo": "NOSOTROS ESPERÁBAMOS…",
                "lectura": "Nosotros pensábamos que él sería el que debía liberar a Israel. (Lc 24, 19b-21)",
                "reflexion": "Jesús, Tú sabes que también mi fe es débil. Despierta en mí el aumento de fe para que mi esperanza no siga siendo frágil. Dame el don de tu Espíritu para saber bien en quién tengo puesta mi fe.",
                "imagen": "/static/misterio3.jpg"
            },
            {
                "titulo": "CUARTO MISTERIO",
                "subtitulo": "¿NO ERA NECESARIO QUE PADECIERA?",
                "lectura": "¿No tenía que ser así y que el Mesías padeciera para entrar en su gloria? (Lc 24, 25-27)",
                "reflexion": "¡Oh Jesús, ni para ti fue fácil padecer! Permite que la cruz de todos los que sufren florezca con la esperanza de la resurrección. Ayúdanos a cargar nuestra cruz con amor, aun sin entenderla.",
                "imagen": "/static/misterio4.jpg"
            },
            {
                "titulo": "QUINTO MISTERIO",
                "subtitulo": "¿NO ARDÍAN NUESTROS CORAZONES?",
                "lectura": "Tomó el pan, pronunció la bendición, lo partió y se lo dio. En ese momento se les abrieron los ojos. (Lc 24, 28-32)",
                "reflexion": "Señor, enciende el fuego que calienta los corazones fríos. Da a los sacerdotes la gracia de celebrar la misa para que siempre puedan reconocerte en la Hostia Sagrada.",
                "imagen": "/static/misterio5.jpg"
            }
        ],
        "conclusion": {
            "titulo": "ORACIÓN CONCLUSIVA",
            "texto": "¡Gracias Jesús por este encuentro! Sé Tú Señor el remedio a mi alma y la protección de mi vida. A partir de hoy quiero caminar decidido por la vida y no rendirme. Espero que tú y tu Madre Santísima sean siempre mis compañeros de viaje. Amén.",
            "imagen": "/static/Jesus.jpg"
        }
    }
    return jsonify(rosario_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
