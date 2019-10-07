import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Preprocessing import from_ftp
from ftplib import FTP
path = 'C:/Niagara'
remote_path = '/atitest4/'
ftp = FTP('ftp1.onerheem.com')
data_path = 'C:/Niagara/FieldTest'
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir() ]    
for sub in subfolders:
	name = os.path.basename(os.path.normpath(sub))
	start_str = "Niagara-" + name
	dl = from_ftp(str_date_start = "2019-5-1",path=path, remote_path=remote_path, ftp = ftp, start_str = start_str, data_path = sub)
	if __name__ == '__main__':
		dl.ftp_sync()