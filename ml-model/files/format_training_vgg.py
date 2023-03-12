from pathlib import Path
from os import listdir, walk

import pandas as pd

from tqdm import tqdm

from random import randrange


current_path = Path(__file__).parent

first_files = []
second_files = []
values = []

original_file_paths = []
transformed_image_file_paths = []

folders = [f for f in (current_path / 'output').iterdir()
           if f.is_dir()]

for i in tqdm(folders, desc='Iterating thru folders'):
    og_file = i / 'original_file.jpeg'

    transformed_folder = i / 'transformed'

    og_file_path = f'output/{i}/original_file.jpeg'
    original_file_paths.append(og_file_path)

    for transformed in listdir(transformed_folder):
        same_file = f'output/{i}/transformed/{transformed}'

        transformed_image_file_paths.append((same_file, og_file_path))

        first_files.append(og_file_path)
        second_files.append(same_file)
        values.append(1)

for i in tqdm(transformed_image_file_paths, desc='Adding negative examples'):

    while True:
        rand_file = original_file_paths[randrange(0, len(original_file_paths))]

        if rand_file != i[1]:
            break

    first_files.append(rand_file)
    second_files.append(i[0])
    values.append(0)


pd.DataFrame({
    'first_file': first_files,
    'second_file': second_files,
    'output': values
}).to_csv('paths_output.csv')
