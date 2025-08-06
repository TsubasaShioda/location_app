import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torchvision.transforms as transforms
from PIL import Image

app = Flask(__name__)
CORS(app)

# モデルとクラス名のパス
MODEL_PATH = 'model.pth'
CLASS_NAMES_PATH = 'class_names.txt'

# デバイスの設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# モデルのロード
try:
    model = torch.load(MODEL_PATH, map_location=device)
    model.eval()
except FileNotFoundError:
    model = None
    print(f"Error: Model file not found at {MODEL_PATH}")


# クラス名のロード
try:
    with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
        class_names = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    class_names = None
    print(f"Error: Class names file not found at {CLASS_NAMES_PATH}")


# 画像の前処理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or class_names is None:
        return jsonify({'error': 'Model or class names not loaded'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        image_tensor = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted_idx = torch.max(outputs, 1)
            predicted_class = class_names[predicted_idx.item()]

        return jsonify({'prediction': predicted_class})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
