import numpy as np
from pathlib import Path

def save(path, img):
	with open(Path(path), 'wb') as f:
		f.write(bytes("P5\n", 'utf-8'))
		f.write(bytes(str(img.shape[1]) + " " + str(img.shape[0]) + "\n", 'utf-8'))
		if img.dtype == np.uint8:
			max_value = (2 ** 8) - 1
		else:
			max_value = (2 ** 16) - 1
		f.write(bytes(str(max_value) + "\n", 'utf-8'))
		f.write(np.ascontiguousarray(img).data)

def load(path, verbose=False):
	with open(Path(path), 'rb') as f:
		f.readline()  # P5 not interesting for us
		text = f.readline().decode("utf-8").strip().split(" ")
		width, height = int(text[0]), int(text[1])
		if verbose:
			print("Image size:", width, "x", height)
		max_value = int(f.readline().decode("utf-8").strip())
		bit_depth = int(np.log2(max_value + 1))
		if bit_depth == 8:
			dtype = np.uint8
		else:
			dtype = np.uint16
		if verbose:
			print("Bit depth:", bit_depth)
		img = np.empty((height, width), dtype=dtype)
		f.readinto(img.data)

	return img
