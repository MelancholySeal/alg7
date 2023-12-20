#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from heapq import heappush, heappop


def display_tree(hierarchy, level=0, levels=None):
    if levels is None:
        levels = []
    if isinstance(hierarchy, int):
        return

    for i, (node, child) in enumerate(hierarchy.items()):
        if i == len(hierarchy) - 1 and level != 0:
            levels[level - 1] = False
        branch = ''.join('│   ' if lev else '    ' for lev in levels[:-1])
        branch += "└── " if i == len(hierarchy) - 1 else "├── "
        if level == 0:
            print(f"{node}")
        elif isinstance(child, int):
            print(f"{branch}'{node}' ── {child}")
        else:
            print(f"{branch}{str(node).split()[0]}")
        display_tree(child, level + 1, levels + [True])


def build_huffman_tree(frequencies):
    heap = []
    length = len(frequencies)
    visited_frequencies = set()

    for i in frequencies:
        heappush(heap, (frequencies[i], i))

    while len(heap) > 1:
        f1, i = heappop(heap)
        f2, j = heappop(heap)
        fs = f1 + f2
        ord_val = ord('a')
        fl = str(fs)

        while fl in visited_frequencies:
            letter = chr(ord_val)
            fl = str(fs) + " " + letter
            ord_val += 1

        visited_frequencies.add(fl)
        frequencies[fl] = {"{}".format(x): frequencies[x] for x in [i, j]}
        del frequencies[i], frequencies[j]
        heappush(heap, (fs, fl))

    return frequencies


def generate_huffman_codes(tree, codes, path=''):
    for i, (node, child) in enumerate(tree.items()):
        if isinstance(child, int):
            codes[node] = path[1:] + str(abs(i - 1))
        else:
            generate_huffman_codes(child, codes, path + str(abs(i - 1)))
    return codes


def substitute_text(text, code_dict):
    substituted_text = ''
    for char in text:
        if char in code_dict:
            substituted_text += code_dict[char]
        else:
            substituted_text += char
    return substituted_text


def huffman_decode(encoded_text, huffman_tree):
    decoded_text = ""
    key = list(huffman_tree.keys())[0]
    current_node = huffman_tree[key]

    for bit in encoded_text:
        for i, (node, child) in enumerate(current_node.items()):
            if str(i) != bit:
                if isinstance(child, int):
                    decoded_text += node
                    current_node = huffman_tree[key]
                    break
                current_node = child
                break

    return decoded_text


if __name__ == '__main__':
    input_sentence = input("Введите текст: ")
    char_count = {}

    for char in input_sentence:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    print("Подсчет символов:")
    for char, count in char_count.items():
        print(f"   '{char}': {count} раз")

    huff_tree = build_huffman_tree(char_count)
    print("\nДерево Хаффмана:")
    display_tree(huff_tree)

    huff_codes = generate_huffman_codes(huff_tree, dict())
    print("\nКод Хаффмана:")
    for char, code in huff_codes.items():
        print(f"   '{char}': {code}")

    encoded_sentence = str(substitute_text(input_sentence, huff_codes))
    print("\nЗакодированный текст:")
    print(f"   {encoded_sentence}")

    decoded_text = huffman_decode(encoded_sentence, huff_tree)
    print("\nДекодированный текст:")
    print(f"   {decoded_text}")
