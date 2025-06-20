def preprocess(s):
    return "^#" + "#".join(s) + "#$"

def manachers_algorithm(s):
    T = preprocess(s)
    n = len(T)
    P = [0] * n
    C = 0  # center of the current palindrome
    R = 0  # right boundary of the current palindrome

    for i in range(1, n - 1):
        mirror = 2 * C - i
        if i < R:
            P[i] = min(R - i, P[mirror])
        
        # Attempt to expand palindrome centered at i
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1

        # Update center and right boundary if expanded past R
        if i + P[i] > R:
            C = i
            R = i + P[i]

    max_len = 0
    res = []

    for i in range(1, n - 1):
        length = P[i]
        if length > 1:
            start = (i - length) // 2  # map back to original string
            substr = s[start:start + length]
            if length > max_len:
                max_len = length
                res = [substr]
            elif length == max_len:
                res.append(substr)

    if not res:
        print("None")
    else:
        print(min(res))  # lexicographically smallest

# Main
inputStr = input().strip()
manachers_algorithm(inputStr)
