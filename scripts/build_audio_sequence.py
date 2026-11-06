from pathlib import Path
import wave

audio_dir = Path(__file__).resolve().parents[1] / 'assets' / 'pinyin'
sounds = sorted(audio_dir.glob('*-sound.wav'))
assert len(sounds) == 47, f'Expected 47 pinyin sounds, found {len(sounds)}'

for sound_path in sounds:
    stem = sound_path.name.removesuffix('-sound.wav')
    example_path = audio_dir / f'{stem}-example.wav'
    with wave.open(str(sound_path), 'rb') as source:
        params = source.getparams()
        sound = source.readframes(source.getnframes())
    with wave.open(str(example_path), 'rb') as source:
        assert source.getframerate() == params.framerate
        assert source.getnchannels() == params.nchannels
        assert source.getsampwidth() == params.sampwidth
        example = source.readframes(source.getnframes())
    silence = bytes(params.framerate * params.nchannels * params.sampwidth)
    sequence = silence.join([sound, sound, sound, example, example])
    with wave.open(str(audio_dir / f'{stem}.wav'), 'wb') as output:
        output.setparams(params)
        output.writeframes(sequence)
    sound_path.unlink()
    example_path.unlink()

print(f'Built {len(sounds)} pinyin sequences, each with 1-second pauses')
