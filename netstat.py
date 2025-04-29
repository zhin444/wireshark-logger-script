import os,subprocess,datetime,sys
from os import path
from multiprocessing import Process
from datetime import datetime,timedelta


## ##########################
## saves netstat and 
## arp command output to file
#############################
def tail(tout=3600):
	#######################################################
	## filename with datetime format 
	## year-month-day@@hour_minute_seconds_useconds.txt
	## example: 2024-06-06@@15_45_23_568449
	if tout == 0: tout = 3600
	file_name = str(datetime.today()).replace(':','_'); 
	file_name = file_name.replace('.','_'); 
	file_name = file_name.replace(' ','@@')+'.txt'
	#****************************************************************************
	#************************ path to save text file ****************************
	file_path = path.join(os.path.splitroot(os.path.realpath(os.path.curdir))[0],
					   path.sep,
					   "users","lbdkn","documents","libros","nature",file_name)
	#****************************************************************************
	########################################################
	########################################################

	############################## 
	## arp command output filename 
	warp_file_path = path.join(os.path.splitroot(os.path.realpath(os.path.curdir))[0],path.sep,"users","lbdkn","documents","libros","nature",'warp_'+file_name)
	##############################
	##############################

	######################################
	## sets the time start(time_now) 
	## and time when the script should end
	time_now = datetime.now()
	time_wait = timedelta(seconds=tout)
	time_end = time_now + time_wait
	######################################
	######################################

	#####################################################################
	## appends the netstat 
	## and arp output to the same file 
	## if the time passed is less than an hour
	#####################################################################
	while ( time_end - time_now ) > timedelta(seconds=1) :
		cmd = f'netstat -b -a -n -o >> "{file_path}"' #command to execute
		subprocess.getoutput(cmd) #executes command
		print(cmd)

		cmd = F'arp -a -v >> "{warp_file_path}"' #command to execute
		subprocess.getoutput(cmd) #executes command
		print(cmd)
		time_now = datetime.now() #updates time
	#####################################################################
	#####################################################################
		
if __name__ == '__main__':
	tout = 0
	try:
		tout = int(sys.argv[1])
	except:
		pass
	
	tail(tout)
