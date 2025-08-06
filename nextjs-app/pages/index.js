import { useState } from 'react';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [confidenceResult, setConfidenceResult] = useState(null); // 信頼度を追加
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setPredictionResult(null);
    setConfidenceResult(null); // 信頼度もリセット
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('画像ファイルを選択してください。');
      return;
    }

    setLoading(true);
    setError(null);
    setPredictionResult(null);
    setConfidenceResult(null); // 信頼度もリセット

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://localhost:5001/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'APIからの応答に失敗しました。');
      }

      const data = await response.json();
      setPredictionResult(data.prediction);
      setConfidenceResult(data.confidence); // 信頼度を設定
    } catch (err) {
      setError(err.message || '画像のアップロード中にエラーが発生しました。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>地域予測アプリ</h1>
      <p style={styles.description}>風景画像をアップロードして、どの地域か予測します。</p>

      <div style={styles.uploadBox}>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={styles.fileInput}
        />
        <button onClick={handleUpload} disabled={loading} style={styles.button}>
          {loading ? '予測中...' : '画像をアップロードして予測'}
        </button>
      </div>

      {error && <p style={styles.errorMessage}>エラー: {error}</p>}

      {predictionResult && (
        <div style={styles.resultBox}>
          <h2 style={styles.resultTitle}>予測結果:</h2>
          <p style={styles.resultText}>
            {predictionResult}
            {confidenceResult !== null && (
              <span style={styles.confidenceText}> (信頼度: {(confidenceResult * 100).toFixed(2)}%)</span>
            )}
          </p>
        </div>
      )}

      {selectedFile && (
        <div style={styles.previewBox}>
          <h2 style={styles.previewTitle}>選択された画像:</h2>
          <img
            src={URL.createObjectURL(selectedFile)}
            alt="Preview"
            style={styles.previewImage}
          />
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    maxWidth: '800px',
    margin: '50px auto',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    textAlign: 'center',
    backgroundColor: '#f9f9f9',
  },
  title: {
    color: '#333',
    fontSize: '2.5em',
    marginBottom: '10px',
  },
  description: {
    color: '#666',
    fontSize: '1.1em',
    marginBottom: '30px',
  },
  uploadBox: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '20px',
    marginBottom: '30px',
  },
  fileInput: {
    padding: '10px',
    border: '1px solid #ccc',
    borderRadius: '5px',
    width: '100%',
    maxWidth: '300px',
  },
  button: {
    backgroundColor: '#0070f3',
    color: 'white',
    padding: '12px 25px',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '1.1em',
    transition: 'background-color 0.3s ease',
  },
  buttonHover: {
    backgroundColor: '#005bb5',
  },
  errorMessage: {
    color: 'red',
    marginTop: '20px',
    fontWeight: 'bold',
  },
  resultBox: {
    marginTop: '30px',
    padding: '20px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: '#e6f7ff',
  },
  resultTitle: {
    color: '#005bb5',
    fontSize: '1.8em',
    marginBottom: '10px',
  },
  resultText: {
    color: '#333',
    fontSize: '1.5em',
    fontWeight: 'bold',
  },
  previewBox: {
    marginTop: '30px',
    padding: '20px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: '#fff',
  },
  previewTitle: {
    color: '#333',
    fontSize: '1.5em',
    marginBottom: '15px',
  },
  previewImage: {
    maxWidth: '100%',
    height: 'auto',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  confidenceText: {
    fontSize: '0.8em',
    color: '#555',
    marginLeft: '10px',
  },
};