#!/user/bin/python3
import os
import json
import re
import string
from time import sleep


class HandleLogClass:
    
    ''' log name '''
    logname = "/log.txt"
   
            
    def enter(self):
        print ('-- start handle log --')
    
    def end(self):
        print ('-- handle ending --')
    
    def __init__(self):
        
        self.rootpath = os.path.dirname(os.path.realpath(__file__));
        self.logpath = self.rootpath + self.logname
        print ('The log path : %s' % (self.logpath))
 
   
    '''     
    def print_debug(self):
        print 'data = 0x%x   addr =0x%x ' % (self.data,self.addr) 
        print 'id(data) = 0x%x   id(addr) =0x%x ' % (id(self.data),id(self.addr)) 
    '''
    
    def txt_num_line(self):
        self.numline = sum(1 for line in open(self.logpath))
        print (self.numline)
       
    def show_line_data(self):
        fd = open(self.logpath,"r") 
        for line in fd.readlines():
            print (line)

        fd.close()
        
    def get_key_value(self):
        fd = open(self.logpath,"r")
        
        _addr_value = "";
        _data_value = ""; 
        _len_value = "";
        _cmd  = "";
        
        for line in fd.readlines():                      
            #print line      #debug
            if 'Read' in line or 'Write' in line :
                 
                wxlist= re.split(r',',line)   #wxlist is list format data
            
                for index in range(len(wxlist)):
                    _str = wxlist[index]      #addr=0x111  
       
                    if 'offset' in _str:
                        # print 'offset'
                         _local = _str.find('=')   
                         str_value = _str[_local+1:len(_str)]    #0x
                         _addr_value = str_value
                    
                         if 'Read' in _str:
                             _cmd = "read"
                         elif 'Write' in _str:
                             _cmd = "write" 
                    elif 'data' in _str:
                        # print 'data'
                         _local = _str.find('=')   
                         str_value = _str[_local+1:len(_str)]    #0x
                         _data_value = str_value
                    elif 'size' in _str:
                        # print 'size'
                         _local = _str.find('=')   
                         str_value = _str[_local+1:len(_str)-1]    #0x
                         _len_value = str_value
                    else:
                         pass
                  
                #print _addr_value , _data_value ,_len_value ,_cmd      #debug
            
                self.json_handle(_addr_value, _data_value,_len_value, _cmd ,'invaild')      
            
            else:
                 pass
                 #print "no write/read line"     #debug add
        fd.close()
 #   def scan_line_data(self):
    JsonPacket ='{"offset": "1","data": "2" ,"size" :"3" ,"cmd" : "read", "item" : "5"}'
    
    def json_handle(self,offset,data,size,cmd,item):
                
         template = {"offset": offset,"data": data ,"size" :size ,"cmd" : cmd, "item" : item}
         
        # print str(template)+ self.JsonPacket
         #print type(str(template))
   
         self.JsonPacket = self.JsonPacket + ','+ json.dumps(template)
         
                                                  
    #     list_t = json.loads(json.dumps(eval(handle_string),indent=32))  #json to list
    def record_number_cmd(self):
        list_t = list(eval(self.JsonPacket))  #json to list
       
        for index in range(len(list_t)):     #for index in range(len(list_t)):
            time = 0 
            if list_t[index]['item'] == 'invaild' :
                ###
                time = time + 1 
                for next in range(index+1,len(list_t)) :
                    if list_t[index]['cmd'] == list_t[next]['cmd'] and list_t[index]['offset'] == list_t[next]['offset']:
                            # print list_t[index]    #debug add
                             list_t[next]['item'] = 'vaild'
                             time = time +1
                     
                    else :
                        pass
                list_t[index]['item'] = str(time)
                
            else :
                pass 
            
       
        self.record_json_format_data = json.dumps (list_t,indent=32)    #after handle the source json format data,then put the record data to record_json_format_data
        

    def jsondata_to_file(self):     #put the json data to logjson.log file
         jsonfile = open('logjson.json','w')
         jsonfile.write(self.record_json_format_data)
         jsonfile.close()
         
    def _print(self):
        print("hello world")     
         

Loghandle = HandleLogClass() 

Loghandle.enter()

Loghandle.get_key_value()
Loghandle.record_number_cmd()
Loghandle.jsondata_to_file()

Loghandle.end()

sleep(2)




