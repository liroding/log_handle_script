#!/user/bin/python3
import os
import json
import new
import re
import string

from telnetlib import OLD_ENVIRON
from lib2to3.fixer_util import String

class HandleLogClass:
    
    ''' log name '''
    logname = "/debuglog.log"
   
            
    def enter(self):
        print '-- start handle log --'
    
    def end(self):
        print '-- handle ending --'
    
    def __init__(self):
        
        self.rootpath = os.path.dirname(os.path.realpath(__file__));
        self.logpath = self.rootpath + self.logname
        print 'The log path : %s' % (self.logpath)
 
   
    '''     
    def print_debug(self):
        print 'data = 0x%x   addr =0x%x ' % (self.data,self.addr) 
        print 'id(data) = 0x%x   id(addr) =0x%x ' % (id(self.data),id(self.addr)) 
    '''
    
    def txt_num_line(self):
        self.numline = sum(1 for line in open(self.logpath))
        print self.numline
       
    def show_line_data(self):
        fd = open(self.logpath,"rw+") 
        for line in fd.readlines():
            print line

        fd.close()
        
    def get_key_value(self):
        fd = open(self.logpath,"rw+")
        
        _addr_value = '';
        _data_value = ''; 
        _len_value = '';
        _cmd  = '';
        
        for line in fd.readlines():                      
            print line      #debug
            if 'Read' in line or 'Write' in line :
                 
                wxlist= re.split(r',',line)   #wxlist is list format data
            
                for index in range(len(wxlist)):
                    _str = wxlist[index]      #addr=0x111  
       
                    if 'offset' in _str:
                         print 'offset'
                         _local = _str.find('=')   
                         str_value = _str[_local+1:len(_str)]    #0x
                         _addr_value = str_value
                    
                         if 'Read' in _str:
                             _cmd = "read"
                         elif 'Write' in _str:
                             _cmd = "write" 
                    elif 'data' in _str:
                         print 'data'
                         _local = _str.find('=')   
                         str_value = _str[_local+1:len(_str)]    #0x
                         _data_value = str_value
                    elif 'size' in _str:
                         print 'size'
                         _local = _str.find('=')   
                         str_value = _str[_local+1:len(_str)-1]    #0x
                         _len_value = str_value
                    else:
                         pass
                  
                print _addr_value , _data_value ,_len_value ,_cmd
            
                self.json_handle(_addr_value, _data_value,_len_value, _cmd)      
            
            else:
                 print "no write/read line" 
        fd.close()
 #   def scan_line_data(self):
    JsonPacket = {'offset': '0' ,'data': '0', 'size' : '0' ,'cmd' : '0'}
    
    def json_handle(self,offset,data,size,cmd):
                
         template = {'offset': offset,'data': data ,'size' :size ,'cmd' : cmd}
   
         self.JsonPacket = self.JsonPacket ,template
                           
         handle_string = str( str(self.JsonPacket).replace('(','') ).replace(')','')   #dict to string
                        
         
         self.json_format_string = json.dumps(eval(handle_string),indent=32)   #eval(handle_string) [string to dict] 
         
    #     list_t = json.loads(json.dumps(eval(handle_string),indent=32))  #json to list
    def record_number_cmd(self,_jsonformatdata):
        print _jsonformatdata    # debug  out the json format string data
        
        list_t = json.loads(json.dumps(eval(_jsonformatdata),indent=32))  #json to list 
        
        print list_t        #debug out list data
        
        dict_t = list_t[1]
        
        print dict_t       #debug out dict data

        print dict_t['size']        
             
        

Loghandle = HandleLogClass() 

Loghandle.get_key_value()


Loghandle.record_number_cmd(Loghandle.json_format_string)

