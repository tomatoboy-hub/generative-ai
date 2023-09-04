# generative-ai
StableDiffusionのAPIを用いたwebアプリケーション

## 仮想環境の作成とアクティベーション

### 新しい venv 仮想環境を作成

- **Linux/Mac**:
    ```bash
    python3 -m venv new_venv_directory
    ```

- **Windows**:
    ```bash
    python -m venv new_venv_directory
    ```

### 仮想環境をアクティブにする

- **Linux/Mac**:
    ```bash
    source new_venv_directory/bin/activate
    ```

- **Windows**:
    ```bash
    new_venv_directory\Scripts\activate
    ```


## 依存関係のインストール

`requirements.txt`があるディレクトリに移動
 ```bash
 cd generative_ai/100pro
 ```


`requirements.txt` から依存関係をインストールします。

```bash
pip install -r requirements.txt
```

## Djangoアプリケーションの起動
`manage.py` があるディレクトリに移動 100proにある
以下を実行して表示されるURLを開く
```bash
python manage.py runserver
```
