"""Compute (all) LCS between two strings with dynamic programming. Modified from 

https://github.com/google-research/lasertagger/blob/8739f5c0c0c03f2b931311fe7fb9339d028ab82d/phrase_vocabulary_optimization.py
"""

class Tree:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


def lcs_dynamic_programing(source, target):
    """Computes the Longest Common Subsequence (LCS).

    Description of the dynamic programming algorithm:
    https://www.algorithmist.com/index.php/Longest_Common_Subsequence

    Args:
        source: List of source tokens.
        target: List of target tokens.

    Returns:
        List of tokens in the LCS.
    """
    table = lcs_table(source, target)
    return backtrack(table, source, target, len(source), len(target))


def lcs_table(source, target):
    """Returns the Longest Common Subsequence dynamic programming table."""
    rows = len(source)
    cols = len(target)
    lcs_table = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if source[i - 1] == target[j - 1]:
                lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
            else:
                lcs_table[i][j] = max(lcs_table[i - 1][j], lcs_table[i][j - 1])
    return lcs_table

def backtrack_single(table, source, target, i, j):
    """回溯 LCS 表来重建 LCS，此方法只能得到一个 LCS。

    Args:
        table: LCS 表，注意该表的大小为 (len(source) + 1) × (len(target) + 1)。
        source: 源字符串，list 形式。
        target: 目标字符串，list 形式。
        i: 当前行的索引。
        j: 当前列的索引。

    Returns:
        LCS 列表。
    """
    if i == 0 or j == 0:
        # 如果i或者j为0，则说明有一方已经是空字符串，此时直接返回空
        return []
    if source[i - 1] == target[j - 1]:  # 为什么不是 source[i] 和 target[j] 呢？实际上就是，因为 table 表的大小是要比实际 source 和 target 长度大 1 的，所以要减 1，不然就 index out of range 了。
        # Append the aligned token to output.
        # 如果 source[i - 1] 和 target[j - 1] 相等，则表示该值便是当前的 source 和 target 的 LCS 的最后一个 token，
        # 然后 source 和 target 分别往前推一个 token 再去寻找，也是一个递归的过程
        return _backtrack(table, source, target, i - 1, j - 1) + [target[j - 1]]
    if table[i][j - 1] > table[i - 1][j]:
        # 如果不相等的话，接下来就是寻找相等的元素，这些元素才可能属于 LCS。
        # 如果不等且 source[:i] 和 target[:j-1] 的 LCS 长度，大于 source[:i-1] 和 target[:j] 的 LCS 长度，
        # 那么就从 source[:i] 和 target[:j-1] 寻找相等的元素
        return _backtrack(table, source, target, i, j - 1)
    else:
        # 和上面同理
        return _backtrack(table, source, target, i - 1, j)

def backtrack(table, source, target, i, j):
    """回溯 LCS 表来重建 LCS，此方法可得到所有 LCS。"""
    tree = Tree()
    if i == 0 or j == 0:
        return Tree()
    if source[i - 1] == target[j - 1]:
        tree.data = target[j - 1]
        tree.left = backtrack(table, source, target, i - 1, j - 1)
        return Tree(
            data=target[j - 1], left=backtrack(table, source, target, i - 1, j - 1)
        )
    if table[i][j - 1] > table[i - 1][j]:
        return Tree(left=backtrack(table, source, target, i, j - 1))
    elif table[i][j - 1] == table[i - 1][j]:
        left = backtrack(table, source, target, i, j - 1)
        right = backtrack(table, source, target, i - 1, j)
        return Tree(left=left, right=right)
    else:
        return Tree(right=backtrack(table, source, target, i - 1, j))


def traverse_tree(root):
    if root is None:
        return []
    if root.left == None and root.right == None:
        return [str(root.data)]
    return [
        str(root.data) + p for p in traverse_tree(root.left) + traverse_tree(root.right)
    ]


def main():
    examples = [("ABCBDAB", "BDCABA"), ("ABDEDA", "ADEBADDA")]
    for s, t in examples:
        tree = lcs_dynamic_programing(s, t)
        paths = traverse_tree(tree)
        paths = [i.replace("None", "")[::-1] for i in paths]
        print(f"LCS between {s} and {t}: {paths}")


if __name__ == "__main__":
    main()
