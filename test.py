from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def color_palette():
    # Define the colors you want in the palette
    colors = [
        '#FF5733', '#33FF57', '#5733FF', '#FFD133', '#33FFF5', '#F533FF',
        '#33FFAA', '#AA33FF', '#FFAA33', '#AAFF33', '#33FF57', '#5733FF'
    ]
    return render_template('palette.html', colors=colors)

if __name__ == '__main__':
    app.run(debug=True)