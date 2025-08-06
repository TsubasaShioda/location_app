# 地域予測アプリケーション

このプロジェクトは、Next.jsで構築されたフロントエンドと、FlaskおよびPyTorchで構築されたPython APIから構成される地域予測アプリケーション。

## アプリケーション構成

### 1. フロントエンド (Next.js)
- **場所:** `nextjs-app/` ディレクトリ
- **技術:** Next.js (Reactフレームワーク)
- **役割:** ユーザーインターフェースを提供し、画像のアップロードと予測結果の表示を行う。
- **実行ポート:** `http://localhost:3000`
- **APIとの連携:** バックエンドAPI (`http://localhost:5001/predict`) に対して画像を送信し、予測結果を受け取る。

### 2. バックエンド (Flask API with PyTorch)
- **場所:** プロジェクトルート (`api.py`)
- **技術:** Flask (Webフレームワーク), PyTorch (機械学習ライブラリ)
- **役割:** フロントエンドから送信された画像を受け取り、PyTorchモデルを使用して地域を予測し、結果を返す。
- **実行ポート:** `http://localhost:5001`
- **モデル:** `model.pth` (DenseNet121の重み) と `class_names.txt` (クラス名) を使用して予測を行う。
- **Python環境:** `venv/` ディレクトリ内の仮想環境で動作し、必要なライブラリ (Flask, Flask-CORS, torch, torchvision) がインストールされている。

## ファイル構造の概要

```
location_prediction_project/
├── api.py                  # Flask APIスクリプト
├── class_names.txt         # 予測クラス名リスト
├── model.pth               # 学習済みPyTorchモデルの重み
├── save_model.py           # モデル学習・保存用スクリプト (学習済みモデルのアーキテクチャはDenseNet121)
├── commands.txt            # アプリケーション起動・停止コマンドのまとめ
├── README.md               # このファイル
├── .gitignore              # Git管理から除外するファイル・ディレクトリ
├── venv/                   # Python仮想環境
└── nextjs-app/             # Next.jsフロントエンドアプリケーション
    ├── pages/
    │   └── index.js        # メインのフロントエンドコード
    ├── public/
    ├── styles/
    ├── ...
    └── package.json
```

