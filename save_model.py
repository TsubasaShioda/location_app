import torch
import os
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import numpy as np
from collections import Counter
from torch.optim.lr_scheduler import StepLR

def save_model():
    """
    指定されたハイパーパラメータでモデルを学習し、保存する関数。
    """
    # --- ハイパーパラメータ設定 ---
    learning_rate = 0.0001
    image_size = 224
    epochs = 30  # レポートに基づき30エポックで学習
    batch_size = 16 # レポートに基づき16
    model_save_path = './model.pth' # モデル保存パス
    class_names_path = './class_names.txt' # クラス名保存パス

    # シード値の設定
    seed_value = 42
    torch.manual_seed(seed_value)
    np.random.seed(seed_value)
    print(f"シード値 {seed_value} が設定されました。")

    # デバイスの設定
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f"計算に {device} を使用します。")

    # データセットのルートディレクトリ (学科サーバーのパスに合わせて要変更)
    # 重要: このパスは学科サーバーの実際のデータセットパスに変更してください。
    data_dir = '/tmp/split_dataset' 
    train_dir = os.path.join(data_dir, 'train')

    if not os.path.exists(train_dir):
        print(f"エラー: データセットディレクトリが見つかりません: {train_dir}")
        print("スクリプト内の `data_dir` を、学科サーバー上のデータセットへの正しいパスに修正してください。")
        return

    # 画像の変換処理
    train_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # データローダーの作成
    train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # クラスの重み付け
    class_counts = Counter(train_dataset.targets)
    class_weights = torch.tensor([len(train_dataset) / class_counts[i] for i in range(len(train_dataset.classes))], dtype=torch.float32)
    class_weights = class_weights.to(device)

    # モデルの定義
    model = models.densenet121(pretrained=True)
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, len(train_dataset.classes))
    model = model.to(device)

    # 損失関数と最適化関数
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = StepLR(optimizer, step_size=7, gamma=0.1)

    # 学習
    print("\n学習を開始します...")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        scheduler.step()
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {running_loss / len(train_loader):.4f}')

    print('学習が完了しました。')

    # モデルの重みを保存
    torch.save(model.state_dict(), model_save_path)
    print(f"モデルを {model_save_path} に保存しました。")

    # クラス名を保存 (推論時にクラスのインデックスと名前を対応させるために必要)
    class_names = train_dataset.classes
    with open(class_names_path, 'w') as f:
        for name in class_names:
            f.write(f"{name}\n")
    print(f"クラス名を {class_names_path} に保存しました。")


if __name__ == '__main__':
    save_model()