"""Compute (all) LCS between two strings with brute force."""

import re
import itertools


def get_all_subsequences_generator(s):
    for i in range(1, len(s) + 1):
        yield from itertools.combinations(s, i)


def get_all_subsequences(s):
    subs = []
    for i in range(1, len(s) + 1):
        subs.extend(list(itertools.combinations(s, i)))
    return subs


def is_subsequence(subs, s):
    if re.match(".*" + ".*".join(subs) + ".*", s):
        return True
    return False


def lcs_brute_force(s1, s2):
    if len(s1) < len(s2):
        short = s1
        long_ = s2
    else:
        short = s2
        long_ = s1
    cs = []
    for sub in get_all_subsequences_generator(short):
        if is_subsequence(sub, long_):
            cs.append(sub)
    max_len = len(max(cs, key=len))
    return (s for s in cs if len(s) == max_len)


def main():
    examples = [("ABCBDAB", "BDCABA"), ("ABDEDA", "ADEBADDA")]
    for s, t in examples:
        lcs = lcs_brute_force(s, t)
        lcs = ["".join(i) for i in lcs]
        print(f"LCS between {s} and {t}: {lcs}")


if __name__ == "__main__":
    main()
