"""
Build pdfs from student notebooks. You need a 'report_rubric.pdf' in the same directory as this file.
"""
import sys
import os
import glob
import re

if len(sys.argv)>1:
    paths=sys.argv[1:]
else:
    paths=[os.curdir]

files = []
skiprubric = False

for path in paths:
    if path.startswith('--skip'):
        skiprubric = True
        continue
    if os.path.isdir(path):
        files += glob.glob(os.path.join(path,'*.ipynb'))
    elif os.path.isfile(path):
        files += [path]

rubricPath = os.path.join(os.path.dirname(sys.argv[0]),'report_rubric.pdf')

print("Files:",files)

for afile in files:

    blocks = afile.split('/')
    print("Found blocks:", blocks)
    fname = blocks[-1]
    print("Searching for username in ", blocks[1])
    userRE = re.compile("\((.+)\)")
    m = userRE.search(blocks[1])
    username = m.group(1)
    print("found username:", username)
    #codeDir = '/'.join(blocks[:-1])
    #os.chdir(os.path.join(cwd, codeDir))
    #print("Checking %s" % codeDir)

    fpath, fsrc = os.path.split(afile)
    fRoot = os.path.splitext(fsrc)[0]
    fPDF = os.path.join(fpath, fRoot + '.pdf')
    fDest = '.'.join(['./output/' + username,'out','pdf'])

    if not os.path.exists(fDest):
        cmd = 'jupyter nbconvert --to PDF "%s"' % afile
        print("executing:", cmd)
        result = os.system(cmd)
        if not result:
            if skiprubric:
                cmd = 'mv "%s" "%s"' % (fPDF, fDest)
            else:
                cmd = 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="%s" "%s" "%s"' % (fDest, rubricPath, fPDF)
            print("executing:", cmd)
            result = os.system(cmd)
            if not result:
                print("Complete!", fDest)
                if not skiprubric:
                    os.unlink(fPDF)
            else:
                print("Ack")
        else:
            print("Ack Ack!")
    else:
        print("%s already exists" % fDest)
