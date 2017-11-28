arr = [69, 10, 30, 2, 16, 8, 31, 22]

def swap(arr, x, y):
  arr[x], arr[y] = arr[y], arr[x]

def split(arr, first, last):
  pivot = int((first + last) / 2)
  left = first
  right = last
  while(left < right):
    while(left < right and arr[left] < arr[pivot]):
      left +=1
    while(left < right and arr[right] >= arr[pivot]):
      right -= 1
    if(left < right):
      swap(arr, left, right)
    print(arr)
  swap(arr, pivot, right)
  print(arr)
  return left


def sort(arr, first, last):
  if(first < last):
    pivot = split(arr, first, last)
    sort(arr, first, pivot - 1)
    sort(arr, pivot + 1, last)

sort(arr, 0, len(arr) - 1)