"""Fetch CC BY-SA 4.0 human Mandarin syllable recordings from audio-cmn.

Source: https://github.com/hugolpz/audio-cmn/tree/master/64k/syllabs
Speaker: Chen Wang. Project: Hugo Lopez, PLIDAM–INALCO.
Only first-tone files needed by the teaching cards are downloaded.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import time

from pinyin_audio_sources import SOUND_TO_SYLLABLE

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets' / 'pinyin' / 'mandarin-syllables'
BASE = 'https://raw.githubusercontent.com/hugolpz/audio-cmn/master/64k/syllabs'
SYLLABLES = sorted(set(SOUND_TO_SYLLABLE.values()))


def download(syllable):
    destination = OUTPUT / f'{syllable}.mp3'
    if destination.exists() and destination.stat().st_size > 2000:
        return syllable
    for attempt in range(4):
        result = subprocess.run(
            ['curl', '-fLsS', '--retry', '2', '--retry-all-errors', '--max-time', '30',
             f'{BASE}/cmn-{syllable}.mp3'],
            capture_output=True,
        )
        if result.returncode == 0:
            content = result.stdout
            break
        if attempt == 3:
            raise RuntimeError(f'Download failed for {syllable}: {result.stderr.decode(errors="replace")}')
        time.sleep(attempt + 1)
    if len(content) < 2000 or not (content.startswith(b'ID3') or content[:2] in (b'\xff\xfb', b'\xff\xf3')):
        raise RuntimeError(f'Invalid audio for {syllable}')
    destination.write_bytes(content)
    return syllable


OUTPUT.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=4) as pool:
    completed = list(pool.map(download, SYLLABLES))
print(f'Downloaded {len(completed)} first-tone Mandarin recordings')
