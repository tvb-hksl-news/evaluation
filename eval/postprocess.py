import json
from functools import cache

from .utils import get_latest_split


def build_trie(mapping):
    trie = {}
    for source, target in mapping.items():
        node = trie
        for char in source:
            if char not in node:
                node[char] = {}
            node = node[char]
        node["#leaf"] = target
    return trie


def replace_with_trie(text, trie):
    result = []
    length = len(text)
    i = 0

    while i < length:
        j = i
        node = trie
        target = None
        end = i

        while j < length and text[j] in node:
            node = node[text[j]]
            if "#leaf" in node and (j == length - 1 or text[j + 1] == " "):
                target = node["#leaf"]
                end = j
            j += 1

        if target:  # replace the matched phrase
            result.append(target)
            # print(f"replace: {text[i:end+1]} -> {target}")
            i = end + 1
        else:  # keep the original character
            result.append(text[i])
            i += 1

    return "".join(result)


def load_homosign_groups():
    split_dir = get_latest_split()
    groups = json.load(open(split_dir / "homosigns.json", "r"))
    return groups


@cache
def build_homosign_trie():
    groups = load_homosign_groups()
    mapping = {}
    for group in groups:
        target = max(group, key=lambda x: (len(x.split("+")), -len(x)))
        for gloss in group:
            if gloss != target:
                mapping[gloss.replace("+", " ")] = target.replace("+", " ")
    mapping = dict(sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True))
    return build_trie(mapping)


def postprocess(sentence):
    trie = build_homosign_trie()
    old = sentence
    new = replace_with_trie(old, trie)
    # if old != new:
    #     print(f"postprocess: ")
    #     print(f"  old: {old}")
    #     print(f"  new: {new}")
    return new
