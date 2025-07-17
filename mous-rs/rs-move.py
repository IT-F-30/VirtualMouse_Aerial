# パッケージ名 (mous_rs) をインポート
import mous_rs

print("Rustモジュールの関数を呼び出します...")

# Rustで定義した関数を実行
mous_rs.rsmove(100, 200)
mous_rs.rsclick()

print("完了！")