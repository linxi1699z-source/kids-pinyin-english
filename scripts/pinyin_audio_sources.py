"""First-tone syllable recordings for the pinyin teaching cards.

Initials use the classroom reading sounds: bō, pō, mō, fō; dē, tē, nē,
lē; and so on. Finals without a standalone syllable use their usual
zero-initial spelling (for example ui -> wēi and iu -> yōu).
"""

SOUND_TO_SYLLABLE = {
    'b': 'bo1', 'p': 'po1', 'm': 'mo1', 'f': 'fo1',
    'd': 'de1', 't': 'te1', 'n': 'ne1', 'l': 'le1',
    'g': 'ge1', 'k': 'ke1', 'h': 'he1',
    'j': 'ji1', 'q': 'qi1', 'x': 'xi1',
    'zh': 'zhi1', 'ch': 'chi1', 'sh': 'shi1', 'r': 'ri1',
    'z': 'zi1', 'c': 'ci1', 's': 'si1',
    'y': 'yi1', 'w': 'wu1',
    'a': 'a1', 'o': 'o1', 'e': 'e1', 'i': 'yi1',
    'u': 'wu1', 'ü': 'yu1',
    'ai': 'ai1', 'ei': 'ei1', 'ui': 'wei1',
    'ao': 'ao1', 'ou': 'ou1', 'iu': 'you1',
    'ie': 'ye1', 'üe': 'yue1', 'er': 'er1',
    'an': 'an1', 'en': 'en1', 'in': 'yin1',
    'un': 'wen1', 'ün': 'yun1', 'ang': 'ang1',
    'eng': 'eng1', 'ing': 'ying1', 'ong': 'weng1',
}

assert len(SOUND_TO_SYLLABLE) == 47
