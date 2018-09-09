def search(arr, el, beg, end, spec = True):
	if len(arr) == 0:
		return None
	if spec:
		i = (end - beg) // 2 + beg
		if end - beg == 1 and arr[beg][0] != el:
			return None
		if el == arr[i][0]:
			return i
		elif el < arr[i][0]:
			return search(arr, el, 0, i)
		else:
			return search(arr, el, i, len(arr))
	else:
		i = (end - beg) // 2 + beg
		if end - beg == 1 and arr[beg].uid != el:
			return None
		if el == arr[i].uid:
			return i
		elif el < arr[i].uid:
			return search(arr, el, 0, i, spec = False)
		else:
			return search(arr, el, i, len(arr), spec = False)

def silly_search(arr, el):
	for i in range(len(arr) - 1, -1, -1):
		if arr[i].uid == el:
			return i
	return None

def silly_search_vk(arr, el):
	for i in range(len(arr) - 1, -1, -1):
		if arr[i].guid == el:
			return i
	return None

def search_vk(arr, el, beg, end):
	if len(arr) == 0:
		return None
	i = (end - beg) // 2 + beg
	if end - beg == 1 and arr[beg].guid != el:
		return None
	if el == arr[i].guid:
		return i
	elif el < arr[i].guid:
		return search_vk(arr, el, 0, i)
	else:
		return search_vk(arr, el, i, len(arr))
