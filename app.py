from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Define a list of 12 colors
colors = ['#ff0000', '#ff7f00', '#ffff00', '#7fff00', '#00ff00', '#00ff7f', '#00ffff', '#007fff', '#0000ff', '#7f00ff', '#ff00ff', '#ff007f']

@app.route('/')
def index():
    return render_template('index.html', colors=colors)

@app.route('/random_color', methods=['GET'])
def random_color():
    color = random.choice(colors)
    return jsonify({'color': color})

@app.route('/mix_colors', methods=['POST'])
def mix_colors():
    data = request.get_json()
    color1 = data['color1']
    color2 = data['color2']
    percent1 = data['percent1']
    percent2 = data['percent2']
    
    # Check if color strings are empty
    if not color1 or not color2:
        return jsonify({'mixed_color': "#FFFFFF"})  # Return white if either color is not provided

    # Convert percentages to ratios
    total_percent = percent1 + percent2
    ratio1 = percent1 / total_percent
    ratio2 = percent2 / total_percent

    # Extract RGB values from color strings
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    # Interpolate RGB values based on the ratios
    r = int(r1 * ratio1 + r2 * ratio2)
    g = int(g1 * ratio1 + g2 * ratio2)
    b = int(b1 * ratio1 + b2 * ratio2)

    # Convert interpolated RGB values to hexadecimal format
    mixed_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    return jsonify({'mixed_color': mixed_color})

if __name__ == '__main__':
    app.run(debug=True)
