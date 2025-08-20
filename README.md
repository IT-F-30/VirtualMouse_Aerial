# VirtualMouse-Aeria

## はじめに
VirtualMouse-Aerial(以降Aerial)は、空中で手を動かすとその手の動きに合わせてマウスを動かすプログラムです。

# 動作環境
 - Python v3.13.5
 - Rust v1.85.0

## 使い方
- 以下のコマンドを実行するか上記の動作環境の通りに環境を整備してください

``` setup.sh
# Windows (PowerShell)
# winget を使用して Rust と Python をインストールします
winget install --id Rustlang.Rustup -e && winget install --id Python.Python.3.13 -e

# インストール後、新しいターミナルを開いて以下を実行し、バージョンを合わせます
rustup toolchain install 1.85.0
rustup default 1.85.0

# macOS (Terminal)
# Homebrew を使用して Rust と Python をインストールします
# Homebrew がない場合は https://brew.sh/index_ja からインストールしてください
brew install rust python@3.13

# インストール後、以下を実行しバージョンを合わせます
rustup toolchain install 1.85.0
rustup default 1.85.0
```

### 使い方
- 以下のコマンドを実行してください

``` use.sh

```
