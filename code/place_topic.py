# System libs
import os
from os import listdir
from os.path import isfile, join
import re
from pathlib import Path

# Numerical libs
import numpy as np
from scipy.io import loadmat
import collections

def process_one_object(content):
    list_place = list()
    loc_place1 = content.find('<PLACES>')
    loc_place2 = content.find('</PLACES>')
    if loc_place1 != -1 and loc_place2 != -1:
        string_place = content[loc_place1:loc_place2]
        loc_s = [idx.start() for idx in re.finditer('<D>', string_place)]
        loc_e = [idx.start() for idx in re.finditer('</D>', string_place)]
        for i in range(0, len(loc_s)):
            list_place.append(string_place[loc_s[i]+3:loc_e[i]])
    
    list_topic = list()
    loc_topic1 = content.find('<TOPICS>')
    loc_topic2 = content.find('</TOPICS>')
    if loc_topic1 != -1 and loc_topic2 != -1:
        string_topic = content[loc_topic1:loc_topic2]
        loc_s = [idx.start() for idx in re.finditer('<D>', string_topic)]
        loc_e = [idx.start() for idx in re.finditer('</D>', string_topic)]
        for i in range(0, len(loc_s)):
            list_topic.append(string_topic[loc_s[i]+3:loc_e[i]])

    return list_place, list_topic     


def process_one_file(file_name, list_place, list_topic, list_counts):
    print(file_name)
    whole_txt = Path(file_name).read_text()
    loc_s = [idx.start() for idx in re.finditer('<REUTERS', whole_txt)]
    loc_e = [idx.start() for idx in re.finditer('</REUTERS>', whole_txt)]
    for i in range(0, len(loc_s)):
        content_i = whole_txt[loc_s[i]-8:loc_e[i]]
        list_place_i, list_topic_i = process_one_object(content_i)
        list_place += list_place_i
        list_topic += list_topic_i

        if len(list_place_i) == 0:
            list_counts[0] += 1
        if len(list_topic_i) == 0:
            list_counts[1] += 1
        list_counts[2] += 1
            
def process_one_fold(fold_path, result_place, result_topic):
    file_names = [f for f in listdir(fold_path) if isfile(join(fold_path, f))]
    
    # reading    
    list_place = list()
    list_topic = list()
    list_counts = [0, 0, 0]
    for file_name in file_names:
        process_one_file(fold_path + '\\' + file_name, list_place, list_topic, list_counts)
    
    # counting
    counter_place = collections.Counter(list_place)
    file_palce = open(result_place, 'w')
    for name, num in counter_place.items():
        file_palce.write(name + " " + str(num) + "\n")
    file_palce.close()

    counter_topic = collections.Counter(list_topic)
    file_topic = open(result_topic, 'w')
    for name, num in counter_topic.items():
        file_topic.write(name + " " + str(num) + "\n")
    file_topic.close()

    print(str(list_counts[0]) + ' of ' + str(list_counts[2]) + ' data objects have no entries for PLACES')
    print(str(list_counts[1]) + ' of ' + str(list_counts[2]) + ' data objects have no entries for TOPICS')


def main():
    fold_path = 'C:\\Media\\Courses\\DataMining\\lab1\\data'
    result_place = 'C:\\Media\\Courses\\DataMining\\lab1\\place.txt'
    result_topic = 'C:\\Media\\Courses\\DataMining\\lab1\\topic.txt'
    process_one_fold(fold_path, result_place, result_topic)

if __name__ == '__main__':
    main()