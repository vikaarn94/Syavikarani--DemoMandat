from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

app = Flask(__name__)

def calculate_stats(numbers):
    try:
        return {
            'mean': np.mean(numbers),
            'median': np.median(numbers),
            'mode': mode(numbers),
            'std_dev': np.std(numbers),
            'variance': np.var(numbers),
            'min': np.min(numbers),
            'max': np.max(numbers),
            'range': np.max(numbers) - np.min(numbers)
        }
    except StatisticsError:
        return {
            'mean': np.mean(numbers),
            'median': np.median(numbers),
            'mode': 'No unique mode',
            'std_dev': np.std(numbers),
            'variance': np.var(numbers),
            'min': np.min(numbers),
            'max': np.max(numbers),
            'range': np.max(numbers) - np.min(numbers)
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    stats = None
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            df = pd.read_csv(file)
            col = df.select_dtypes(include=[np.number]).columns[0]  # pakai kolom numerik pertama
            data = df[col].dropna().values
            stats = calculate_stats(data)
        elif 'manual_input' in request.form:
            input_text = request.form['manual_input']
            try:
                numbers = [float(x) for x in input_text.replace(',', ' ').split()]
                stats = calculate_stats(numbers)
            except ValueError:
                stats = {'error': 'Input tidak valid. Masukkan angka dipisah spasi atau koma.'}
    return render_template('index.html', stats=stats)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
