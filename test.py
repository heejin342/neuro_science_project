import glob
import os

files_path = os.path.join('C:/MAVE_RawData', '*')
files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
b = str(files[0])
print(files[0])

a = ""
b = b + '/Fp1_FFT.txt'
inFile = open(b, "r", encoding="ANSI")
inList = inFile.readlines()
for inString in inList:
    a += inString
inFile.close()

print(a)


