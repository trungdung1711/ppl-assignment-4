# 2210573
'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from Utils import *
# from StaticCheck import *
# 5/2/2025
# instead of StaticCheck
from Visitor import *
# from Utils import Utils
from AST import *

# from StaticError import *
from Emitter import Emitter, MType, ClassType
from Frame import Frame
from abc import ABC, abstractmethod
from functools import reduce


####################################################
# @idea from: https://github.com/huynhtuandat05december/CSE-PPL

# I am tired to implement a new data structure
# for this assignment because the framework is tightly
# coupled with the [Frame, Emitter]
# thus we would rely on this whole framework
# of the teacher to save the time, and note that
# This is not the intermediate code generation
# we are just generate the assembly-like java byte
# code, in the real compiler, the intermediate code
# is an internal representation used for optimization
# and code generation for the back-end,
# intermediate code allows us to have different
# front-end, but same back-end - a bridge between
# front-end and back-end - 5/2/2025
####################################################
class Val(ABC):
    pass


class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value


class CName(Val):
    def __init__(self, value,isStatic=True):
        #value: String
        self.isStatic = isStatic
        self.value = value


####################################################
# ADDED CLASS
# Exist in StaticCheck?

####################################################
# In the case of Go (help to prevent semantic meaning):
# Object (named thing):
# - Var
# - Const
# - TypeName    - no need (global)
# - Func        - no need (global)
####################################################
class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name        # name of this
        self.mtype = mtype      # type of Var or Const
        self.value = value      # index or CName

    # def __str__(self):
    #     return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"


class SubBody():
    def __init__(self, frame, sym):
        self.frame = frame
        self.sym = sym


class Access():
    def __init__(self, frame, sym, isLeft, isFirst=False):
        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst
####################################################


####################################################
# 
####################################################
class FirstPass(BaseVisitor):
    def __init__(self, ast, directory):
        self.ast                = ast
        self.directory          = directory
        self.class_emitters     = dict()
        # self.interface_emitters = dict()


    def go(self):
        self.visit(self.ast, None)
        return self.class_emitters


    def visitProgram(self, ast, o):
        [self.visit(decl, o) for decl in ast.decl]


    def visitStructType(self, ast, o):
        # create a new emitter for this struct
        name = ast.name
        emitter = Emitter(self.directory + '/' + name + '.j', name)
        self.class_emitters[name] = emitter


    def visitInterfaceType(self, ast, o):
        # create a new emitter for this interface
        name = ast.name
        emitter = Emitter(self.directory + '/' + name + '.j', name)
        self.class_emitters[name] = emitter


    def visitMethodDecl(self, ast, o):
        pass


    def visitFuncDecl(self, ast, o):
        pass


    def visitVarDecl(self, ast, o):
        pass


    def visitConstDecl(self, ast, o):
        pass


