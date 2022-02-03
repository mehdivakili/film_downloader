import pysubs2
import os

base_dir = 'E:\\Video\\'
delay = int(input())
for i in range(int(input()), int(input()) + 1):
    if os.path.exists(rf'{base_dir}bleach {i:03d}.srt'):
        subs = pysubs2.load(rf'{base_dir}bleach {i:03d}.srt')
        subs.shift(s=delay)
        subs.save(rf'{base_dir}bleach {i:03d}.srt')
