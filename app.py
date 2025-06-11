from flask import Flask, request, jsonify
import base64
import io
import torch
from PIL import Image

app = Flask(__name__)
from model_load import load, transform, idx2char, device
import torch

model = load()


def predict(image):
    image_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image_tensor)
    prediction = ''
    for output in outputs:
        _, predicted_idx = torch.max(output, 1)
        prediction += idx2char[predicted_idx.item()]
    return prediction


@app.route('/', methods=['POST'])
def handle_predict():
    try:
        data = request.json
        img_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_data)).convert('RGB')
        prediction = predict(img)
        return jsonify({"prediction": prediction, "status": "success"})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3636, debug=True)
