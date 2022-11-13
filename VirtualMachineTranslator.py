class Parser:
    
    arithmetic_commands = {'add','sub','neg','eq','gt','lt','and','or','not'}
    special_commands={'C_PUSH','C_POP','C_FUNCTION','C_CALL','C_ARITHMETIC'}
    def __init__(self,filename): ## opens file for processing
        
        self.filename=open(filename,mode='r')
        self.tok_list=[]
        self.command_type=None
    
    def has_more_commands(self):
        original=self.filename.tell()
        curr= self.filename.readline()
        self.filename.seek(original)
        
        if(curr==''):
            return False
        elif(curr[-1]=='\n' or (curr.strip() !='')):
             return True
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
    memory_pointers={
        'stack':0,
        'local':1,
        'argument':2,
        'this':3,
        'that':4,
        'temp':5
    }
    operation_to_sign={
        'neg':'-',
        'not':'!',
        'add':'+',
        'sub':'-',
        'and':'&',
        'or':'|'
    }
    
    operations_comparisons={
        'eq':'JEQ',
        'lt':'JLT',
        'gt':'JGT'
    }
    
    two_operands={'add','sub','and','or','gt','lt','eq'} #Operators with 2 operands
    one_operand={'neg','not'} #Operator with one operand
    ##Generates assemebly code 
    def __init__(self,filename):
        self.filename= open(filename,mode='w')
        self.number=0
    
    def add_comment(self,arr):
        string_comment=f'   //{" ".join(arr)}\n'
        self.filename.write(string_comment)
        
        
        
    def write_arithmetic(self,command):
        self.add_comment(command)
        lower=command[0].lower()
        


        string_1='''@R0
A=M-1
'''
        string_op=string_3=''
        
        if(lower in CodeWriter.one_operand):
            string_2=f'M={CodeWriter.operation_to_sign[lower]}M'
        else:
            string_op='''A=A-1
D=M
A=A+1
'''         
            if(lower in CodeWriter.operation_to_sign and lower in CodeWriter.two_operands):
            
                string_2=f'''D=D{CodeWriter.operation_to_sign[lower]}M
A=A-1
M=D
'''  
            else:
                string_2= f'''D=D-M
A=A-1
M=D
D=A
@13
M=D
A=M
D=M

@write_1_{self.number}
D;{CodeWriter.operations_comparisons[lower]}

@13
A=M
M=0

@end_of_condition_{self.number}
0;JMP

(write_1_{self.number})
@13
A=M
M=-1

(end_of_condition_{self.number})
'''
                self.number+=1
                
            string_3= '''@R0
M=M-1
'''
        
        self.filename.write(string_1+string_op+string_2+string_3+'\n');
            
    
    
    def write_push_pop(self, arr):
        self.add_comment(arr)
        lower=arr[0].lower()
        
        if(arr[0].lower()=='pop'):
            self.write_pop(arr)
        else:
            self.write_push(arr)        
        
        
 
    def write_pop(self,arr):
        lower= arr[1].lower()
        string_non_static=''
        if(lower in CodeWriter.memory_pointers):
            string_non_static=f'''@{arr[2]}
D=A
@ {CodeWriter.memory_pointers[lower]}
D=D+{'A' if lower=='temp' else 'M'}
'''
        string_static=f'''@{self.filename.name.title()[:-3]+f'{arr[2]}'}
D=A
'''
        
        string_compulsory=f'''@R13
M=D
@ {CodeWriter.memory_pointers['stack']}
M=M-1
A=M
D=M
@R13
A=M
M=D
'''
        if(arr[1].lower()=='static'):
            self.filename.write(string_static)
        else:
            self.filename.write(string_non_static)
            
            
        self.filename.write(string_compulsory)
        
            
    
    def write_push(self,arr):
        lower= arr[1].lower()
        str_otherwise=''
        str_non_static=f'''@{arr[2]}
D=A
'''
        str_static= f'''@{self.filename.name.title()[:-3]+f'{arr[2]}' }
D=M
'''
        
        if(lower in CodeWriter.memory_pointers):

            str_otherwise=f'''@ {CodeWriter.memory_pointers[lower]}
A=D+{'A' if lower=='temp' else 'M'}
D=M
'''
        str_compulsory=f'''@{CodeWriter.memory_pointers['stack']}
M=M+1
A=M-1
M=D
'''
        if(arr[1].lower()=='static'):
            self.filename.write(str_static)
        else:
            self.filename.write(str_non_static)
            if(arr[1].lower()!='constant'):
                self.filename.write(str_otherwise)
        self.filename.write(str_compulsory)
        
    
    
    def close(self):
        
        string='''
    //END
(END)
@END
0;JMP
'''
        
        self.filename.write(string)
        self.filename.close()
        
        
        
        
        #VM Translatior
def VM_Translator(file_name):
    parser = Parser(file_name)
    codewriter= CodeWriter(f'C:\\Users\\Admin\\Downloads\\nand2tetris\\nand2tetris\\projects\\07\\StackArithmetic\\StackTest\\{file_name[:-2]}asm') 

    while (parser.has_more_commands()):
        lis=parser.tokenize()
        if(lis==[]):
            continue
        command = parser.get_command()
        if(command=='C_ARITHMETIC'):
            codewriter.write_arithmetic(lis)
        else:
            codewriter.write_push_pop(lis)

    codewriter.close()
    
    
    #Start of Execution
    VM_Translator('BasicTest.vm')    

    
