import os
import sys


def count_lines(file_path):
	with open(file_path, 'r', encoding='utf-8') as file:
		return sum(1 for line in file)
def count_lines_in_directory(directory):
	total_lines = 0
	for root, dirs, files in os.walk(directory):
		for file_name in files:
			if file_name.endswith('.py'):
				file_path = os.path.join(root, file_name)
				lines = count_lines(file_path)
				print(f"{file_path}: {lines} lines")
				total_lines += lines
	return total_lines


def count_folder_lines(directory):
	# You can specify the directory path directly if you prefer
	total_lines = count_lines_in_directory(directory)
	print(f"\nTotal lines in all .py files: {total_lines}")


if __name__ == "__main__":

	reproved = False

	if len(sys.argv) != 2:
		directory_path = None
		print("Usage: python countlines.py <directory_path>\nOr specify a directory path for me to iterate over\n")

	else:
		directory_path = sys.argv[1]


	while directory_path is None:
		display_message = ""
		if reproved:
			display_message += "Invalid directory.\n"
		display_message = "Enter the directory path or hit Ctrl+C to exit.\n"

		try:
			directory_path = input()
			total_lines = count_lines_in_directory(directory_path)
			print(f"\nTotal lines in all .py files: {total_lines}")

		except:
			reproved = True
			pass
