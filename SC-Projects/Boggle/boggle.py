"""
File: boggle.py
Name: Kevin Chen
----------------------------------------
Thank a lot for Sean's hint :D
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'

dictionary = []
total = []


def main():
	# creating boggle grid
	grid = fill_gird()
	# Run the boggle game if the grid exists
	if grid is not None:
		play_boggle(grid)


def play_boggle(grid):
	global total
	read_dictionary()
	used = []
	# Call helper function
	for y in range(4):
		for x in range(4):
			cur_s = grid[y][x]
			# append the index of starting letter(a tuple)
			used.append((y, x))
			# running recursive function
			boggle_helper(grid, cur_s, used, y, x)
			# remove (y, x) from 'used'
			used.remove((y, x))
	# print the number of found words when it got out of helper
	print('There are', len(total), 'words in total.')


def boggle_helper(grid, cur_s, used, y, x):
	# Find a adjacent element
	for j in range(-1, 2):
		for i in range(-1, 2):
			if (i, j) != (0, 0):
				if 0 <= x + i <= 3 and 0 <= y+j <= 3 and (y+j, x+i) not in used:
					# Choose
					# New element(new_y, new_x)
					now_y = y+j
					now_x = x+i
					# append the index(tuple) to 'used'
					used.append((now_y, now_x))
					# add the letter to cur_s
					cur_s += grid[now_y][now_x]
					# Check if cur_s is a sub_string in the dictionary
					if has_prefix(cur_s):
						# Check if the cur_s is a word in the dictionary
						if len(cur_s) >= 4 and cur_s in dictionary and cur_s not in total:
							print(f'Found "{cur_s}"')
							total.append(cur_s)
						# Explore (doing recursive)
						boggle_helper(grid, cur_s, used, now_y, now_x)
					# Un-choose (pop the last letter of cur_s, and remove the last element of 'used')
					cur_s = cur_s[:len(cur_s)-1]
					used.pop(-1)


def fill_gird():
	"""
	This function will let users create the boggle grid
	return grid(dict) if valid, else, return None
	"""
	grid = {}
	for i in range(4):
		s = input(f'{i + 1} row of letters: ')
		lst = s.split()
		if len(lst) != 4 or len(''.join(lst)) != 4 or not ''.join(lst).isalpha():
			print('Illegal input')
			return None
		for j in range(4):
			lst[j] = lst[j].lower()
		grid[i] = lst
	return grid

def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	# load data into the dictionary(list) word by word
	global dictionary
	with open(FILE, 'r') as f:
		for word in f:
			dictionary += word.split('\n')


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for word in dictionary:
		if word.startswith(sub_s):
			return True
	return False


if __name__ == '__main__':
	main()
