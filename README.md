# Spam Killer for Misskey

## 依存関係

### ArchLinux

```
pacman -S opencv zbar
```
### Ubuntu

```
apt install -y libopencv-dev libzbar0
```

## 実行方法

```bash
python -m venv .venv

# アクティベート
pip install -r requirements.txt
# コンフィグを用意

python main.py
```

チェンジログは`git-cliff`で生成してます

```bash
git cliff -o CHANGELOG.md
```
