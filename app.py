from flask import Flask, render_template, request
import pickle
import numpy as np
import webbrowser
import threading

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        area = float(request.form['area'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        floors = float(request.form['floors'])

        features = np.array([[area, bedrooms, bathrooms, floors]])
        prediction = model.predict(features)[0]

        return render_template("index.html",
                               prediction_text=f"🏠 Predicted Price: ₹ {round(prediction,2)}")

    except Exception as e:
        return render_template("index.html",
                               prediction_text=f"❌ Error: {str(e)}")

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)