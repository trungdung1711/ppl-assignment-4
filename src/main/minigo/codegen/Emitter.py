from Utils import *
# from StaticCheck import *
# from StaticError import *
# import CodeGenerator as cgen
from CodeGenError import IllegalOperandException
from MachineCode import JasminCode
from AST import *


# same concept of MType
class Method:
    def __init__(self, name, params, result, className = 'MiniGoClass'):
        self.name   = name
        self.params = params      # list of Type (from prof)
        self.result = result      # Type (from prof)
        self.className = className


    def invoke(self):
        return '/'.join([self.className, self.name])


class StaticMethod:
    def __init__(self, name, params, result, class_name):
        self.class_name = class_name
        self.name       = name
        self.params     = params      # list of Type (from prof)
        self.result     = result      # Type (from prof)

    
    def invoke(self):
        return '/'.join([self.class_name, self.name])


class Class:
    def __init__(self, name):
        self.name = name


class Interface:
    def __init__(self, name):
        self.name = name


class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

    # Can cause error in getJVMType
    # Mtype is in StaticCheck -> wrong
    # def __str__(self):
    #     return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"


# skip inheritence, because it is not quite important
class ClassType():
    def __init__(self, name):
        #value: Id
        self.name = name



class Emitter():
    def __init__(self, filename, class_name):
        self.class_name = class_name
        self.filename = filename
        self.buff = list()
        self.jvm = JasminCode()


    # This method can be changed
    # to define our Type
    # must change ArrayType
    # NOTE
    def getJVMType(self, inType):
        typeIn = type(inType)

        if typeIn is IntType:
            return "I"
        
        elif typeIn is FloatType:
            return 'F'
        
        elif typeIn is BoolType:
            return 'Z'
        
        elif typeIn is StringType:
            return "Ljava/lang/String;"
        
        elif typeIn is VoidType:
            return "V"
        
        # int[] is object which is different from int[][]
        elif type(inType) is ArrayType:
            # NOTE: must check the dimension
            # [5][4][2][5]
            return ''.join('[' for diemn in inType.dimens) + self.getJVMType(inType.eleType)
            # return "[" + self.getJVMType(inType.eleType)

        # semantic checking is done
        elif isinstance(inType, Id):
            return 'L' + inType.name + ';'
        
        # class and interface is the same in this case
        # but different when method call
        # one - invokeVirtual
        # one - invokeInterface
        # used to resolve to type in the [expression]
        # which is important in Var, Const
        # in the type descriptor -> L<class_name>; -> OK for that
        elif isinstance(inType, Class):
            return 'L' + inType.name + ';'
        
        elif isinstance(inType, Interface):
            return 'L' + inType.name + ';'
        
        # method descriptor
        elif isinstance(inType, Method):
            return '(' + ''.join(list(map(lambda par: self.getJVMType(par), inType.params))) + ')' + self.getJVMType(inType.result)
        

        elif isinstance(inType, StaticMethod):
            return '(' + ''.join(list(map(lambda par: self.getJVMType(par), inType.params))) + ')' + self.getJVMType(inType.result)

        
        elif typeIn is MType:
            return "(" + "".join(list(map(lambda x: self.getJVMType(x), inType.partype))) + ")" + self.getJVMType(inType.rettype)
        

        elif typeIn is ClassType:
            return "L" + inType.name + ";"
        
        else:
            return str(typeIn)


    def getFullType(inType):
        typeIn = type(inType)
        if typeIn is IntType:
            return "int"
        elif typeIn is StringType:
            return "java/lang/String"
        elif typeIn is VoidType:
            return "void"


    def emitPUSHICONST(self, in_, frame):
        #in: Int or Sring
        #frame: Frame
        
        frame.push();
        if type(in_) is int:
            i = in_
            if i >= -1 and i <=5:
                return self.jvm.emitICONST(i)
            
            elif i >= -128 and i <= 127:
                return self.jvm.emitBIPUSH(i)
            
            elif i >= -32768 and i <= 32767:
                return self.jvm.emitSIPUSH(i)
            
            else:
                return self.jvm.emitLDC(str(i))

        elif type(in_) is str:
            if in_ == "true":
                return self.emitPUSHICONST(1, frame)
            elif in_ == "false":
                return self.emitPUSHICONST(0, frame)
            else:
                return self.emitPUSHICONST(int(in_), frame)

    def emitPUSHFCONST(self, in_, frame):
        #in_: String
        #frame: Frame
        
        f = float(in_)
        frame.push()
        rst = "{0:.4f}".format(f)
        if rst == "0.0" or rst == "1.0" or rst == "2.0":
            return self.jvm.emitFCONST(rst)
        else:
            return self.jvm.emitLDC(in_)           

    ''' 
    *    generate code to push a constant onto the operand stack.
    *    @param in the lexeme of the constant
    *    @param typ the type of the constant
    '''
    def emitPUSHCONST(self, in_, typ, frame):
        #in_: String
        #typ: Type
        #frame: Frame
        
        if type(typ) is IntType:
            return self.emitPUSHICONST(in_, frame)

        elif type(typ) is StringType:
            frame.push()
            return self.jvm.emitLDC(in_)

        else:
            raise IllegalOperandException(in_)

    ##############################################################

    def emitALOAD(self, in_, frame):
        #in_: Type
        #frame: Frame
        #..., arrayref, index, value -> ...
        
        frame.pop()
        if type(in_) is IntType:
            return self.jvm.emitIALOAD()
        elif type(in_) is ArrayType or type(in_) is ClassType or type(in_) is StringType:
            return self.jvm.emitAALOAD()
        else:
            raise IllegalOperandException(str(in_))

    def emitASTORE(self, in_, frame):
        #in_: Type
        #frame: Frame
        #..., arrayref, index, value -> ...
        
        frame.pop()
        frame.pop()
        frame.pop()
        if type(in_) is IntType:
            return self.jvm.emitIASTORE()
        elif type(in_) is ArrayType or type(in_) is ClassType or type(in_) is StringType:
            return self.jvm.emitAASTORE()
        else:
            raise IllegalOperandException(str(in_))

    '''    generate the var directive for a local variable.
    *   @param in the index of the local variable.
    *   @param varName the name of the local variable.
    *   @param inType the type of the local variable.
    *   @param fromLabel the starting label of the scope where the variable is active.
    *   @param toLabel the ending label  of the scope where the variable is active.
    '''
    def emitVAR(self, in_, varName, inType, fromLabel, toLabel, frame):
        #in_: Int
        #varName: String
        #inType: Type
        #fromLabel: Int
        #toLabel: Int
        #frame: Frame
        
        return self.jvm.emitVAR(in_, varName, self.getJVMType(inType), fromLabel, toLabel)


    # Must add more cases
    # Using the Operand stack + Local variable array of JVM
    def emitREADVAR(self, name, inType, index, frame):
        #name: String
        #inType: Type
        #index: Int
        #frame: Frame
        #... -> ..., value
        
        frame.push()
        if type(inType) is IntType:
            return self.jvm.emitILOAD(index)
        
        elif type(inType) is BoolType:
            return self.jvm.emitILOAD(index)
        
        elif isinstance(inType, FloatType):
            return self.jvm.emitFLOAD(index)
        
        elif isinstance(IntType, StringType):
            return self.jvm.emitALOAD(index)

        elif isinstance(inType, (Class, Interface)):
            return self.jvm.emitALOAD(index)
        
        # must handle different cases of Id
        # if it is static -> get static
        elif isinstance(inType, Id):
            # then this is the object [JVM stores it in heap]
            # we would use reference to work with it
            # using aload
            return self.jvm.emitALOAD(index)

        # ArrayType is considered to be object
        elif type(inType) is ArrayType or type(inType) is ClassType or type(inType) is StringType:
            return self.jvm.emitALOAD(index)
        
        else:
            raise IllegalOperandException(name)

    ''' generate the second instruction for array cell access
    *
    '''
    def emitREADVAR2(self, name, typ, frame):
        #name: String
        #typ: Type
        #frame: Frame
        #... -> ..., value

        #frame.push()
        raise IllegalOperandException(name)

    '''
    *   generate code to pop a value on top of the operand stack and store it to a block-scoped variable.
    *   @param name the symbol entry of the variable.
    '''
    def emitWRITEVAR(self, name, inType, index, frame):
        #name: String
        #inType: Type
        #index: Int
        #frame: Frame
        #..., value -> ...
        
        frame.pop()

        if type(inType) is IntType:
            return self.jvm.emitISTORE(index)
        
        elif isinstance(inType, FloatType):
            return self.jvm.emitFSTORE(index)
        
        elif isinstance(inType, BoolType):
            return self.jvm.emitISTORE(index)
        
        elif isinstance(inType, (Class, Interface)):
            return self.jvm.emitASTORE(index)
        
        elif isinstance(inType, Class):
            return self.jvm.emitASTORE(index)
        
        elif type(inType) is ArrayType or type(inType) is ClassType or type(inType) is StringType:
            return self.jvm.emitASTORE(index)
        
        else:
            raise IllegalOperandException(name)

    ''' generate the second instruction for array cell access
    *
    '''
    def emitWRITEVAR2(self, name, typ, frame):
        #name: String
        #typ: Type
        #frame: Frame
        #..., value -> ...

        #frame.push()
        raise IllegalOperandException(name)

    ''' generate the field (static) directive for a class mutable or immutable attribute.
    *   @param lexeme the name of the attribute.
    *   @param in the type of the attribute.
    *   @param isFinal true in case of constant; false otherwise
    '''
    def emitATTRIBUTE(self, lexeme, in_, isStatic, isFinal, value):
        #lexeme: String
        #in_: Type
        #isFinal: Boolean
        #value: String
        if isStatic:
            return self.jvm.emitSTATICFIELD(lexeme, self.getJVMType(in_), isFinal, value)
        else:
            return self.jvm.emitFIELD(lexeme, self.getJVMType(in_), isFinal, value)

    def emitGETSTATIC(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame

        frame.push()
        return self.jvm.emitGETSTATIC(lexeme, self.getJVMType(in_))

    def emitPUTSTATIC(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame
        
        frame.pop()
        return self.jvm.emitPUTSTATIC(lexeme, self.getJVMType(in_))

    def emitGETFIELD(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame

        return self.jvm.emitGETFIELD(lexeme, self.getJVMType(in_))

    def emitPUTFIELD(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame

        frame.pop()
        frame.pop()
        return self.jvm.emitPUTFIELD(lexeme, self.getJVMType(in_))

    ''' generate code to invoke a static method
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name)
    *   @param in the type descriptor of the method.
    '''
    def emitINVOKESTATIC(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame

        typ = in_
        list(map(lambda x: frame.pop(), typ.params))
        if not type(typ.result) is VoidType:
            frame.push()
        return self.jvm.emitINVOKESTATIC(lexeme, self.getJVMType(in_))

    ''' generate code to invoke a special method
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name)
    *   @param in the type descriptor of the method.
    '''
    def emitINVOKESPECIAL(self, frame, lexeme=None, in_=None):
        #lexeme: String
        #in_: Type
        #frame: Frame

        if not lexeme is None and not in_ is None:
            typ = in_
            list(map(lambda x: frame.pop(), typ.partype))
            frame.pop()
            if not type(typ.rettype) is VoidType:
                frame.push()
            return self.jvm.emitINVOKESPECIAL(lexeme, self.getJVMType(in_))
        elif lexeme is None and in_ is None:
            frame.pop()
            return self.jvm.emitINVOKESPECIAL()

    ''' generate code to invoke a virtual method
    * @param lexeme the qualified name of the method(i.e., class-name/method-name)
    * @param in the type descriptor of the method.
    '''
    def emitINVOKEVIRTUAL(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame

        # params of Method same MType

        typ = in_
        # pop arguments
        # pop object
        list(map(lambda x: frame.pop(), typ.params))
        frame.pop()
        if not type(typ.result) is VoidType:
            # return value
            frame.push()
        return self.jvm.emitINVOKEVIRTUAL(lexeme, self.getJVMType(in_))
    

    def emit_invoke_interface(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame

        # params of Method same MType

        typ = in_
        number = 1
        for param in typ.params:
            number += 1
        # pop arguments
        # pop object
        list(map(lambda x: frame.pop(), typ.params))
        frame.pop()
        if not type(typ.result) is VoidType:
            # return value
            frame.push()
        return self.jvm.emitINVOKEINTERFACE(lexeme, self.getJVMType(in_), number)

    '''
    *   generate ineg, fneg.
    *   @param in the type of the operands.
    '''
    def emitNEGOP(self, in_, frame):
        #in_: Type
        #frame: Frame
        #..., value -> ..., result

        if type(in_) is IntType:
            return self.jvm.emitINEG()
        else:
            return self.jvm.emitFNEG()

    def emitNOT(self, in_, frame):
        #in_: Type
        #frame: Frame

        label1 = frame.getNewLabel()
        label2 = frame.getNewLabel()
        result = list()
        result.append(emitIFTRUE(label1, frame))
        result.append(emitPUSHCONST("true", in_, frame))
        result.append(emitGOTO(label2, frame))
        result.append(emitLABEL(label1, frame))
        result.append(emitPUSHCONST("false", in_, frame))
        result.append(emitLABEL(label2, frame))
        return ''.join(result)

    '''
    *   generate iadd, isub, fadd or fsub.
    *   @param lexeme the lexeme of the operator.
    *   @param in the type of the operands.
    '''
    def emitADDOP(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame
        #..., value1, value2 -> ..., result

        frame.pop()
        if lexeme == "+":
            if type(in_) is IntType:
                return self.jvm.emitIADD()
            else:
                return self.jvm.emitFADD()
        else:
            if type(in_) is IntType:
                return self.jvm.emitISUB()
            else:
                return self.jvm.emitFSUB()

    '''
    *   generate imul, idiv, fmul or fdiv.
    *   @param lexeme the lexeme of the operator.
    *   @param in the type of the operands.
    '''

    def emitMULOP(self, lexeme, in_, frame):
        #lexeme: String
        #in_: Type
        #frame: Frame
        #..., value1, value2 -> ..., result

        frame.pop()
        if lexeme == "*":
            if type(in_) is IntType:
                return self.jvm.emitIMUL()
            else:
                return self.jvm.emitFMUL()
        else:
            if type(in_) is IntType:
                return self.jvm.emitIDIV()
            else:
                return self.jvm.emitFDIV()

    def emitDIV(self, frame):
        #frame: Frame

        frame.pop()
        return self.jvm.emitIDIV()

    def emitMOD(self, frame):
        #frame: Frame

        frame.pop()
        return self.jvm.emitIREM()

    '''
    *   generate iand
    '''

    def emitANDOP(self, frame):
        #frame: Frame

        frame.pop()
        frame.pop()
        frame.push()
        return self.jvm.emitIAND()

    '''
    *   generate ior
    '''
    def emitOROP(self, frame):
        #frame: Frame

        frame.pop()
        frame.pop()
        frame.push()
        return self.jvm.emitIOR()

    def emitREOP(self, op, in_, frame):
        #op: String
        #in_: Type
        #frame: Frame
        #..., value1, value2 -> ..., result

        result = list()
        labelF = frame.getNewLabel()
        labelO = frame.getNewLabel()

        frame.pop()
        frame.pop()
        if op == ">":
            result.append(self.jvm.emitIFICMPLE(labelF))
        elif op == ">=":
            result.append(self.jvm.emitIFICMPLT(labelF))
        elif op == "<":
            result.append(self.jvm.emitIFICMPGE(labelF))
        elif op == "<=":
            result.append(self.jvm.emitIFICMPGT(labelF))
        elif op == "!=":
            result.append(self.jvm.emitIFICMPEQ(labelF))
        elif op == "==":
            result.append(self.jvm.emitIFICMPNE(labelF))
        result.append(self.emitPUSHCONST("1", IntType(), frame))
        frame.pop()
        result.append(self.emitGOTO(labelO, frame))
        result.append(self.emitLABEL(labelF, frame))
        result.append(self.emitPUSHCONST("0", IntType(), frame))
        result.append(self.emitLABEL(labelO, frame))
        return ''.join(result)

    def emitRELOP(self, op, in_, trueLabel, falseLabel, frame):
        #op: String
        #in_: Type
        #trueLabel: Int
        #falseLabel: Int
        #frame: Frame
        #..., value1, value2 -> ..., result

        result = list()

        frame.pop()
        frame.pop()
        if op == ">":
            result.append(self.jvm.emitIFICMPLE(falseLabel))
            result.append(self.emitGOTO(trueLabel))
        elif op == ">=":
            result.append(self.jvm.emitIFICMPLT(falseLabel))
        elif op == "<":
            result.append(self.jvm.emitIFICMPGE(falseLabel))
        elif op == "<=":
            result.append(self.jvm.emitIFICMPGT(falseLabel))
        elif op == "!=":
            result.append(self.jvm.emitIFICMPEQ(falseLabel))
        elif op == "==":
            result.append(self.jvm.emitIFICMPNE(falseLabel))
        result.append(self.jvm.emitGOTO(trueLabel))
        return ''.join(result)

    '''   generate the method directive for a function.
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name).
    *   @param in the type descriptor of the method.
    *   @param isStatic <code>true</code> if the method is static; <code>false</code> otherwise.
    '''

    def emitMETHOD(self, lexeme, in_, isStatic, frame):
        #lexeme: String
        #in_: Type (defined by my professor, but can be changed)
        #isStatic: Boolean
        #frame: Frame

        return self.jvm.emitMETHOD(lexeme, self.getJVMType(in_), isStatic)

    '''   generate the end directive for a function.
    '''
    def emitENDMETHOD(self, frame):
        #frame: Frame

        buffer = list()
        buffer.append(self.jvm.emitLIMITSTACK(frame.getMaxOpStackSize()))
        buffer.append(self.jvm.emitLIMITLOCAL(frame.getMaxIndex()))
        buffer.append(self.jvm.emitENDMETHOD())
        return ''.join(buffer)

    def getConst(self, ast):
        #ast: Literal
        if type(ast) is IntLiteral:
            return (str(ast.value), IntType())

    '''   generate code to initialize a local array variable.<p>
    *   @param index the index of the local variable.
    *   @param in the type of the local array variable.
    '''

    '''   generate code to initialize local array variables.
    *   @param in the list of symbol entries corresponding to local array variable.    
    '''

    '''   generate code to jump to label if the value on top of operand stack is true.<p>
    *   ifgt label
    *   @param label the label where the execution continues if the value on top of stack is true.
    '''
    def emitIFTRUE(self, label, frame):
        #label: Int
        #frame: Frame

        frame.pop()
        return self.jvm.emitIFGT(label)

    '''
    *   generate code to jump to label if the value on top of operand stack is false.<p>
    *   ifle label
    *   @param label the label where the execution continues if the value on top of stack is false.
    '''
    def emitIFFALSE(self, label, frame):
        #label: Int
        #frame: Frame

        frame.pop()
        return self.jvm.emitIFLE(label)

    def emitIFICMPGT(self, label, frame):
        #label: Int
        #frame: Frame

        frame.pop()
        return self.jvm.emitIFICMPGT(label)

    def emitIFICMPLT(self, label, frame):
        #label: Int
        #frame: Frame

        frame.pop()
        return self.jvm.emitIFICMPLT(label)    

    '''   generate code to duplicate the value on the top of the operand stack.<p>
    *   Stack:<p>
    *   Before: ...,value1<p>
    *   After:  ...,value1,value1<p>
    '''
    def emitDUP(self, frame):
        #frame: Frame

        frame.push()
        return self.jvm.emitDUP()

    def emitPOP(self, frame):
        #frame: Frame

        frame.pop()
        return self.jvm.emitPOP()

    '''   generate code to exchange an integer on top of stack to a floating-point number.
    '''
    def emitI2F(self, frame):
        #frame: Frame

        return self.jvm.emitI2F()

    ''' generate code to return.
    *   <ul>
    *   <li>ireturn if the type is IntegerType or BooleanType
    *   <li>freturn if the type is RealType
    *   <li>return if the type is null
    *   </ul>
    *   @param in the type of the returned expression.
    '''


    # NOTE: must add more cases about return
    def emitRETURN(self, in_, frame):
        #in_: Type
        #frame: Frame

        if type(in_) is IntType:
            frame.pop()
            return self.jvm.emitIRETURN()

        elif isinstance(in_, BoolType):
            frame.pop()
            return self.jvm.emitIRETURN()

        elif isinstance(in_, FloatType):
            frame.pop()
            return self.jvm.emitFRETURN()

        elif isinstance(in_, StringType):
            frame.pop()
            return self.jvm.emitARETURN()

        elif isinstance(in_, ArrayType):
            frame.pop()
            return self.jvm.emitARETURN()

        elif isinstance(in_, Class):
            frame.pop()
            return self.jvm.emitARETURN()

        elif isinstance(in_, Interface):
            frame.pop()
            return self.jvm.emitARETURN()

        elif type(in_) is VoidType:
            return self.jvm.emitRETURN()

    ''' generate code that represents a label	
    *   @param label the label
    *   @return code Label<label>:
    '''
    def emitLABEL(self, label, frame):
        #label: Int
        #frame: Frame

        return self.jvm.emitLABEL(label)

    ''' generate code to jump to a label	
    *   @param label the label
    *   @return code goto Label<label>
    '''
    def emitGOTO(self, label, frame):
        #label: Int
        #frame: Frame

        return self.jvm.emitGOTO(label)

    ''' generate some starting directives for a class.<p>
    *   .source MPC.CLASSNAME.java<p>
    *   .class public MPC.CLASSNAME<p>
    *   .super java/lang/Object<p>
    '''
    def emitPROLOG(self, name, parent):
        #name: String
        #parent: String

        result = list()
        result.append(self.jvm.emitSOURCE(name + ".java"))
        result.append(self.jvm.emitCLASS("public " + name))
        result.append(self.jvm.emitSUPER("java/land/Object" if parent == "" else parent))
        return ''.join(result)

    def emitLIMITSTACK(self, num):
        #num: Int

        return self.jvm.emitLIMITSTACK(num)

    def emitLIMITLOCAL(self, num):
        #num: Int

        return self.jvm.emitLIMITLOCAL(num)

    def emitEPILOG(self):
        file = open(self.filename, "w")
        file.write(''.join(self.buff))
        file.close()

    ''' print out the code to screen
    *   @param in the code to be printed out
    '''
    def printout(self, in_):
        #in_: String

        self.buff.append(in_)

    def clearBuff(self):
        self.buff.clear()


    # my utils
    '''
    - same function as printout
    - just buffering the code
    - use emitEPILOG to write the whole buffer to file
    '''
    def buffer(self, in_):
        #in_: String

        self.buff.append(in_)


    def get_jvm(self) -> JasminCode:
        return self.jvm
    

    def emit_class_declaration(self):
        code = list()
        code.append(self.jvm.emitSOURCE(self.class_name + '.java'))
        code.append(self.jvm.emitCLASS('public ' + self.class_name))
        code.append(self.jvm.emitSUPER('/'.join(['java', 'lang', 'Object'])))        
        return ''.join(code)


    def emit_field(self, name, typ):
        td = self.getJVMType(typ)
        return self.jvm.emitINSTANCEFIELD(name, td, False, None)


    # will be called later for interface checking
    def emit_class_implements(self, interfaces : list[str]):
        code = [self.jvm.emitIMPLEMENTS(interface) for interface in interfaces]
        code.append(
            self.emit_line(1)
        )
        return ''.join(code)


    def emit_interface_declaration(self):
        code = list()
        code.append(self.jvm.emitSOURCE(self.class_name + '.java'))
        code.append(self.jvm.emitINTERFACE(self.class_name))
        code.append(self.jvm.emitSUPER('/'.join(['java', 'lang', 'Object'])))
        return ''.join(code)
    

    def emit_abstract_method(self, name : str, signature : MType):
        code = list()
        meth_signature = self.getJVMType(signature)
        code.append(
            self.jvm.emitMETHOD(
                name,
                meth_signature,
                False,
                True
            )
        )

        code.append(
            self.jvm.emitENDMETHOD()
        )

        return ''.join(code)
    

    def emit_line(self, number : int):
        code = [self.jvm.END for i in range(number)]
        return ''.join(code)
    

    def emitDEFAULTINIT(self, name, frame):
        frame.pop()
        typ = Method('<init>', [], VoidType(), name)
        type_descriptor = self.getJVMType(typ)
        return self.jvm.emitINVOKESPECIAL(typ.invoke(), type_descriptor)
    

    def emitNEW(self, name, frame):
        # ... -> ... ref
        frame.push()
        return self.jvm.emitNEW(name)
    

    # abstraction
    def emitSTRINGADD(self, frame, codeX, codeY):
        # ...str, str -> str
        
        # 1. must create the StringBuilder
        code = list()
        code.append(
            self.emitNEW('java/lang/StringBuilder', frame)
        )

        # 2. dupplicate that ref
        code.append(
            self.emitDUP(frame)
        )

        code.append(
            self.emitDEFAULTINIT('java/lang/StringBuilder', frame)
        )

        # code to calculate string X
        code.append(
            codeX
        )

        # call append
        append = Method('append', [Class('java/lang/String')], Class('java/lang/StringBuilder'), 'java/lang/StringBuilder')
        code.append(
            self.emitINVOKEVIRTUAL(append.invoke(), append, frame)
        )

        # generate code for Y
        code.append(
            codeY
        )

        # call append one more time, take 2 return 1
        code.append(
            self.emitINVOKEVIRTUAL(append.invoke(), append, frame)
        )

        # call to string and return
        toString = Method('toString', [], Class('java/lang/String'), 'java/lang/StringBuilder')
        code.append(
            self.emitINVOKEVIRTUAL(toString.invoke(), toString, frame)
        )

        # now the result is in the operand stack
        return ''.join(code)
    

    def emitNULL(self, frame):
        frame.push()
        return self.jvm.INDENT + 'aconst_null' + self.jvm.END