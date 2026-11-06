# 拼音与英语启蒙

适合 4–5 岁儿童的手机学习页面，包含拼音和英语字母识别、短句示例与慢速跟读。

## 使用

直接打开 `index.html`，或在项目目录运行 `python3 -m http.server 4174`，再访问 `http://127.0.0.1:4174/`。

页面音频保存在 `assets/pinyin` 和 `assets/english`，需与 `index.html` 一起保留。点击“听一听”会朗读当前内容；点击“上一个”或“下一个”会自动朗读切换后的内容。

## 音频

全部 47 个拼音示范音使用一声的人声音节录音，案例使用系统普通话语音。英文字母名称和案例使用系统美式英语语音；字母音频只念字母名称，不读“capital”。每个拼音或字母读三遍，案例读两遍，每段之间留一秒。音频生成脚本位于 `scripts/`。如需重新生成，先运行 `python3 -m pip install -r requirements-audio.txt`，再依次运行 `python3 scripts/download_pinyin_syllables.py`、`python3 scripts/generate_audio.py` 和 `python3 scripts/generate_english_audio.py`。

### 拼音录音来源

`assets/pinyin/mandarin-syllables/*.mp3` 来自 [audio-cmn](https://github.com/hugolpz/audio-cmn) 的 `64k/syllabs` 目录，录音者 Chen Wang；项目由 Hugo Lopez（PLIDAM–INALCO）整理，Nicolas Vion 提供录音软件与技术支持。原音频采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 授权。本项目将其转成 WAV、重复三遍，并与案例朗读组合；由这些录音改编的拼音音频继续按 CC BY-SA 4.0 使用。
