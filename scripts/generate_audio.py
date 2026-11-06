from pathlib import Path
import re
import subprocess
import wave

import miniaudio
from pinyin_audio_sources import SOUND_TO_SYLLABLE

root = Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text()
output = root / 'assets' / 'pinyin'
output.mkdir(parents=True, exist_ok=True)

def read_map(name):
    block = re.search(rf'const {name}=\{{(.*?)\}};', html, re.S).group(1)
    return {key.strip("'"): value for key, value in re.findall(r"('?[a-zü]+'?):'([^']*)'", block)}

examples = read_map('pinyinExample')
assert SOUND_TO_SYLLABLE.keys() == examples.keys(), 'Pinyin audio map differs from examples'
native_dir = output / 'mandarin-syllables'
assert all((native_dir / f'{name}.mp3').exists() for name in SOUND_TO_SYLLABLE.values()), 'Missing syllable recordings; run download_pinyin_syllables.py'

for kind, rate in [('sound', '135'), ('example', '115')]:
    for syllable, text in examples.items():
        stem = syllable.replace('ü', 'v')
        temporary = output / f'{stem}-{kind}.aiff'
        final = output / f'{stem}-{kind}.wav'
        if kind == 'sound':
            source = native_dir / f'{SOUND_TO_SYLLABLE[syllable]}.mp3'
            decoded = miniaudio.decode_file(str(source), nchannels=1, sample_rate=22050)
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

print(f'Generated {len(examples) * 2} Mandarin audio files in {output}')
subprocess.run(['python3', str(root / 'scripts' / 'build_audio_sequence.py')], check=True)