class SecondPass(BaseVisitor):
    class Method:
        def __init__(self, name, params, result):
            self.name   = name
            self.params = params      # list of Type (from prof)
            self.result = result      # Type (from prof)


    @staticmethod
    def identical(t1, t2) -> bool:
        # based on the type of ast
        if (t1 is t2):
            return True
        
        if (type(t1) is not type(t2)):
            return False
        
        # same type
        elif isinstance(t1, IntType) and isinstance(t2, IntType):
            return True
        
        elif isinstance(t1, FloatType) and isinstance(t2, FloatType):
            return True
        
        elif isinstance(t1, BoolType) and isinstance(t2, BoolType):
            return True
        
        elif isinstance(t1, StringType) and isinstance(t2, StringType):
            return True
        
        elif isinstance(t1, VoidType) and isinstance(t2, VoidType):
            return True
        
        elif isinstance(t1, ArrayType) and isinstance(t2, ArrayType):
            # NOTE: assume that it is always IntLiteral
            # but if it not IntLiteral -> Const
            # in the case of Const, then to bypass
            # we can check for the dimention, if it is same dimention
            # implement -> the interface (different value -> not the case)
            # -> semantic checking prevent it, no assignment like that
            # and implements that is totally OK (all), might be others will prevent
            # that -> only checking for the dimention
            if not SecondPass.identical(t1.eleType, t2.eleType):
                return False
            if len(t1.dimens) != len(t2.dimens):
                return False
            # NOTE: don't check for the size, because
            # in java int[] and int[][] are all objects
            return True
        
        elif isinstance(t1, Id) and isinstance(t2, Id):
            return t1.name == t2.name
        
        # dead code
        elif isinstance(t1, SecondPass.Struct) and isinstance(t2, SecondPass.Struct):
            # same name means same type
            return t1.name == t2.name
        
        elif isinstance(t1, SecondPass.Interface) and isinstance(t2, SecondPass.Interface):
            # same name means same type
            return t1.name == t2.name
        
        return False


    class Struct:
        def __init__(self, name):
            self.name = name


    class Interface:
        def __init__(self, name):
            self.name = name



    @staticmethod
    def same_signature(m1, m2) -> bool:

        if type(m1) != type(m2):
            return False
        
        elif (not isinstance(m1, SecondPass.Method) or not isinstance(m2, SecondPass.Method)):
            return False
        
        elif len(m1.params) != len(m2.params):
            return False
        
        elif type(m1.result) != type(m2.result):
            return False

        # same len of param, same return, check for param
        else:
            return all(SecondPass.identical(t1, t2) for t1, t2 in zip(m1.params, m2.params))


    def __init__(self, ast):
        self.ast         = ast
        self.structs     = dict()    # name - list[methods]
        self.interfaces  = dict()    # name - list[methods]

        self.result      = dict()    # name - list[names]


    def go(self):
        self.visit(self.ast, None)
        self.check()
        return self.result
    

    # for debugging
    def debug_print_result(self):
        for struct, interfaces in self.result.items():
            if interfaces:
                joined = ", ".join(interfaces)
                print(f"{struct}: {joined}")
            else:
                print(f"{struct}: (no interfaces)")


    def check(self):
        # check which structs implement
        # which interfaces -> note, used for
        # emitter of struct
        # for each of the structs
        # for each of the interfaces
        # check that whether it implements any interface
        # will be run after collecting all methods of structs
        # and interfaces

        for struct, smethods in self.structs.items():
            for interface, imethods in self.interfaces.items():
                # debug
                # print(f'{struct} is being checked with {interface}')
                if SecondPass.a_implements_b(smethods, imethods):
                    self.result[struct].add(interface)


    @staticmethod
    def a_implements_b(Amethods, Bmethods) -> bool:
        """check whether struct A implements interface B or not

        Args:
            Amethods (list): list of methods of struct A
            Bmethods (list): list of methods of interface B

        Returns:
            bool: True if Bmethods is a subset of Amethods
        """
        # checking whether methods in B are subset of A
        # if not -> false
        Aname_set = set([method.name for method in Amethods])
        Bname_set = set([method.name for method in Bmethods])
        # debug
        # print(f'Methods of struct {Aname_set} and Methods of interface {Bname_set}')
        if not Bname_set.issubset(Aname_set):
            return False
        
        # true about subset
        # check the signature
        # loop through the interface's method
        # and check for the struct methods
        # def method_check(acc, cur):
        #     method = next(filter(lambda method: method.name == cur.name, Amethods), None)
        #     # checking the signature of both methods
        #     acc.append(SecondPass.same_signature(cur, method))
        #     return acc
        # return all(reduce(method_check, Bmethods, []))
    
        return all(
            SecondPass.same_signature(method, next(filter(lambda x : x.name == method.name, Amethods), None))
            for method in Bmethods
        )


    def visitProgram(self, ast, o):
        [self.visit(decl, None) for decl in ast.decl]


    def visitStructType(self, ast, o):
        # init the list for each structs
        self.result[ast.name] = set()


    def visitMethodDecl(self, ast, o):
        class_name = ast.recType.name
        if class_name not in self.structs:
            # first time
            self.structs[class_name] = []
        # contain the key
        # 1. create the method
        # 2. append to to the list Method
        self.structs[class_name].append(self.visit(ast.fun, None))


    def visitFuncDecl(self, ast, o):
        param_types = [self.visit(param, None) for param in ast.params]
        return SecondPass.Method(ast.name, param_types, ast.retType)


    def visitParamDecl(self, ast, o):
        return ast.parType


    def visitInterfaceType(self, ast, o):
        # 1. visit this node
        # we would know all the methods of this interface
        # 2. just allocate the list immediately
        # 3. visit each of the prototype to get the method
        # print(f'Visit interface {ast.name}')
        method_lists = [self.visit(method, None) for method in ast.methods]
        self.interfaces[ast.name] = method_lists


    def visitPrototype(self, ast, o):
        return SecondPass.Method(ast.name, ast.params, ast.retType)


    def visitVarDecl(self, ast, o):
        pass


    def visitConstDecl(self, ast, o):
        pass


