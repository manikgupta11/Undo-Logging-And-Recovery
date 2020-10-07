import sys
def dprint(dict1,fo):
	"""
	Write variables in output file
	"""
	dstr=""
	for i in sorted(dict1.keys()):
		dstr+=i+" "+str(dict1[i])+" "
	# print(dstr)
	fo.write(dstr[:-1]+"\n")


def round_robin(trans_list,quantum,trans):
	"""
	Perform round robin on different transactions.
	Make one combined list
	"""
	list2=[]
	step1=0
	step2=quantum

	while True:
		flag=0
		for i in range(len(trans_list)):	
			for j in range(step1,step2):
				if j<len(trans_list[i]):
			
					if j==0:
						list2.append([i,"start"])

					list2.append([i,trans_list[i][j]])

					if j==len(trans_list[i])-1:
						list2.append([i,"end"])
					flag=1
		if flag==0:
			break
		
		step1+=quantum
		step2+=quantum
		
	return list2

def readfile(file,x,dvars,mvars,lvars,trans):

	f=open(file)
	input_list=f.readlines()
	input_list=[i.rstrip("\n") for i in input_list]
	vars=input_list[0].split()
	i=0

	#Read disk variables
	while i < len(vars):
		dvars[vars[i]] = int(vars[i+1])
		i+=2
	# print("Disk variables: ", dvars)

	trans_list=[]
	# print(input_list)

	#Read transaction
	for i in range(len(input_list)):
		if input_list[i]=='':continue
		if input_list[i][0]=='T':
			loop=input_list[i].split()[1]
			trans.append(input_list[i].split()[0])
			list2=[]
			for j in range(1,int(loop)+1):
				list2.append(input_list[i+j])
			trans_list.append(list2)
	# print(trans)
	return trans_list

def logging(round_robin_list,dvars,mvars,lvars,trans,fo):
	"""
	Write entries in log file for OUTPUT and WRITE operations
	"""
	for j in round_robin_list:
		# If variable to read is already in memory, copy this to local variable
		# Otherwise read from disk
		# For READ(A, t): If A already in memory, then t=A
		# otherwise read A from disk, then t=A
		if(j[1].startswith("READ")):
			read1=j[1].split('(')[1].split(',')[0]
			read2=j[1].split('(')[1].split(',')[1].split(')')[0]
			if read1 not in mvars.keys():
				mvars[read1]=dvars[read1]
			lvars[read2]=mvars[read1]

		# Copy local variable to memory
		# For WRITE(A, t): make A=t in memory(not disk)	
		elif(j[1].startswith("WRITE")):

			write1=j[1].split('(')[1].split(',')[0]
			write2=j[1].split('(')[1].split(',')[1].split(')')[0]
			fo.write("<"+ trans[j[0]] + ", "+ write1 + ", "+str(mvars[write1]) + ">" + "\n")
			# print("<"+ trans[j[0]] + ", "+ write1 + ", "+str(mvars[write1]) + ">")
			mvars[write1] = lvars[write2]
			dprint(mvars,fo)
			dprint(dvars,fo)

		# Write a variable from memory(if present) to disk 
		# For OUTPUT(A): Write A from memory to disk
		elif(j[1].startswith("OUTPUT")):
			var1=j[1].split('(')[1].split(')')[0]
			for i in mvars.keys():
				dvars[var1]=mvars[var1]

		elif(j[1].startswith("start")):
			# print("<START "+ trans[j[0]] +">")
			fo.write("<START "+ trans[j[0]] +">"+"\n")
			dprint(mvars,fo)
			dprint(dvars,fo)
		elif(j[1].startswith("end")):
			# print("<COMMIT "+ trans[j[0]] +">")
			fo.write("<COMMIT "+ trans[j[0]] +">"+"\n")
			dprint(mvars,fo)
			dprint(dvars,fo)

		else:
			# print(j)
			j[1]=j[1].replace(':','')
			j[1]=j[1].replace(' ','')
			var1=j[1].split('=')[0]
			if len(j[1].split('=')[1].split('*'))==2:
				var2=j[1].split('=')[1].split('*')[0]
				var3=j[1].split('=')[1].split('*')[1]
				lvars[var1]=lvars[var2]*int(var3)
			elif len(j[1].split('=')[1].split('/'))==2:
				var2=j[1].split('=')[1].split('/')[0]
				var3=j[1].split('=')[1].split('/')[1]
				lvars[var1]=lvars[var2]//int(var3)
			elif len(j[1].split('=')[1].split('+'))==2:
				var2=j[1].split('=')[1].split('+')[0]
				var3=j[1].split('=')[1].split('+')[1]
				lvars[var1]=lvars[var2]+int(var3)
			elif len(j[1].split('=')[1].split('-'))==2:
				var2=j[1].split('=')[1].split('-')[0]
				var3=j[1].split('=')[1].split('-')[1]
				lvars[var1]=lvars[var2]-int(var3)
			else:
				pass


def main():
	input_file=sys.argv[1]
	output_file="output.txt"
	x=int(sys.argv[2])
	dvars={} #Variables on disk
	mvars={} #Variables in memory
	lvars={} #Local variables
	trans=[] #transactions nos
	trans_list=readfile(input_file,x,dvars,mvars,lvars,trans)
	round_robin_list=round_robin(trans_list,x,trans)
	# print(round_robin_list)

	fo=open(output_file,"w")
	logging(round_robin_list,dvars,mvars,lvars,trans,fo)
	fo.close()
	# print("Disk variables: ", dvars)
	# print("Memory variables: ", mvars)
	# print("Local variables: ", lvars)

if __name__ == "__main__":
    main()
