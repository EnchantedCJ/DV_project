import os

for root,subdirs,files in os.walk('./'):
    if root == './':
        for i, subdir in enumerate(subdirs):
            print(subdir)
            os.rename(subdir, 'TZ%04d' % (i+1))
        exit(0)