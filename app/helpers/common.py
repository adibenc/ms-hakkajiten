import os
from pprint import pprint

def scan_dir_rc(dir_path):
	"""
	Recursively scans a directory and returns a list of all files within it.

	Args:
		dir_path: The path to the directory to scan.

	Returns:
		A list of file paths relative to the input directory.
	"""

	result = []
	for filename in os.listdir(dir_path):
		if filename.startswith('.'):
			continue

		file_path = os.path.join(dir_path, filename)

		if os.path.isdir(file_path):
			for child_filename in scan_dir_rc(file_path):
				result.append(os.path.join(filename, child_filename))
		else:
			result.append(filename)

	return result
