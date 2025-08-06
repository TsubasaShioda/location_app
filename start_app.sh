#!/bin/bash

# アプリケーションを停止する
echo "既存のアプリケーションを停止しています..."
lsof -ti :5001 | xargs kill -9
lsof -ti :3000 | xargs kill -9

# 古いログファイルをクリーンアップする
echo "古いログファイルを削除しています..."
rm -f /Users/shiodatsubasa/location_prediction_project/api.log /Users/shiodatsubasa/location_prediction_project/nextjs.log

# APIサーバーを起動する
echo "APIサーバーを起動しています..."
/Users/shiodatsubasa/location_prediction_project/venv/bin/python /Users/shiodatsubasa/location_prediction_project/api.py > /Users/shiodatsubasa/location_prediction_project/api.log 2>&1 &
API_PID=$!
echo "APIサーバーがPID: $API_PID で起動しました。"

# Next.jsアプリケーションを起動する
echo "Next.jsアプリケーションを起動しています..."
cd /Users/shiodatsubasa/location_prediction_project/nextjs-app && npm run dev | tee ../nextjs.log &
NEXTJS_PID=$!
echo "Next.jsアプリケーションがPID: $NEXTJS_PID で起動しました。"

echo "\nアプリケーションの起動が完了しました。"
echo "APIサーバーのログ: /Users/shiodatsubasa/location_prediction_project/api.log"
echo "Next.jsのログ: /Users/shiodatsubasa/location_prediction_project/nextjs.log"
echo "Webブラウザで http://localhost:3000 にアクセスしてください。"
