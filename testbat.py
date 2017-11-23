import os

basedir= os.path.abspath(os.path.dirname(__file__))

bat_path=os.path.join(basedir, 'running.bat')

print(bat_path)

if os.path.isfile(bat_path):
    os.system(bat_path)