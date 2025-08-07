from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get form data
        mass = float(request.form['mass'])
        speed = float(request.form['speed'])
        height_of_burst = float(request.form['height_of_burst'])
        entry_angle = float(request.form['entry_angle'])
        
        # Here you can add your calculation logic
        # For now, just returning the input values
        result = {
            'mass': mass,
            'speed': speed,
            'height_of_burst': height_of_burst,
            'entry_angle': entry_angle,
            'status': 'success',
            'message': 'Parameters received successfully!'
        }
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': 'Please enter valid numeric values for all parameters.'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500

def create_html_template():
    """Create the HTML template file"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impact Calculator GUI</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            width: 100%;
            max-width: 500px;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
            font-size: 1.1em;
        }
        
        input[type="number"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
            box-sizing: border-box;
        }
        
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .units {
            color: #888;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 8px;
            display: none;
        }
        
        .result.success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        
        .result.error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .result-content {
            margin-top: 15px;
        }
        
        .result-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 5px 0;
        }
        
        .result-label {
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Impact Calculator</h1>
        
        <form id="impactForm">
            <div class="form-group">
                <label for="mass">Mass</label>
                <input type="number" id="mass" name="mass" step="0.01" required>
                <div class="units">kg</div>
            </div>
            
            <div class="form-group">
                <label for="speed">Speed</label>
                <input type="number" id="speed" name="speed" step="0.01" required>
                <div class="units">km/s</div>
            </div>
            
            <div class="form-group">
                <label for="height_of_burst">Height of Burst</label>
                <input type="number" id="height_of_burst" name="height_of_burst" step="0.01" required>
                <div class="units">km</div>
            </div>
            
            <div class="form-group">
                <label for="entry_angle">Entry Angle</label>
                <input type="number" id="entry_angle" name="entry_angle" step="0.01" min="0" max="90" required>
                <div class="units">degrees (0-90)</div>
            </div>
            
            <button type="submit">Calculate Impact</button>
        </form>
        
        <div id="result" class="result">
            <div id="resultMessage"></div>
            <div id="resultContent" class="result-content"></div>
        </div>
    </div>

    <script>
        document.getElementById('impactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            const resultMessage = document.getElementById('resultMessage');
            const resultContent = document.getElementById('resultContent');
            
            // Show loading state
            resultDiv.style.display = 'block';
            resultDiv.className = 'result';
            resultMessage.textContent = 'Calculating...';
            resultContent.innerHTML = '';
            
            fetch('/calculate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    resultDiv.className = 'result success';
                    resultMessage.textContent = data.message;
                    
                    // Display the input parameters
                    const params = [
                        { label: 'Mass', value: data.mass + ' kg' },
                        { label: 'Speed', value: data.speed + ' km/s' },
                        { label: 'Height of Burst', value: data.height_of_burst + ' km' },
                        { label: 'Entry Angle', value: data.entry_angle + '°' }
                    ];
                    
                    resultContent.innerHTML = '<h3>Input Parameters:</h3>';
                    params.forEach(param => {
                        resultContent.innerHTML += `
                            <div class="result-item">
                                <span class="result-label">${param.label}:</span>
                                <span>${param.value}</span>
                            </div>
                        `;
                    });
                } else {
                    resultDiv.className = 'result error';
                    resultMessage.textContent = data.message;
                }
            })
            .catch(error => {
                resultDiv.className = 'result error';
                resultMessage.textContent = 'An error occurred while processing the request.';
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    """
    Main function to run the Flask web application
    """
    # Create the HTML template
    create_html_template()
    
    print("Starting Impact Calculator GUI...")
    
    # Get port from environment variable (for cloud deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Server will run on port: {port}")
    
    # Run the Flask app
    # For production deployment, debug should be False
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main() 