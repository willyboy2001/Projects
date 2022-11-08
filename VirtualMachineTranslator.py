class Parser:
    
    arithmetic_commands = {'add','sub','neg','eq','gt','lt','and','or','not'}
    special_commands={'C_PUSH','C_POP','C_FUNCTION','C_CALL'}
    def __init__(self,filename): ## opens file for processing
        
        self.filename=open(filename,mode='r')
        self.tok_list=[]
        self.command_type=None
    
    def has_more_commands(self):
        original=self.filename.tell()
        curr= self.filename.readline()
        self.filename.seek(original)
        
        if(curr==''):
            self.end_of_file=True
            return False
        elif(curr[-1]=='\n' or (curr.strip() !='')):
             return True
        self.end_of_file=True
        return False
    
    
    
    def advance(self):
        return self.filename.readline()
    
    
    
    def tokenize(self):
        lis= list(self.advance().split())
        length=len(lis)
        tok_list=[]
        
        for val in lis:
            if('//' in val):
                break
            tok_list.append(val)
        
        self.tok_list=tok_list
        
        return tok_list
        
    
    
    def get_command(self):
        length=len(self.tok_list)
        s=None
        
       
        if(self.tok_list[0].lower() in Parser.arithmetic_commands):
            s= 'C_ARITHMETIC'
        elif(self.tok_list[0].lower()=='push'):
            s= 'C_PUSH'
        elif(self.tok_list[0].lower()=='pop'):
            s= 'C_POP'
        else:
            pass
        
        self.command_type=s
        return s
    
    
    def arg1(self):
        if(self.command_type=='C_ARITHMETIC'):
            return self.tok_list[0]
        return self.tok_list[1]
    
    def arg2(self):
        if(len(self.tok_list)>1):
            return self.tok_list[2]
        
        
        
            
        
        
        
        
        

class CodeWriter:
    ##Generates assemebly code 
    def __init__(self,filename):
        self.filename= open(filename,mode='w')
        
    def write_arithmetic(self,command):
        string_comment=f'   //{command.upper()}\n'
        string_1='''@R0
A=M-1
'''
        string_op=string_3=''

        if(command.lower()=='not'):
            string_2='M=!M'
        elif(command.lower()=='neg'):
            string_2='M=-M'
        else:
            string_op='''A=A-1
D=M
A=A+1
'''            
            if(command.lower()=='add'):
                string_2='D=D+M'
            elif(command.lower()=='sub'):
                string_2='D=D-M'
            elif(command.lower()=='and'): 
                string_2='D=D&M'
            elif(command.lower()=='or'):
                string_2='D=D|M'
            elif(command.lower()=='sub'):
                string_2='D=D-M'     
            else:
                pass
        
            string_3= '''
A=A-1
M=D
@R0
M=M-1
'''
        
        self.filename.write(string_comment+string_1+string_op+string_2+string_3+'\n');
            
    
    
    
    
    def close(self):
        
        string='''
    //END
(END)
@END
0;JMP
'''
        
        self.filename.write(string)
        self.filename.close()

        
        
        
        
def VM_Translator(file_name):
    parser = Parser(file_name)
    codewriter= CodeWriter(file_name+'.asm') 

    while (parser.has_more_commands()):
        lis=parser.tokenize()
        if(lis==[]):
            continue
        command = parser.get_command()
        if(command=='C_ARITHMETIC'):
            codewriter.write_arithmetic(lis[0])

    codewriter.close()      
      
