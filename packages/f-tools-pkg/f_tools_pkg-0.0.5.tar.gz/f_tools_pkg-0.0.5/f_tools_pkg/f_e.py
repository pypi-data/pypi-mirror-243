import os

class yc_e:
    def __init__(self,timeout):
        
        for num in range(0,timeout):
            ret = os.popen("e z").readlines()
            if ret[0].find("sync 0 = 02")!=-1:
                break
        if(num >=timeout):  
            print("can't e command")
            
    def e_k(self):
        os.system("e k")
        
    def e_p(self):
        while True:
            ret = os.popen("e p").readline()
            print(ret)
            if ret.find("Stopped") != -1:
                break
        return int(ret.split(" ")[3].replace(":",""),16)
    
    def e_pu(self):
        while True:
            ret = os.popen("e pu").readline()
            print(ret)
            if ret.find("Stopped") != -1:
                break
        return int(ret.split(" ")[3].replace(":",""),16)

    def e_pr(self):
        while True:
            ret = os.popen("e pr").readline()
            print(ret)
            if ret.find("Stopped") != -1:
                break
        return int(ret.split(" ")[3].replace(":",""),16)
    
    def e_tu(self):
        addr = -1
        ret = os.popen("e tu").readline()
        print(ret)
        if ret.find("CPU") != -1:
            addr = int(ret.split(" ")[3].replace(":",""),16)
        return addr
    
    def e_nu(self):
        addr = -1
        ret = os.popen("e nu").readline()
        print(ret)
        if ret.find("CPU") != -1:
            addr = int(ret.split(" ")[3].replace(":",""),16)
        return addr
    
    def e_cu(self):
        ret = os.popen("e cu").readline()
        print(ret)
        return self.e_au()
        
    def e_bu(self,addr):
        ret = os.popen("e bu " + hex(addr).replace("0x","")).readline()
        print(ret)
    
    def e_ru(self,reg):
        ret = os.popen("e ru "+reg).readline()
        print(ret)
        return [int(ret.split(" ")[1],10),ret.split(" ")[3].strip()]
        
    
    def e_au(self):
        isstop = 0
        pc = 0
        ret = os.popen("e au").readline()
        if ret.find("Stopped") != -1:
            isstop = 1
        else:
            isstop = 0
        pc = int(ret.split(" ")[3].replace(":",""),16)
        return [isstop,pc]
        
        
    def tohex(self,d):
        return hex(d).replace("0x","")
            
    def get_mem_data(self,addr,len):
        result = os.popen("e "+self.tohex(addr)+"l"+self.tohex(len)).readlines()
        odata=[]
        for line in result[1:]:
            for data in line.split(":")[1].strip().split(" "):
                odata.append(int(data,16))
        return odata
    
    def get_byte(self,addr):
        ret = self.get_mem_data(addr,1)
        return ret[0]

    def get_word(self,addr):
        ret = self.get_mem_data(addr,2)
        return ret[0] + (ret[1] << 8)

    def get_dword(self,addr):
        ret = self.get_mem_data(addr,4)
        return ret[0] + (ret[1] << 8) + (ret[2] << 16) + (ret[3] << 24)
    
    def set_data(self,addr,data):
        os.system("e "+self.tohex(addr)+" "+self.tohex(data))

    def set_byte(self,addr,data):
        self.set_data(addr,("%02x" %data))

    def set_word(self,addr,data):
        self.set_data(addr,("%04x" %data))

    def set_dword(self,addr,data):
        self.set_data(addr,("%08x" %data))