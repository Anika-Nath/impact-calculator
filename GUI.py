from flask import Flask, render_template, request, jsonify
import os
import io, base64, math
import matplotlib
matplotlib.use("Agg")  # required on servers
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np


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
        
        image_b64 = generate_damage_image(mass, speed, height_of_burst, entry_angle)

        # Here you can add your calculation logic
        # For now, just returning the input values
        result = {
            'mass': mass,
            'speed': speed,
            'height_of_burst': height_of_burst,
            'entry_angle': entry_angle,
            'status': 'success',
            'message': 'Parameters received successfully!',
            'image': image_b64
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

def map_ke_to_size(mass_kg, speed_km_s, ke_min=1e9, ke_max=1e14):
    v = speed_km_s * 1000.0  # m/s
    KE = 0.5 * mass_kg * v * v  # Joules

    # Map log10(KE) from [ke_min, ke_max] to [2, 14] units of full width
    logK = math.log10(max(KE, 1.0))
    t = (logK - math.log10(ke_min)) / (math.log10(ke_max) - math.log10(ke_min))
    t = max(0.0, min(t, 1.0))
    return 2.0 + t * 12.0

def map_height_to_ecc(height_km, ref_km=50.0):
    frac = max(0.0, min(height_km / ref_km, 1.0))
    e = 1.0 - 0.9 * frac
    return max(0.05, min(e, 0.95))

def mass_to_gray(mass_kg, ref_mass=10000.0):
    g = max(0.0, min(mass_kg / ref_mass, 1.0))
    gray = 1.0 - 0.85 * g
    return str(gray)

def generate_damage_image(mass, speed, height_of_burst, entry_angle_deg):
    width = map_ke_to_size(mass, speed)            # major axis
    e = map_height_to_ecc(height_of_burst)         # eccentricity
    a = width / 2.0
    b = a * math.sqrt(max(1.0 - e * e, 0.0025))    # semi minor
    height_val = 2.0 * b
    face = mass_to_gray(mass)
    angle = entry_angle_deg

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect("equal")

    ell = Ellipse((0, 0), width, height_val, angle=angle,
                  edgecolor="black", facecolor=face, lw=2)
    ax.add_patch(ell)

    theta = math.radians(angle)
    x_line = [-a * math.cos(theta), a * math.cos(theta)]
    y_line = [-a * math.sin(theta), a * math.sin(theta)]
    ax.plot(x_line, y_line, color="red", lw=2)

    canvas = 12.0
    ax.set_xlim(-canvas, canvas)
    ax.set_ylim(-canvas, canvas)
    ax.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

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


