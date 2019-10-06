#pyuic5 -x [FILENAME].ui -o [FILENAME].py
import os
import glob
path = os.getcwd()
new_path = os.path.dirname(os.getcwd())
file_names = glob.glob('*.ui')
py_names = [x.replace('.ui', '.py') for x in file_names]
for x in range(len(file_names)):
    os.system('pyuic5 -x '+file_names[x]+' -o '+py_names[x])
for x in range(len(py_names)):
    os.replace(path+'\\'+py_names[x], new_path+'\\'+py_names[x])