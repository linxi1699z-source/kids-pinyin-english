from pathlib import Path
import re
import subprocess
import wave

import miniaudio

root = Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text()
output = root / 'assets' / 'pinyin'
output.mkdir(parents=True, exist_ok=True)

def read_map(name):
    block = re.search(rf'const {name}=\{{(.*?)\}};', html, re.S).group(1)
    return {key.strip("'"): value for key, value in re.findall(r"('?[a-zü]+'?):'([^']*)'", block)}

sounds = read_map('pinyinVoice')
examples = read_map('pinyinExample')
assert sounds.keys() == examples.keys(), 'Pinyin audio map differs from examples'
native_symbols = set('b p m f d t n l g k h j q x zh ch sh r z c s a o e i u ü ai ei ao ou an en ang eng er'.split())
native_dir = output / 'moe-symbols'
assert all((native_dir / f'{key.replace("ü", "v")}.mp3').exists() for key in native_symbols), 'Missing licensed symbol recordings; run download_moe_symbols.py'

for kind, mapping, rate in [('sound', sounds, '135'), ('example', examples, '115')]:
    for syllable, text in mapping.items():
        stem = syllable.replace('ü', 'v')
        temporary = output / f'{stem}-{kind}.aiff'
        final = output / f'{stem}-{kind}.wav'
        if kind == 'sound' and syllable in native_symbols:
            decoded = miniaudio.decode_file(str(native_dir / f'{stem}.mp3'), nchannels=1, sample_rate=22050)
            with wave.open(str(final), 'wb') as target:
                target.setnchannels(1)
                target.setsampwidth(2)
                target.setframerate(22050)
                target.writeframes(decoded.samples.tobytes())
        else:
            subprocess.run(['say', '-v', 'Tingting', '-r', rate, '-o', str(temporary), text], check=True)
            subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@22050', str(temporary), str(final)], check=True)
            temporary.unlink()
        if final.stat().st_size < 5000:
            raise RuntimeError(f'Empty audio: {final}')

print(f'Generated {len(sounds) * 2} Mandarin audio files in {output}')
subprocess.run(['python3', str(root / 'scripts' / 'build_audio_sequence.py')], check=True)
