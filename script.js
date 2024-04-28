function updateTargetColor() {
    fetch('/random_color')
        .then(response => response.json())
        .then(data => {
            document.getElementById('color-box').style.backgroundColor = data.color;
        });
}

function chooseCustomColor() {
    document.getElementById('canvas').click();
}

function clearCanvas() {
    document.getElementById('canvas').style.backgroundColor = 'white';
}

function mixColors() {
    const color1 = document.getElementById('color1').value;
    const color2 = document.getElementById('color2').value;
    const percent1 = parseFloat(document.getElementById('percent1').value);
    const percent2 = parseFloat(document.getElementById('percent2').value);

    fetch('/mix_colors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ color1, color2, percent1, percent2 })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('mixed-color').style.backgroundColor = data.mixed_color;
        });
}

document.addEventListener('DOMContentLoaded', function () {
    updateTargetColor();
});
