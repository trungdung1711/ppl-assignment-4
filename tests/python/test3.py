def getDimension(value):
    if isinstance(value, list):
        return [len(value)] + getDimension(value[0])
    
    else:
        return []

arr = [[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]]
print(getDimension(arr))