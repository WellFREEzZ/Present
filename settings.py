import os

local_dir = os.path.dirname(__file__)
output_dir = os.path.join(local_dir, 'output')
audio_dir = os.path.join(local_dir, 'audio')
input_dir = os.path.join(local_dir, 'input')
datafile = os.path.join(local_dir, 'global.dat')

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)

with open(datafile, 'r') as f:
    font_size, threshold = (int(i) for i in (f.read()).split('|'))

files = {}
i = 1
for f in os.listdir(input_dir):
    if os.path.isfile(os.path.join(input_dir, f)):
        files.update({i: f})
        i += 1
