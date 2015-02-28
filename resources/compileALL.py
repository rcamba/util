if __name__ == "__main__":
	import compileall, os
	compileall.compile_dir( os.getcwd(), -1)
	os.system("del compileALL.pyc")