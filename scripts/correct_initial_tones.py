"""Replace the falling vowel in selected teaching sounds with a level-tone vowel.

The source vowel comes from a first-tone syllable with the same final. Keep
the initial consonant from each original sound. This avoids relying on a
fourth-tone Chinese character as the pronunciation guide for l, n, and t.
"""
from pathlib import Path
from array import array
import wave

audio_dir = Path(__file__).resolve().parents[1] / 'assets' / 'pinyin'

def read(name):
    with wave.open(str(audio_dir / f'{name}-sound.wav'), 'rb') as stream:
        return stream.getparams(), array('h', stream.readframes(stream.getnframes()))

def write(name, params, data):
    with wave.open(str(audio_dir / f'{name}-sound.wav'), 'wb') as stream:
        stream.setparams(params)
        stream.writeframes(data.tobytes())

# target: (first-tone source, target onset length in seconds, source vowel start)
edits = {
    'd': ('g', .025, .045),
    't': ('g', .095, .045),
    'n': ('g', .045, .045),
    'l': ('g', .045, .045),
    'f': ('b', .075, .050),
    'c': ('z', .105, .055),
    'r': ('sh', .045, .100),
}

for target, (source, onset_seconds, source_seconds) in edits.items():
    params, original = read(target)
    source_params, donor = read(source)
    assert (params.framerate, params.nchannels, params.sampwidth) == (source_params.framerate, source_params.nchannels, source_params.sampwidth)
    rate = params.framerate
    cut = int(onset_seconds * rate)
    source_start = int(source_seconds * rate)
    # The source file already has trailing quiet frames; trim after 240 ms.
    vowel = donor[source_start:min(len(donor), int(.24 * rate))]
    fade = int(.008 * rate)
    result = array('h', original[:cut - fade])
    for i in range(fade):
        blend = (original[cut - fade + i] * (fade - i) + vowel[i] * i) / fade
        result.append(int(blend))
    result.extend(vowel[fade:])
    tail = min(int(.012 * rate), len(result))
    for i in range(tail):
        result[-tail + i] = int(result[-tail + i] * (tail - i) / tail)
    write(target, params, result)

print('Corrected first-tone teaching sounds:', ', '.join(edits))
