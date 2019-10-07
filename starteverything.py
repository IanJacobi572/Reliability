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
			if len(sys.argv) > 1:
				for d in sys.argv[1:]:
					if d in root:
						call(['python', root + '/'+f])
			else:
				call(['python', root + '/'+f])