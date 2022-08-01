import os

try:
	exec(open('module_algo.py').read())
	exec(open('Test_algo.py').read())
	exec(open('Expected_algo.py').read())
	exec(open('merger.py').read())
	print("SUCCESS")
except:
	print("PROCESS FAILED")
