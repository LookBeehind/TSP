def get_elements_above_diagonals(arr):
    n = len(arr)
    m = len(arr[0])

    # List to hold elements above diagonals
    above_diagonals = []

    # Get elements above the main diagonals
    for i in range(n):
        for j in range(m):
            if i < j:  # Elements above the main diagonal (i == j)
                above_diagonals.append(arr[i][j])

    # Get elements above the anti-diagonals
    for i in range(n):
        for j in range(m):
            if i + j < n - 1:  # Elements above the anti-diagonal (i + j == n - 1)
                above_diagonals.append(arr[i][j])

    return above_diagonals


# Example 2D array
arr = [
    [1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2],
    [3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4],
    [5, 5, 5, 5, 5]
]

# Get elements above diagonals
result = get_elements_above_diagonals(arr)
print(result)