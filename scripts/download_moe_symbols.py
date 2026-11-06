"""Download the CC BY 4.0 Mandarin phonetic symbol recordings used by Taiwan Lounge.

The files are unaltered conversions of recordings from Taiwan's Ministry of
Education Manual of the Phonetic Symbols of Mandarin Chinese. See README.md.
Run once when preparing audio assets; generate_audio.py uses the local copies.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets' / 'pinyin' / 'moe-symbols'
INITIALS = 'b p m f d t n l g k h j q x zh ch sh r z c s'.split()
FINALS = 'a o e eh i u v ai ei ao ou an en ang eng er'.split()
SYMBOLS = INITIALS + FINALS
BASE = 'https://taiwanlounge.com/assets/audio/pinyin'


def download(initial):
    destination = OUTPUT / f'{initial}.mp3'
    if destination.exists() and destination.stat().st_size > 2000:
        return initial
    for attempt in range(4):
        result = subprocess.run(
            ['curl', '-fLsS', '--retry', '2', '--retry-all-errors', '--max-time', '20', f'{BASE}/{initial}.mp3'],
            capture_output=True,
        )
        if result.returncode == 0:
            content = result.stdout
            break
        if attempt == 3:
            raise RuntimeError(f'Download failed for {initial}: {result.stderr.decode(errors="replace")}')
        time.sleep(attempt + 1)
    if not content.startswith(b'ID3') or len(content) < 2000:
        raise RuntimeError(f'Invalid source audio: {initial}')
    destination.write_bytes(content)
    return initial


OUTPUT.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=2) as pool:
    completed = list(pool.map(download, SYMBOLS))
print(f'Downloaded {len(completed)} attributed Mandarin phonetic symbol recordings')
