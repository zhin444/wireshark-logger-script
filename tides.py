import subprocess,datetime,sys
from os import path
from multiprocessing import Pool
defaultTimeout = 3600

def woof(parmessan):
	# adapter_name,tout = str(parmessan).split('@_@')
	#****************************************************************************
	#************************ path to save text file ****************************
	cwd=path.join('C:',path.sep,'Users','lbdkn','Documents','libros','nature','bark') #current working directory
	#****************************************************************************
	subprocess.call(f'start python woof.py  "{parmessan}" ' ,cwd=cwd,shell=True) #runs cmd


#########################
## saves wireshark output 
## from 4 interfaces
## wifi:woof
## localhost: luci
## poof: VPN
## poofTON: VPN TUN
#########################
if __name__ == '__main__':
	tout = 0 
	try:
		tout = int(sys.argv[1])
	except Exception as e:
		print(f'EXCEPTION SETTING TIMEOUT {e.args}')

	with Pool(4) as process_pool:
		if tout==0: tout=datetime.timedelta(seconds=defaultTimeout) 
		##########################################################
		## runs the woof function separetly with 4 different parameters
		process_pool.map(woof,[ f'woof@_@{str(tout)}',
						 f'luci@_@{str(tout)}',
						 f'poof@_@{str(tout)}', 
						 f'poofTON@_@{str(tout)}'])
		##########################################################
		##########################################################

	####################################################
	## prints the time left until the process shuts down
	####################################################
	t_now = datetime.datetime.now()
	t_start = t_now
	t_wait = datetime.timedelta(seconds=tout)
	if tout==0: tout=datetime.timedelta(seconds=defaultTimeout)
	print(f'TIMEOUT: {str(t_wait.seconds-300)}')
	####################################################
	####################################################

	###################################################
	## runs for the alotted time tout or defaultTimeout 
	while (datetime.datetime.now()-t_start) < (datetime.timedelta(seconds=t_wait.seconds-300)):
		t_now = datetime.datetime.now()
	###################################################
	###################################################
