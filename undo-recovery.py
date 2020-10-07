import sys
def read_file(file,log_record,dvars):
    """
    Read input file and initial variables on disk
    """
    f=open(file)
    for i in f:
        log_record.append(i.rstrip('\n'))
    i=0
    # print(log_record)
    diskvars=log_record[0].split()
    for  i in range(0,len(diskvars),2):
        dvars[diskvars[i]] = int(diskvars[i+1])
    # print("DISK vars: ",dvars)

def findcase(log_record,dvars):
    startflag=0
    endflag=0
    for i in log_record[:1:-1]:
        if(i.find("START CKPT")!=-1):
            startflag=1
        elif(i.find("END CKPT")!=-1):
            endflag=1
    # Case1: Neither <START CKPT> nor <END CKPT> present
    if startflag==0 and endflag==0:
        # print("case1: no checkpt")
        case1(log_record,dvars)

    # Case2: Both <START CKPT> and <END CKPT> present
    elif startflag==1 and endflag==1:
        # print("case1: both start  and end checkpt")
        case2(log_record,dvars)

    # Case3: Only <START CKPT> 
    elif startflag==1 and endflag==0:
        # print("case1: only start checkpt")
        case3(log_record,dvars)

    # Case4: Only <END CKPT> 
    else:
        print("End ckpt present but not start ckpt")

def case1(log_record,dvars):
    """
    Case1: Neither <START CKPT> nor <END CKPT> present
    Traverse in reverse from last transaction:
        If transaction is committed: do nothing
        else: write into disk
    """
    committed=[]
    for i in log_record[:1:-1]:
        if(i.find("COMMIT")!=-1):
            committed.append(i.split(" ")[1].split(">")[0])
        elif(i[1]=='T'):
            trans=i.replace(" ","").split(',')[0].split('<')[1]
            var=i.replace(" ","").split(',')[1]
            val=int(i.replace(" ","").split(',')[2].split('>')[0])
            if trans not in committed:
                dvars[var]=val
    # print("committed: ",committed)

def case2(log_record,dvars):
    """
    Case2: Both <START CKPT> and <END CKPT> present
    Traverse in reverse from last transaction upto <START CKPT> only:
        If transaction is committed: do nothing
        else: write into disk
    """
    idx=-1
    committed=[]
    for i in range(len(log_record)):
        j=log_record[i].find("START CKPT")
        if(j!=-1): 
            idx=i
            break

    for i in log_record[:idx:-1]:
        if(i.find("COMMIT")!=-1):
            committed.append(i.split(" ")[1].split(">")[0])
        elif(i[1]=='T'):
            trans=i.replace(" ","").split(',')[0].split('<')[1]
            var=i.replace(" ","").split(',')[1]
            val=int(i.replace(" ","").split(',')[2].split('>')[0])
            if trans not in committed:
                dvars[var]=val
    # print("committed: ",committed)
    # print("dvars: ",dvars)

def case3(log_record,dvars):
    """
    # Case3: Only <START CKPT> 
    Traverse in reverse from last transaction upto last transaction in <START CKPT(T1,...Tk)>
        If transaction is committed: do nothing
        else: write into disk
    """
    idx=-1
    committed=[]
    ckpttrans=[]
    for i in range(len(log_record)):
        if log_record[i].find("START CKPT")!=-1:
            trans=log_record[i].split("(")[1].replace(" ","").rstrip(")>")
            for i in trans.split(','):
                ckpttrans.append(i)
        
    # print(ckpttrans)

    for i in log_record[:1:-1]:
        if len(ckpttrans)==0:
            break
        elif(i.find("COMMIT")!=-1):
            committed.append(i.split(" ")[1].split(">")[0])
        elif(i[1]=='T'):
            # print(i)
            trans=i.replace(" ","").split(',')[0].split('<')[1]
            var=i.replace(" ","").split(',')[1]
            val=int(i.replace(" ","").split(',')[2].split('>')[0])
            if trans not in committed:
                dvars[var]=val
        elif(i.find("START")!=-1):
            trans=i.split(" ")[1].split(">")[0]
            # print("trans: ",trans)
            if trans in ckpttrans:
                ckpttrans.remove(trans)

    # print("committed: ",committed)
    # print("dvars: ",dvars)
 
def main():
    log_record=[]
    dvars={} # Variables on disk
    input_file = sys.argv[1]
    output_file="output.txt"
    read_file(input_file,log_record,dvars)
    findcase(log_record,dvars)
    fo=open(output_file,'w')
    dstr=""
    for i in sorted(dvars.keys()):
        dstr+=i+" "+str(dvars[i])+" "
    fo.write(dstr[:-1]+"\n")
    fo.close()
    # print("dvars: ",dvars)

if __name__ == "__main__":
    main()