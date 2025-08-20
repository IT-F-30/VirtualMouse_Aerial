# VirtualMouse-Aeria

## はじめに
VirtualMouse-Aerialは、空中で手を動かすとその手の動きに合わせてマウスを動かすプログラムです。

# 動作環境
 - Python v3.11.13
 - Rust v1.85.0

## 使い方
- 以下のコマンドを実行するか上記の動作環境の通りに環境を整備してください

#### Windows
```
# Windows (PowerShell)
# winget を使用して Rust と Python をインストールします
winget install --id Rustlang.Rustup -e && winget install --id Python.Python.3.11 -e
# インストール後、新しいターミナルを開いて以下を実行し、バージョンを合わせます
rustup toolchain install 1.85.0
rustup default 1.85.0
```

#### Mac
```
# macOS (Terminal)
# Homebrew を使用して Rust と Python をインストールします
# Homebrew がない場合は https://brew.sh/index_ja からインストールしてください
brew install rust python@3.11

# インストール後、以下を実行しバージョンを合わせます
rustup toolchain install 1.85.0
rustup default 1.85.0
```

### 使い方
以下のコマンドを実行してください

#### windows 
```
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Mac
```
# macOS (Terminal)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 　最後
これでWebカメラが起動し、手の動きでマウスカーソルが動かせるようになるはずです。プログラムを終了するには、Webカメラのウィンドウを選択した状態で q キーを押してください。