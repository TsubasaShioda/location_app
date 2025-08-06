#!/bin/bash

# アプリケーションを停止する
echo "アプリケーションを停止しています..."

lsof -ti :5001 | xargs kill -9
if [ $? -eq 0 ]; then
    echo "APIサーバー (ポート5001) を停止しました。"
else
    echo "APIサーバー (ポート5001) は実行されていませんでした。"
fi

lsof -ti :3000 | xargs kill -9
if [ $? -eq 0 ]; then
    echo "Next.jsアプリケーション (ポート3000) を停止しました。"
else
    echo "Next.jsアプリケーション (ポート3000) は実行されていませんでした。"
fi

echo "\n停止処理が完了しました。"
