from pathlib import Path
import re
import subprocess

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

for kind, mapping, rate in [('sound', sounds, '135'), ('example', examples, '115')]:
    for syllable, text in mapping.items():
        stem = syllable.replace('ü', 'v')
        temporary = output / f'{stem}-{kind}.aiff'
        final = output / f'{stem}-{kind}.wav'
        subprocess.run(['say', '-v', 'Tingting', '-r', rate, '-o', str(temporary), text], check=True)
        subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16', str(temporary), str(final)], check=True)
        temporary.unlink()
        if final.stat().st_size < 5000:
            raise RuntimeError(f'Empty audio: {final}')

print(f'Generated {len(sounds) * 2} Mandarin audio files in {output}')
subprocess.run(['python3', str(root / 'scripts' / 'correct_initial_tones.py')], check=True)
subprocess.run(['python3', str(root / 'scripts' / 'build_audio_sequence.py')], check=True)