INTTYPE     = IntType()
FLOATTYPE   = FloatType()
BOOLTYPE    = BoolType()
STRTYPE     = StringType()
VOID        = VoidType()
ID          = Id


class ThirdPass(BaseVisitor):
    def __init__(self, ast, class_emitters, structs_interfaces):
        self.ast                = ast
        self.class_emitters     = class_emitters
        self.structs_interfaces = structs_interfaces


    def get_emitter(self, name : str) -> Emitter:
        return self.class_emitters[name]


    @staticmethod
    def buffer_init(emitter : Emitter):
        # NOTE: nothing to do with return type of Frame
        frame = Frame('<init>', VOID)
        method_type = MType([], VOID)
        emitter.buffer(emitter.emitMETHOD('<init>', method_type, False, frame))
        # scope of this method
        frame.enterScope(True)

        # NOTE: JVM will automatically push <this> for us
        # frame simulates the operand stack
        this_index = frame.getNewIndex()
        this_type  = Id(emitter.class_name)
        # .var is used for debugging
        emitter.buffer(emitter.emitVAR(
            this_index, 
            'this', 
            this_type, 
            frame.getStartLabel(), 
            frame.getEndLabel(), 
            frame))
        
        # put label, for other methods, functions
        # scope are different
        # NOTE
        emitter.buffer(
            emitter.emitLABEL(frame.getStartLabel(), frame)
        )
        # read this from local variable array
        emitter.buffer(
            emitter.emitREADVAR(
                'this',
                this_type,
                0,
                frame
            )
        )
        # invoke the <int>
        emitter.buffer(
            emitter.emitINVOKESPECIAL(
                frame
            )
        )

        emitter.buffer(
            emitter.emitLABEL(
                frame.getEndLabel(), frame
            )
        )

        emitter.buffer(
            emitter.emitRETURN(
                VOID, frame
            )
        )

        # end of the method
        emitter.buffer(
            emitter.emitENDMETHOD(
                frame
            )
        )

        frame.exitScope()


    def go(self):
        self.visit(self.ast, self.class_emitters)


    # for debugging, write the structs
    # with no methods, for checking,
    # also skip the .implement directive
    def debug_write(self):
        [e.emitEPILOG() for e in self.class_emitters.values()]


    def visitProgram(self, ast, o):
        [self.visit(decl, o) for decl in ast.decl]


    def visitStructType(self, ast, o):
        # emit

        # NOTE: current skip .implements
        # to be able to put the field first
        # .class public <name>
        # .super java/lang/Object
        # .implements <name> <name>

        # .field public <name> <type>
        emitter = self.get_emitter(ast.name)
        interfaces = self.structs_interfaces[ast.name]

        # 1. generate the class declaration part
        code = list()
        code.append(
            emitter.emit_class_declaration()
        )

        code.append(
            emitter.emit_line(1)
        )

        # 2. generate the .implements part
        # NOT for debugging
        # code.append(
        #     emitter.emit_class_implements(interfaces)
        # )

        # 3. generate the .field part
        # NOTE: all fields are all public
        fields = [emitter.emit_field(name, typ) for name, typ in ast.elements]
        code.extend(fields)
        code.append(
            emitter.emit_line(1)
        )

        # 4. generate the <init> method if the dev
        # doesn't give one
        # ThirdPass.buffer_init(emitter)


        emitter.buffer(
            ''.join(code)
        )

        ThirdPass.buffer_init(emitter)


    def visitInterfaceType(self, ast, o):
        # emit
        # .interface public abstract <name>
        # .super java/lang/Object

        # .method public abstract <name>()<type>;
        emitter = self.get_emitter(ast.name)
        code = list()

        # emit the declaration
        code.append(
            emitter.emit_interface_declaration()
        )

        method_code = [self.visit(method, emitter) for method in ast.methods]
        emitter.buffer(
            ''.join(code + method_code)
        )

        # write interface
        # emitter.emitEPILOG()


    def visitPrototype(self, ast, o):
        """.method public abstract <name>()V;
           .emd method


        Args:
            ast (_type_): _description_
            o (_type_): _description_

        Returns:
            _type_: _description_
        """
        emitter : Emitter = o
        code = list()
        code.append(
            emitter.emit_line(1)
        )

        signature = MType(ast.params, ast.retType)
        code.append(
            emitter.emit_abstract_method(ast.name, signature)
        )

        return ''.join(code)
    

    def visitVarDecl(self, ast, o):
        pass


    def visitConstDecl(self, ast, o):
        pass


    def visitFuncDecl(self, ast, o):
        pass


    def visitMethodDecl(self, ast, o):
        pass


