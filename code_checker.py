#!/usr/bin/env python
# coding: utf-8


import os
import re
from tqdm import tqdm
from simhash import Simhash


def get_file_list(folder_path):
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if 'jquery' in file_path.lower():
                continue
            if 'Scrabble_Pieces_AssociativeArray_Jesse.js' in file_path:
                continue
            if file_path[-3:] == '.js':
                file_list.append(file_path)
    return file_list


def extract_content(file_path):

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ''
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )

    with open(file_path, 'r') as file:
        content = file.read()

    # remove comments
    content = re.sub(pattern, replacer, content)

    # remove spaces and newlines
    return ' '.join(content.split())


if __name__ == "__main__":

    folder_path = '/Graphical User Interface Programming 1/HW5/Student Submissions/'

    file_list = get_file_list(folder_path)
    # file_list = file_list[:10]
    print('Total files: ', len(file_list))
    
    max_distance = 20
    top_similar_files = []
    for i in tqdm(range(len(file_list))):
        for j in range(i, len(file_list)):
            if i == j:
                continue
            file_a = extract_content(file_list[i])
            file_b = extract_content(file_list[j])
            hashed_file_a = Simhash(file_a)
            hashed_file_b = Simhash(file_b)
            distance = hashed_file_a.distance(hashed_file_b)
            if distance > max_distance:
                continue
            top_similar_files.append((distance, file_list[i].replace(folder_path, ''), file_list[j].replace(folder_path, '')))
            top_similar_files.sort(key = lambda x :x[0])

    for dis, file_a, file_b in top_similar_files:
        print(dis)
        print(file_a)
        print(file_b)
        print('---')


