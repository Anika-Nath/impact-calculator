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


def main():
    """
    Main function to run the Flask web application
    """
    
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