class Scope:
    def __init__(self):
        self.lst = [[]]


    def current(self):
        """return the current scope

        Returns:
            list: a list of current scope
        """
        return self.lst[-1]

    
    def new_scope(self):
        """append a new scope to the scope chain
        """
        self.lst.append([])
        return
    

    def out_scope(self):
        """pop the current scope out of the scope chain
        """
        self.lst.pop()
        return
    

    def look_up(self, name):
        """return the current object refered

        Args:
            name (str): name of that object (*Ident)

        Returns:
            Symbol: the object
        """
        flatten = [obj for scope in self.lst for obj in scope]
        reverse_flatten = flatten[::-1]
        return next(filter(lambda obj: obj.name == name, reverse_flatten), None)


####################################################
# NOTE: NO SEMANTIC ERROR AT THIS POINT, everything
# is correct, just consider run-time error

# Our task is to generate assembly-like java byte
# code which will be executed by JVM, 
# NOTE that the run-time Java Stack only comes in 
# the execution of the JVM

# 0. CodeGenerator -> .j -> (.class) -> JVM

# 1.
# Thus our task must make a function/method
# to be executed at that time
####################################################

# Mức 1: Sinh mã với các biến chỉ ở các kiểu cơ bản như int,
#  float, boolean và string và thực hiện sinh mã cho 
# các biểu thức và các phát biểu 
# (khai báo và gán phải làm đầu tiên). 
# Khác với init code, các em nên tạo một thành phần của môi trường là 
# "emitter" để cất đối tượng Emitter (mỗi emitter sẽ tạo một file j, do sẽ có nhiều file j nên sẽ có nhiều emitter) 
# tương tự như thành phần "frame" để cất đối tượng Frame để sinh mã cho mỗi phương thức.
class CodeGenerator(BaseVisitor, Utils):


    def __init__(self):
        self.className = "MiniGoClass"
        self.astTree = None
        self.path = None
        self.emit = None
        # added

        # self.global_emitter = None
        self.class_emitters = None
        # self.interface_emitters = None


    def init(self, ast, dir):
        self.main_emitter   = Emitter(dir + '/' + self.className + '.j', self.className)
        # self.global_emitter = Emitter(dir + '/' + 'GlobalClass'  + '.j')
        
        mem = [
            Symbol("putInt",    MType([IntType()],      VoidType()),    CName("io", True)),
            Symbol("putIntLn",  MType([IntType()],      VoidType()),    CName("io", True)),
            Symbol('putFloat',  MType([FloatType()],    VoidType()),    CName('io', True)),
            Symbol('putFloatLn',MType([FloatType()],    VoidType()),    CName('io', True))
                ]
        return mem
    

    def done(self):
        # to write all the buffer to file
        # NOTE: each Emitter has a buffer
        # NOTE: Emitter.printout()      -> just append str to buffer
        # NOTE: Emitter.emit<name>()    -> return the string
        # NOTE: Emitter.emitPROLOG()    -> return str open
        # NOTE: Emiiter.emitEPILOG()    -> write buffer to file

        # 1. GlobalClass
        self.global_emitter.emitEPILOG()

        # 2. MainClass
        self.main_emitter.emitEPILOG()
        pass


    def gen(self, ast, dir_):
        # NOTE: starting point
        # called in test

        gl = self.init(ast, dir_)
        self.astTree = ast
        self.path = dir_
        # for struct -> class -> new file -> new emitter
        # for struct (scatter)
        # for interface -> interface -> new file -> new emitter
        self.main_emitter = Emitter(self.path + '/' + self.className + '.j', self.className)

        # 1. first pass: getting all the emitters for structs
        # and interface
        first_pass = FirstPass(ast, self.path)
        self.class_emitters = first_pass.go()

        # 2. second pass: collect all methods of structs
        # and methods of interfaces, perform type
        # checking to see that whether which interfaces a struct
        # implement
        second_pass = SecondPass(ast)
        structs_interfaces = second_pass.go()
        # debug
        #second_pass.debug_print_result()

        # 3. third pass: generate .class for struct
        # and also fields for struct (prepared for methods)
        # generate all interface files
        third_pass = ThirdPass(ast, self.class_emitters, structs_interfaces)
        third_pass.go()
        third_pass.debug_write()


    # NOTE:
    # Our program will be translated into a assembly-like
    # java bytecode, which will be run by the JVM
    # note that the source code will be
    # in a source named MiniGoClass.java and MiniGoClass.j
    # Because of that, our program will be transformed
    # into a single class of java code


    ####################################################
    # This function will emit the .method public <init>
    # for the MiniGoClass.j
    # All it does is just call the Object.init()
    ####################################################
    def emitObjectInit(self):
        frame = Frame("<init>", VoidType())
        self.emit.printout(self.emit.emitMETHOD("<init>", MType([], VoidType()), False, frame))  # Bắt đầu định nghĩa phương thức <init>
        frame.enterScope(True)  
        self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))  # Tạo biến "this" trong phương thức <init>
        
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))  
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))  
    
        
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))  
        self.emit.printout(self.emit.emitENDMETHOD(frame))  
        frame.exitScope()


    ####################################################
    # May be there is a pass to collect the function
    # and struct and interface first
    # and NOTE that there is no static error at this point
    ####################################################
    def visitProgram(self, ast, c):
        env ={}
        env['env'] = [c]
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        env = reduce(lambda a,x: self.visit(x,a), ast.decl, env)
        self.emitObjectInit()
        self.emit.printout(self.emit.emitEPILOG())
        return env


    ####################################################
    # A Frame is considered to be a stack frame in JVM
    # each method invocation, which will create a new
    # frame and push that in the current 'java stack'
    ####################################################
    def visitFuncDecl(self, ast, o):
        frame = Frame(ast.name, ast.retType)
        isMain = ast.name == "main"
        if isMain:
            mtype = MType([ArrayType([None],StringType())], VoidType())
        else:
            mtype = MType(list(map(lambda x: x.parType, ast.params)), ast.retType)
        o['env'][0].append(Symbol(ast.name, mtype, CName(self.className)))
        env = o.copy()
        env['frame'] = frame
        self.emit.printout(self.emit.emitMETHOD(ast.name, mtype,True, frame))
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        env['env'] = [[]] + env['env']
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType([None],StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            env = reduce(lambda acc,e: self.visit(e,acc),ast.params,env)
        self.visit(ast.body,env)
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(ast.retType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame)) 
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()
        return o
    
        # emitter - GlobalClass
        # frame
        # scope


    def visitVarDecl(self, ast, o):
        if 'frame' not in o: # global var
            o['env'][0].append(Symbol(ast.varName, ast.varType, CName(self.className)))
            self.emit.printout(self.emit.emitATTRIBUTE(ast.varName, ast.varType, True, False, str(ast.varInit.value) if ast.varInit else None))
        else:
            frame = o['frame']
            index = frame.getNewIndex()
            o['env'][0].append(Symbol(ast.varName, ast.varType, Index(index)))
            self.emit.printout(self.emit.emitVAR(index, ast.varName, ast.varType, frame.getStartLabel(), frame.getEndLabel(), frame))  
            if ast.varInit:
                self.emit.printout(self.emit.emitPUSHICONST(ast.varInit.value, frame))
                self.emit.printout(self.emit.emitWRITEVAR(ast.varName, ast.varType, index,  frame))
        return o


    def visitFuncCall(self, ast, o):
        sym = next(filter(lambda x: x.name == ast.funName, o['env'][-1]),None)
        env = o.copy()
        env['isLeft'] = False
        [self.emit.printout(self.visit(x, env)[0]) for x in ast.args]
        self.emit.printout(self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame']))
        return o


    def visitBlock(self, ast, o):
        env = o.copy()
        env['env'] = [[]] + env['env']
        env['frame'].enterScope(False)
        self.emit.printout(self.emit.emitLABEL(env['frame'].getStartLabel(), env['frame']))
        env = reduce(lambda acc,e: self.visit(e,acc),ast.member,env)
        self.emit.printout(self.emit.emitLABEL(env['frame'].getEndLabel(), env['frame']))
        env['frame'].exitScope()
        return o
    

    def visitExpression(self, ast, o):
        # wrapper of expression
        pass


    def visitGlobalDeclaration(self, ast, o):
        # wrapper of global declarations

        # global variable, const
        # 1. add to the current scope
        # 2. generate .field static in GlobalClass

        # struct/interface
        # skip

        # method
        # 1. use class_emitters -> class
        # 2. create a new frame to pass
        # 3. pass the scope to that (chain)

        # function
        # 1. create a new frame to pass
        # 2. pass the scope to that (chain)
        pass


    def visiStmt(self, ast, o):
        # wrapper of statements
        pass


    # normal expr
    def visitIntLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(ast.value, o['frame']), IntType()


    # normal expr
    def visitFloatLiteral(self, ast, o):
        return None
    

    # normal expr
    def visitBinaryOp(self, param):
        return None


    # normal expr
    def visitUnaryOp(self, param):
        return None
    

    # normal expr
    def visitBooleanLiteral(self, param):
        return None


    # normal expr
    def visitStringLiteral(self, param):
        return None


    # normal expr
    def visitArrayLiteral(self, param):
        return None
    

    # normal expr
    def visitStructLiteral(self, param):
        return None


    # normal expr
    def visitNilLiteral(self, param):
        return None


    # expr + type (search in symbol for expr, type -> get?)
    def visitId(self, ast, o):
        sym = next(filter(lambda x: x.name == ast.name, [j for i in o['env'] for j in i]),None)
        if type(sym.value) is Index:
            return self.emit.emitREADVAR(ast.name, sym.mtype, sym.value.value, o['frame']),sym.mtype
        else:         
            return self.emit.emitGETSTATIC(f"{self.className}/{sym.name}",sym.mtype,o['frame']),sym.mtype
    

    def visitConstDecl(self, param):
        return None


    def visitMethodDecl(self, ast, o):
        # emitter .method .end
        # frame
        # scope

        return None


    def visitPrototype(self, param):
        return None


    def visitIntType(self, param):
        return None


    def visitFloatType(self, param):
        return None


    def visitBoolType(self, param):
        return None


    def visitStringType(self, param):
        return None
    

    def visitVoidType(self, param):
        return None


    def visitArrayType(self, param):
        return None


    def visitStructType(self, param):
        return None


    def visitInterfaceType(self, param):
        return None


    def visitAssign(self, param):
        return None


    def visitIf(self, param):
        return None


    def visitForBasic(self, param):
        return None


    def visitForStep(self, param):
        return None


    def visitForEach(self, param):
        return None
    

    def visitContinue(self, param):
        return None


    def visitBreak(self, param):
        return None


    def visitReturn(self, param):
        return None


    # expr + stmt
    def visitMethCall(self, param):
        return None


    # expr + stmt
    def visitArrayCell(self, param):
        return None


    # expr + stmt
    def visitFieldAccess(self, param):
        return None
    

    def visitParamDecl(self, ast, o):
        pass