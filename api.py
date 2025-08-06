import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torchvision.transforms as transforms
from PIL import Image

app = Flask(__name__)
CORS(app)

import os

# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# モデルとクラス名の絶対パスを構築
MODEL_PATH = os.path.join(script_dir, 'model.pth')
CLASS_NAMES_PATH = os.path.join(script_dir, 'class_names.txt')

import torchvision.models as models

# デバイスの設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# クラス名のロード
try:
    with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
        class_names = [line.strip() for line in f.readlines()]
    num_classes = len(class_names)
except FileNotFoundError:
    class_names = None
    num_classes = 0
    print(f"Error: Class names file not found at {CLASS_NAMES_PATH}")

# 各クラスの信頼度スコア (混同行列の対角成分から取得)
# 順序は class_names と一致している必要があります
confidence_scores = {
    "Africa": 0.73,
    "Asia": 0.74,
    "Europe": 0.81,
    "Japan": 0.89,
    "Middle East": 0.46,
    "North America": 0.86,
    "Oceania": 0.78,
    "South America": 0.70,
}

# モデルのロード
try:
    # モデルの構造を定義 (DenseNet121を使用)
    model = models.densenet121(weights=None) 
    num_ftrs = model.classifier.in_features
    model.classifier = torch.nn.Linear(num_ftrs, num_classes) # 出力層をクラス数に合わせる

    # 保存された重みをロード
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
except FileNotFoundError:
    model = None
    print(f"Error: Model file not found at {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")


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

    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
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
            confidence = confidence_scores.get(predicted_class, 0.0) # 信頼度を取得

        return jsonify({'prediction': predicted_class, 'confidence': confidence})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
