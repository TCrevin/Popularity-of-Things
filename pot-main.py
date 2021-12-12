import subprocess

#process0 = subprocess.call(['mkdir', 'test'])
process1 = subprocess.call(['Hit-Count-Engine/main.py'])
process2 = subprocess.call(['Reference-Count-Engine/reference_count_multiprocessing.py'])
#process3 = subprocess.call(['touch', 'test/foobar.txt'])
#with open('test/foobar.txt', 'w') as f:
#    f.write("hello from python")
#    f.close()
#process4 = subprocess.call(['cat', 'test/foobar.txt'])

