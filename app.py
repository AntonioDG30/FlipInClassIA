from flask import Flask, render_template

app = Flask(__name__)

# Definisci la route per la homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    # Avvia l'app in modalità debug
    app.run(debug=True)
