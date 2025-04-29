import subprocess,tempfile,os,sys
from os import path
from datetime import datetime, timedelta
from multiprocessing import Process, Pipe , freeze_support
defaultTimeout = 3600 ## default time for the script to run
init = '' ## adapter name parameter
adapter=''## actual adapter name
suffix = '' ##adapter suffix used in filename
###################################################################################
cwd = path.join('C:',path.sep,'Program Files','Wireshark','tshark') #path to tshark
###################################################################################
time_wait = timedelta(seconds=defaultTimeout) ## set to default wait time
#woof
#luci
#poof
#poofTON

try:
	########################################################
	## script takes in one agrgument: adapterName@_@waitTime
	## then parses the values into init and time_wait
	########################################################
	split_arg = str(sys.argv[1]).split('@_@')
	init = split_arg[0]
	if split_arg[1] != '':
		time_wait = timedelta(seconds=int(split_arg[1]))
	else:
		time_wait =  timedelta(seconds=defaultTimeout)
	########################################################
	########################################################
except:
	##########################################
	## sets default values if exception arises
	##########################################
	init = 'luci' #default to localhost interface/adapter
	time_wait =  timedelta(seconds=defaultTimeout)
	##########################################
	##########################################

#################################################################
## gets adapter name and suffix based on the parsed variable init
#################################################################
if init=='woof':
    adapter = 'Wi-Fi'
    suffix='WF_'
if init=='luci':
    adapter = 'Adapter for loopback traffic capture'
    suffix = 'LOC_'
if init=='poof':
    adapter = 'ProtonVPN'
    suffix = 'PVP_'
if init=='poofTON': 
    adapter = 'ProtonVPN TUN'
    suffix = 'PVPT_'
if init!='woof' and init!='luci' and init!='poof' and init != 'poofTON':
    adapter = 'Wi-Fi'
    suffix='WF_'
#################################################################
#################################################################


def name_file(ch0):

	time_start = ch0.recv() #time start sent from parent pipe connection
	time_now = datetime.now()
	offset_time = time_now - time_start

	############################################################
	## sets filename and file path location
	## strftime : formats the time using the given format string 
	############################################################
	file_name = suffix + time_now.strftime("%d-%m-%y_%H-%M") + '.pcapng'
	#***************************************************************************************************************
	file_path = path.join('C:',path.sep,'Users','lbdkn','Documents','libros','nature','bark',file_name) ## save path
	#***************************************************************************************************************
	############################################################
	############################################################

	subprocess.getoutput(f'TITLE = {adapter}') #sets the terminal title
	################################################## 
	## sends tshark command through the pipe to parent
	##################################################
	ch0.send(f'"{cwd}" -i "{adapter}" -w "{file_path}" -a duration:{str(time_wait.seconds-offset_time.seconds)} ')
	##################################################
	##################################################

	ch0.close() #closes connection

def check_adapator(ch0):	
	#################### 
	## creates temp file
	fp = tempfile.TemporaryFile(suffix='.txt',delete=False,delete_on_close=False)
	fp.close()
	####################
	####################

	##################################################### 
	## string command that save tshark output to tempfile
	## and then executes it using subprocess.getoutput
	#####################################################
	cmd = '"' + cwd + '" -D >> ' + '"' + fp.name + '"' 
	subprocess.getoutput(cmd)
	#####################################################
	#####################################################

	###############################################
	## opens the temp file 
	## if we find the adapter name in the tempfile 
	## we send the process PID and False
	## to the parent through the Pipe
	## else we send the process PID and True
	###############################################
	fp = open(fp.name)
	if fp.read().find('(' + adapter + ')') == -1:
		fp.close()
		os.remove(fp.name)
		ch0.send((os.getppid(),False,))
		ch0.close()
	else:
		fp.close()
		os.remove(fp.name)
		ch0.send((os.getppid(),True,))
		ch0.close()
	###############################################
	###############################################

def call_process(cmd):
	print(f'CALL: {cmd}') # prints the command we are about to execute 
	subprocess.run(' (' + cmd+') ', shell=True) #executes command

#######################################
## if adapter was available run command 
#######################################
def main_troop(check,cmd):
	if  check:
		Process(target=call_process,args=(cmd,)).start()
	else:
		print(f'NO NETWORK ADAPTER : "{adapter}"') # didn't find a usable adapter
#######################################
#######################################

#############################################
## checks if the script has been running 
## for the required time <time_wait> variable
#############################################
def should_timeout(ch_pipe):
	time_start = ch_pipe.recv()
	ch_pipe.send( (datetime.now() - time_start) < time_wait)
#############################################
#############################################

if __name__=='__main__':
	ADEPT = False
	time_start = datetime.now()
	print( '************' ,adapter, '************' )
	print( f'TIME START: {str(time_start.ctime())}\nTIMEOUT(seconds): {str(time_wait.seconds)}' )
	bExcept = False
	while not ADEPT or not bExcept:
		try:
			if (datetime.now() - time_start) > time_wait:
				print(f'KILLING LOCAL TASK PID {PPID}')
				subprocess.getoutput(f'taskkill /f /t /pid {PPID}')
		except Exception as e:
			print(f'''EXCEPTION KILLING LOCAL TASK {e.args}''')
			
		####################################################################
		## creates a pipe 
		## which is used to check if the selected adapter <adapter> variable
		## is available to tshark 
		####################################################################
		p_adept , ch_adept = Pipe() #parent connection , child connection
		check_process = Process(target=check_adapator,args=(ch_adept,))
		check_process.start()
		####################################################################
		####################################################################


		########################################
		## creates a pipe
		## which is used to get a string command 
		########################################
		p_name , ch_name = Pipe() #parent connection , child connection
		p_name.send(time_start)
		name_process = Process(target = name_file,args=(ch_name,))
		name_process.start()
		########################################
		########################################

		PPID,ADEPT = p_adept.recv() ## process PID and True or False if adapter is available
		cmd = p_name.recv() # command from pipe
		for p in [p_adept,p_name]: p.close() ## closes both pipes

		try:
			troop = Process(target = main_troop,args=( ADEPT ,cmd , )) #if the adapter is available run command
			troop.start()
			troop.join()


			###########################################################
			## creates pipe
			## then sends the time_start to child through pipe
			## then checks if time_wait time has passed
			## since the script started via the function should_timeout
			###########################################################
			p_timeout, ch_timeout = Pipe() # creates pipe
			p_timeout.send(time_start) ## sends time start to child through pipe
			timeout_process = Process(target=should_timeout,args=(ch_timeout,)) # checks if time_wait has passed since the script started
			timeout_process.start()
			###########################################################
			###########################################################

			bExcept = p_timeout.recv()
		except Exception as e:
				bExcept = (datetime.now() - time_start) < time_wait
				print(f'{type(e)}\n{e.args}')
		
		





