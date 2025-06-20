def longest_palindrome(s):
    n = len(s)
    result = ""
    
    def expand(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]
    
    for i in range(n):
        # Odd length palindrome
        p1 = expand(i, i)
        # Even length palindrome
        p2 = expand(i, i+1)

        for p in [p1, p2]:
            if len(p) > 1:
                if len(p) > len(result):
                    result = p
                elif len(p) == len(result) and p < result:
                    result = p

    if result == "":
        print("None")
    else:
        print(result)

# Main
inputStr = input().strip()
longest_palindrome(inputStr)