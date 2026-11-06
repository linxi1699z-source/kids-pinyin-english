from pathlib import Path
import re
import subprocess
import tempfile
import wave

root = Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text()
block = re.search(r'const words=\{(.*?)\};', html, re.S).group(1)
words = re.findall(r"([A-Z]):\['([^']+)','([^']+)'\]", block)
assert len(words) == 26, f'Expected 26 words, found {len(words)}'
output_dir = root / 'assets' / 'english'
output_dir.mkdir(parents=True, exist_ok=True)

def make_wav(folder, name, text, voice, rate):
    aiff = folder / f'{name}.aiff'
    wav = folder / f'{name}.wav'
    subprocess.run(['say', '-v', voice, '-r', str(rate), '-o', str(aiff), text], check=True)
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16', str(aiff), str(wav)], check=True)
    with wave.open(str(wav), 'rb') as source:
        params = source.getparams()
        frames = source.readframes(source.getnframes())
    if len(frames) < 4000:
        raise RuntimeError(f'Empty audio: {name}')
    return params, frames

with tempfile.TemporaryDirectory() as temp:
    folder = Path(temp)
    for letter, word, chinese in words:
        example = 'A box.' if letter == 'X' else f'{word}.'
        translation = '一个盒子。' if letter == 'X' else chinese + '。'
        params, letter_frames = make_wav(folder, f'{letter}-letter', letter, 'Samantha', 155)
        example_params, example_frames = make_wav(folder, f'{letter}-example', example, 'Samantha', 140)
        chinese_params, chinese_frames = make_wav(folder, f'{letter}-chinese', translation, 'Tingting', 115)
        assert all(p.framerate == params.framerate and p.nchannels == params.nchannels and p.sampwidth == params.sampwidth for p in [example_params, chinese_params])
        pause = bytes(params.framerate * params.nchannels * params.sampwidth)
        sequence = pause.join([letter_frames] * 3 + [example_frames, chinese_frames, example_frames, chinese_frames])
        with wave.open(str(output_dir / f'{letter}.wav'), 'wb') as target:
            target.setparams(params)
            target.writeframes(sequence)

print(f'Generated {len(words)} English letter sequences in {output_dir}')
