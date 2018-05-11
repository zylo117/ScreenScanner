from fs.memoryfs import MemoryFS
mem_fs = MemoryFS()

mem_fs.makedirs("HelloMem")
mem_fs.create("./hello.mem")

print(mem_fs.listdir("./"))

