def linear_search(arr, key):
	no_key = "Did not find target ("+str(key)+") in the list."
	for i in range(len(arr)):
		if arr[i] == key:
			key_found = "Found target ("+str(key)+") in list at index " + str(i) + "."
			return key_found
	return no_key

def binary_search(arr, key):
	arr = sorted(arr)
	left = 0
	right = len(arr)-1
	key_found = False
	while (left <= right and not key_found):
		middle = (left+right)//2
		if arr[middle] == key:
			matched_index = middle
			key_found = True
		else:
			if key > arr[middle]:
				left = middle + 1
			else: 
				right = middle - 1
	if key_found:
		found_msg = "Found target ("+str(key)+") in list at index " + str(matched_index) + " of the sorted list."
	else:
		found_msg = "Did not find target ("+str(key)+") in the list."
	return found_msg

def fib_search(arr, key):
	arr = sorted(arr)
	length = len(arr)
	fib_min_1 = 1
	fib_min_2 = 0
	fib_num = fib_min_2+fib_min_1
	while fib_num < length:
		fib_min_2 = fib_min_1
		fib_min_1 = fib_num
		fib_num = fib_min_2 + fib_min_1
	offset = -1
	while fib_num>1:
		i = min(offset + fib_min_2, length-1)
		if arr[i] > key:
			fib_num = fib_min_2
			fib_min_1 = fib_min_1 - fib_min_2
			fib_min_2 = fib_num - fib_min_1
		elif arr[i] < key:
			fib_num = fib_min_1
			fib_min_1 = fib_min_2
			fib_min_2 = fib_num - fib_min_1
			offset = i
		else:
			found_msg = "Found target ("+str(key)+") in list at index " + str(i) + " of the sorted list."
			return found_msg
	if (fib_min_1 == 1 and arr[offset+1] == key):
		return offset+1
	found_msg = "Did not find target ("+str(key)+") in the list."
	return found_msg

print(fib_search([1,2,3,4,5,6,7,8],4))
#print(binary_search([8,3,6,4,1,2,7,5],2))
#print(linear_search([1,2,3,4,5,6,7,8],5))



