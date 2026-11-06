# 拼音与英语启蒙

适合 4–5 岁儿童的手机学习页面，包含拼音和英语字母识别、短句示例与慢速跟读。

## 使用

直接打开 `index.html`，或在项目目录运行 `python3 -m http.server 4174`，再访问 `http://127.0.0.1:4174/`。

页面音频保存在 `assets/pinyin` 和 `assets/english`，需与 `index.html` 一起保留。点击“听一听”会朗读当前内容；点击“上一个”或“下一个”会自动朗读切换后的内容。

## 音频

拼音声母及部分韵母使用教育部门的示范录音，其余拼音和案例使用系统普通话语音。英文字母名称和案例使用系统美式英语语音。每个拼音或字母读三遍，案例读两遍，每段之间留一秒。音频生成脚本位于 `scripts/`。如需重新生成，先运行 `python3 -m pip install -r requirements-audio.txt`，再依次运行 `python3 scripts/download_moe_symbols.py`、`python3 scripts/generate_audio.py` 和 `python3 scripts/generate_english_audio.py`。

### 拼音录音来源

`assets/pinyin/moe-symbols/*.mp3` 来自台湾教育部《國語注音符號手冊》的注音符号示范录音，经 [Taiwan Lounge 拼音表](https://taiwanlounge.com/resources/pinyin) 转换格式并重命名，按 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权使用。原始录音版权归台湾教育部；本项目将这些录音转换为 WAV、重复三遍并加入停顿和案例朗读。出处：[國語注音符號手冊](https://language.moe.gov.tw/001/Upload/files/site_content/M0001/juyin/html_en/index.html)。
