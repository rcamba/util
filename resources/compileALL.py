if __name__ == "__main__":
    import compileall
    import os
    compileall.compile_dir(os.getcwd(), -1)
    os.system("del compileALL.pyc")
