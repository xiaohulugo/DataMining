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

class Node(object):
    def __init__(self, char):
        self.char = char
        self.word = []
        self.count = 1
        self.children = []
        self.parent = []
        self.isleaf = False
        self.children_visited = []

def build_prefix_tree(list_words, root_node):
    count_word = 0
    for word in list_words:
        node = root_node
        for char in word:
            found = False
            for child in node.children:
                if char == child.char:
                    child.count += 1
                    node = child
                    found = True
                    break
            if not found:
                new_node = Node(char)
                new_node.parent = node
                node.children.append(new_node)
                node.children_visited.append(False)
                node = new_node
        node.isleaf = True
        node.word = word
        count_word += 1

def depth_first_search_recursive(node, key_chars, list_words, list_count):
    if len(list_words)%100 == 0:
        print('size of keys: ' + str(len(list_words)) + '\n')

    for i in range(0, len(node.children)):
        if node.children_visited[i]:
            continue

        # set the child visited
        node.children_visited[i] = True

        # process the child
        child = node.children[i]
        key_chars.append(child.char)
        if child.isleaf:
            key_new = ''.join(key_chars)
            list_words.append(key_new)
            list_count.append(child.count)
            key_chars.pop()
        else:
            node = child
            depth_first_search_recursive(node, key_chars, list_words, list_count)

    # level up if all children are visited
    if node.parent == []:
        return
    else:
        node = node.parent
        key_chars.pop()
        depth_first_search_recursive(node, key_chars, list_words, list_count)

def depth_first_search_nonrecursive(root, list_words, list_count):
    node_to_visit = list()
    node_to_visit.append(root)
    while len(node_to_visit):
        node_cur = node_to_visit.pop()
        for child in node_cur.children:
            node_to_visit.append(child)

        if node_cur.isleaf:
            list_words.append(node_cur.word)
            list_count.append(node_cur.count)


def process_one_file(file_name):
    print(file_name)
    whole_txt = Path(file_name).read_text()
    loc_s = [idx.start() for idx in re.finditer('<BODY>', whole_txt)]
    loc_e = [idx.start() for idx in re.finditer('</BODY>', whole_txt)]
    list_words = list()
    for i in range(0, len(loc_s)):
        content_i = whole_txt[loc_s[i]+6:loc_e[i]-4]
        list_words_i = re.sub("[^\w]", " ",  content_i).split()
        list_words = list_words + list_words_i
    return list_words

def process_one_fold(fold_path, result_words):
    file_names = [f for f in listdir(fold_path) if isfile(join(fold_path, f))]
    
    # reading    
    list_words = []
    for file_name in file_names:
        list_words += process_one_file(fold_path + '\\' + file_name)

    # build prefix tree
    root_node = Node('*')
    build_prefix_tree(list_words, root_node)

    # get words
    list_words = list()
    list_count = list()
    #depth_first_search_recursive(root_node, key_chars, list_words, list_count)
    depth_first_search_nonrecursive(root_node, list_words, list_count)

    # write out
    file_word = open(result_words, 'w')
    for i in range(0, len(list_words)):
        file_word.write(list_words[i] + " " + str(list_count[i]) + "\n")
    file_word.close()

def main():
    fold_path = 'C:\\Media\\Courses\\DataMining\\lab1\\data'
    result_words = 'C:\\Media\\Courses\\DataMining\\lab1\\words.txt'
    process_one_fold(fold_path, result_words)

if __name__ == '__main__':
    main()
