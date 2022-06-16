from flask import Flask, render_template, request, jsonify
import pickle
import nltk
import sklearn
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

stop_words = stopwords.words('english')
ps = PorterStemmer()

def proccess_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    
    for word in text:
        if word.isalnum():
            y.append(word)
          
    text = y[:] 
    y.clear()
    
    for word in text:
        if word not in stop_words:
            y.append(word)
            
    text = y[:]
    y.clear()
    
    for word in text:
        y.append(ps.stem(word))
    
    return " ".join(y)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/predict', methods=["POST"])
def predict():
    data = request.get_json()
    message = data['message']
    proccessed_message = proccess_text(message)
    vectorized_message = tfidf.transform([proccessed_message])
    prediction = model.predict(vectorized_message)[0]

    if prediction == 1:
        prediction = 'not spam'
    else:
        prediction = 'spam'
    
    return jsonify(prediction_result = prediction)

if __name__ == '__main__':
    app.run(debug=True)