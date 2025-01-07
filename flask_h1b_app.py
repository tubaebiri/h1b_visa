from flask import Flask, request, jsonify, render_template
from h1btahmin import predict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_h1b():
    # Kullanıcıdan gelen verileri al
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    job_title = data.get('jobTitle')
    company = data.get('company')
    worksite = data.get('worksite')

    # Predict fonksiyonunu çağır
    try:
        probability = predict(job_title, company, worksite)
        response = {
            'message': f"{first_name} {last_name}, POSSIBILITY OF GETTING A VISA: %{probability}"
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
