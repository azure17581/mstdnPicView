#  mstdnPicView
マストドンの公開タイムラインに投稿された画像を閲覧するためのスクリプト。ログインなしでのローカルタイムライン取得 API が許可されているサーバーで使用可能。  
windows かつ Full HD モニタを対象にレイアウトを組んでいるため，ほかの環境ではパラメータを変更する必要があるかも。  
(TODO: ウィンドウサイズを可変にする)

### 注意
- **NSFW / CW （いわゆる閲覧注意）が設定された投稿もそのまま表示されます。**

## 必要なもの
- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)

Python のインストール時に追加できる `tkinter` に依存している？
```
pip install pysimplegui
```
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html)
```
pip install Pillow
```

## 使い方
- `picView.py` を実行すると，閲覧するサーバーのドメインを訊かれるので入力して `OK`。
- `保存` をクリックで現在表示している画像が `img` フォルダに保存される。
- トゥート本文をクリックするとその投稿をブラウザで表示する。