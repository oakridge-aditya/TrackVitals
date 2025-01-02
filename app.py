from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP 

app = Flask(__name__)
app.app_context().push()

# Database config for connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:welcome@18.61.8.66:3307/health"
db = SQLAlchemy(app)

# Create database model
class Metrics(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    created = db.Column(db.TIMESTAMP)
    weight = db.Column(db.Integer, nullable=False)
    bp = db.Column(db.Integer, nullable=False)
    sugar = db.Column(db.Integer, nullable=False)
    oxygen = db.Column(db.Integer, nullable=False)
    pulserate = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)


db.create_all()

# Homepage
@app.route('/')
def home():
    return render_template('homepage.html')

# Route displays the blank form
@app.route('/form')
def form():
    return render_template('form.html')

# Save the submitted data in database
@app.route("/process",methods=['GET','POST'])
def process():
    if request.method == 'POST':
        created = request.form.get('created')
        weight = request.form.get('weight')
        bp = request.form.get('bp')
        sugar = request.form.get('sugar')
        oxygen = request.form.get('oxygen')
        pulserate = request.form.get('pulserate')
        temperature = request.form.get('temperature')
        data = Metrics(created=created,weight=weight,bp=bp,sugar=sugar,oxygen=oxygen, pulserate=pulserate, temperature=temperature)
        db.session.add(data)
        db.session.commit()
        return redirect('/chart')

@app.route('/chart')
def chart():
    health_data = Metrics.query.order_by(Metrics.created)
    date_labels = []
    weight_values = []
    bp_values = []
    sugar_values = []
    oxygen_values = []
    pulserate_values = []
    temperature_values = []
    for data in health_data:
        date_labels.append(str(data.created.date()))
        weight_values.append(data.weight)
        bp_values.append(data.bp)
        sugar_values.append(data.sugar)
        oxygen_values.append(data.oxygen)
        pulserate_values.append(data.pulserate)
        temperature_values.append(data.temperature)
    return render_template('charts.html', weight_values=weight_values, labels=date_labels, bp_values=bp_values, sugar_values=sugar_values, oxygen_values=oxygen_values, pulserate_values=pulserate_values, temperature_values=temperature_values)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)