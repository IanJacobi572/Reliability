import os
import os
import sys
sys.path.append((os.getcwd()))
import Preprocessing as prp
from subprocess import call
sub = []
for root, dirs, files in os.walk(os.getcwd()):
	for f in files:
		if ('run') in f:
			try:
				call(['python', root + '/'+f])
			except:
				pass