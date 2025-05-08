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
# 6/2/2025
from enum import Enum
# instead of StaticCheck
from Visitor import *
# from Utils import Utils
from AST import *

# from StaticError import *
from Emitter import Emitter, MType, ClassType, Method, Class, Interface, StaticMethod
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
    def __init__(self, value, isStatic=True):
        #value: String
        self.isStatic = isStatic
        self.value = value


####################################################
# ADDED CLASS
# Exist in StaticCheck?

####################################################
# In the case of Go (help to prevent semantic meaning):
# Object (named thing):
# - Var     | using Symbol
# - Const   | using Symbol
# - TypeName    - no need (global)
# - Func        - no need (global) - should be method
####################################################
class Symbol:
    def __init__(self, name, mtype, index, is_static):
        self.name       = name       # name
        self.mtype      = mtype      # type of Var/Const
        # flatten that field
        # self.value      = value      # index or CName
        self.is_static  = is_static
        self.index      = index
    

    def getStaticName(self):
        return '/'.join(['MiniGoClass', self.name])


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
        
        elif (not isinstance(m1, Method) or not isinstance(m2, Method)):
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
        # will be used to search for method descriptor [method call]
        self.structs     = dict()    # name - list[methods]
        # will be used to search for method descriptor [method call]
        self.interfaces  = dict()    # name - list[methods]
        # will be used to search for function call
        self.functions   = dict()    # name - method

        self.result      = dict()    # name - list[names]


    def go(self):
        self.visit(self.ast, None)
        self.check()
        return self.result, self.structs, self.interfaces, self.functions


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
        # don't call down function
        fun = ast.fun
        param_types = [self.visit(param, None) for param in fun.params]
        method = Method(fun.name, param_types, fun.retType, class_name)
        self.structs[class_name].append(method)


    def visitFuncDecl(self, ast, o):
        param_types = [self.visit(param, None) for param in ast.params]
        self.functions[ast.name] = StaticMethod(ast.name, param_types, ast.retType, 'MiniGoClass')


    def visitParamDecl(self, ast, o):
        return ast.parType


    def visitInterfaceType(self, ast, o):
        # 1. visit this node
        # we would know all the methods of this interface
        # 2. just allocate the list immediately
        # 3. visit each of the prototype to get the method
        # print(f'Visit interface {ast.name}')
        method_lists = [self.visit(method, ast.name) for method in ast.methods]
        self.interfaces[ast.name] = method_lists


    def visitPrototype(self, ast, o):
        return Method(ast.name, ast.params, ast.retType, o)


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


    def add(self, s):
        self.lst[-1].append(s)


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


# we must know the type of it
# var a int ->  know the type
# var a = 10 -> must use the expression for that
class FourthPass(BaseVisitor):
    def __init__(self, ast, emitter):
        self.ast             = ast
        self.main_emitter    = emitter


    def go(self):
        self.visit(self.ast, None)


    def visitProgram(self, ast, o):
        [self.visit(decl, None) for decl in ast.decl]


    def visitVarDecl(self, ast, o):
        pass


    def visitConstDecl(self, ast, o):
        pass


    def visitMethodDecl(self, ast, o):
        pass


    def visitFuncDecl(self, ast, o):
        pass


    def visitStructType(self, ast, o):
        pass


    def visitInterfaceType(self, ast, o):
        pass


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
        self.class_emitters     = None

        # Can add to the type system, but bypass that
        self.structs            = None      # name - [Method]
        self.interfaces         = None      # name - [Method]
        self.functions          = None      # func - [StaticMethod]
        # self.interface_emitters = None

        # buffer for main class
        self.buff_main          = list()
        self.buff_fields        = list()
        self.buff_inits         = list()
        # self.buff_fields        = list()
        self.buff_methods       = list()


    def init(self, ast, dir):
        self.main_emitter   = Emitter(dir + '/' + self.className + '.j', self.className)
        # self.global_emitter = Emitter(dir + '/' + 'GlobalClass'  + '.j')
        
        # mem = [
        #     Symbol("putInt",    MType([IntType()],      VoidType()),    CName("io", True)),
        #     Symbol("putIntLn",  MType([IntType()],      VoidType()),    CName("io", True)),
        #     Symbol('putFloat',  MType([FloatType()],    VoidType()),    CName('io', True)),
        #     Symbol('putFloatLn',MType([FloatType()],    VoidType()),    CName('io', True))
        #         ]
        # return mem
    

    def initCLass(self):
        # NOTE: nothing to do with return type of Frame
        # frame is used to simulate the operation of the operand
        # stack, to emit .limit stack and locals correctly
        frame = Frame('<init>', VOID)
        method_type = Method('<init>', [], VOID, self.className)

        self.buff_inits.append(
            self.main_emitter.emitMETHOD('<init>', method_type, False, frame)
        )
        # scope of this method
        frame.enterScope(True)

        # NOTE: JVM will automatically push <this> for us
        # frame simulates the operand stack
        this_index = frame.getNewIndex()
        this_type  = Id(self.className)
        # .var is used for debugging
        self.buff_inits.append(self.main_emitter.emitVAR(
            this_index, 
            'this', 
            this_type, 
            frame.getStartLabel(), 
            frame.getEndLabel(), 
            frame))
        
        # put label, for other methods, functions
        # scope are different
        # NOTE
        self.buff_inits.append(
            self.main_emitter.emitLABEL(frame.getStartLabel(), frame)
        )
        # read this from local variable array
        self.buff_inits.append(
            self.main_emitter.emitREADVAR(
                'this',
                this_type,
                0,
                frame
            )
        )
        # invoke the <int>
        self.buff_inits.append(
            self.main_emitter.emitINVOKESPECIAL(
                frame
            )
        )

        self.buff_inits.append(
            self.main_emitter.emitLABEL(
                frame.getEndLabel(), frame
            )
        )

        self.buff_inits.append(
            self.main_emitter.emitRETURN(
                VOID, frame
            )
        )

        # end of the method
        self.buff_inits.append(
            self.main_emitter.emitENDMETHOD(
                frame
            )
        )
        frame.exitScope()


    def done(self):
        # to write all the buffer to file
        # NOTE: each Emitter has a buffer
        # NOTE: Emitter.printout()      -> just append str to buffer
        # NOTE: Emitter.emit<name>()    -> return the string
        # NOTE: Emitter.emitPROLOG()    -> return str open
        # NOTE: Emiiter.emitEPILOG()    -> write buffer to file

        # 1. GlobalClass
        # self.global_emitter.emitEPILOG()

        # 2. MiniGoClass buffer out

        # 3. Other structs

        # Moving all buffer to a main buffer
        # .class
        self.main_emitter.buffer(
            ''.join(self.buff_main)
        )

        self.main_emitter.buffer(
            self.main_emitter.emit_line(1)
        )

        # .field
        self.main_emitter.buffer(
            ''.join(self.buff_fields)
        )

        # .<init>
        self.main_emitter.buffer(
            ''.join(self.buff_inits)
        )

        # .method
        self.main_emitter.buffer(
            ''.join(self.buff_methods)
        )

        # <clinit>
        self.main_emitter.buffer(
            ''.join(self.generateclinit())
        )

        # write to the buffer
        # write MiniGoClass
        self.main_emitter.emitEPILOG()

        # write all the emitter of structs
        [emitter.emitEPILOG() for name, emitter in self.class_emitters.items()]


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
        # will be used in CodeGenerator to search for method descriptors used for
        # invoke?
        structs_interfaces, structs, interfaces, functions = second_pass.go()
        self.structs    = structs
        # must return a type to detect that one
        self.interfaces = interfaces
        self.functions  = functions
        # debug
        #second_pass.debug_print_result()

        # 3. third pass: generate .class for struct
        # and also fields for struct (prepared for methods)
        # generate all interface files

        # must also remember to produce .implement
        third_pass = ThirdPass(ast, self.class_emitters, structs_interfaces)
        third_pass.go()
        # third_pass.debug_write()

        # 4. fourth pass: prepare the MiniGoClass.j initialization
        # generate all .field static for struct
        # generate simple <init>

        # <clinit> would require the generation of expression
        # then this would be handled in the final pass
        # generate <clinit>

        # 5. final pass: generate the:
        # - global field    -> .field static
        # - constant field  -> .field final static
        #   if initialisation -> must be done in the <clinit>
        # - function        -> .method static in MiniGoClass.j
        # - method          -> .method for each of the emitter
        
        # first, we have to generate the main class, first
        # .source, .class, .super
        # buffer the init
        # self.initCLass()

        # then starting traversing the tree
        # global -> field -> buffer it to the fields
        # function -> buffer it to the methods
        # method -> get the correct emitter pass -> generate method of others
        
        # finally, generate the <clinit> method for class
        # then write buffer to files
        

        # pass 4
        self.visit(ast, None)
        self.done()


    def addDefaultFunctions(self):
        # because this is the mapping between MiniGo
        # to Java, Function would be mapped to static method
        # a static method is defined by <class>/<field>
        # the <class> must be defined as fully resolved
        # invokestatic io/putInt
        # invokestatic MiniGoClass/Add
        self.functions['putInt']    = StaticMethod('putInt', [INTTYPE], VOID, 'io')
        self.functions['putIntLn']  = StaticMethod('putIntLn', [INTTYPE], VOID, 'io')
        mem = [
        Symbol("putInt",    MType([IntType()],      VoidType()),    CName("io", True)),
        Symbol("putIntLn",  MType([IntType()],      VoidType()),    CName("io", True)),
        Symbol('putFloat',  MType([FloatType()],    VoidType()),    CName('io', True)),
        Symbol('putFloatLn',MType([FloatType()],    VoidType()),    CName('io', True))
            ]


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
    def visitProgram(self, ast, o):
        # buffer the init to this part
        # self.initCLass()
        self.buff_main.append(
            self.main_emitter.emitPROLOG(
                self.className, 'java/lang/Object'
            )
        )

        # create the scope to be used
        emitter = None
        frame = None
        scope = Scope()

        [self.visitGlob(decl, (emitter, frame, scope)) for decl in ast.decl]

        # add the <init> MiniGoClass
        self.initCLass()

        return
        env ={}
        env['env'] = [c]
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        env = reduce(lambda a,x: self.visit(x,a), ast.decl, env)
        self.emitObjectInit()
        self.emit.printout(self.emit.emitEPILOG())
        return env


    def visitGlob(self, ast, o):
        # wrapper of global
        scope : Scope = o[2]

        # case VarDecl, Const
        # 1. create Symbol, add that to the Scope
        # 2. Getting the type
        # 3. create Symbol with static
        # 4. generate .field and put it into the buff_fields
        # not the main_emitter buffer
        fake_frame = Frame('not-used', VOID)

        if isinstance(ast, VarDecl):
            # generate <init> in the <clinit>
            name    = ast.varName
            typ     = ast.varType
            expr    = ast.varInit

            var_type = None
            if typ is not None:
                # get the type
                var_type = self.visitType(typ, o)
            else:
                # type is None, must 
                # get the type from expression

                # because this is not related
                # with any kind of frame
                # not create a new frame
                # a frame is related to method
                # then, this is just simulated frame
                # not generate with method
                _, var_type = self.visitExpr(expr, (self.main_emitter, fake_frame))
            
            # Now I have the type
            # int, bool, float, String, Dog, Animal
            # Symbol with static
            # generate .field
            symbol = Symbol(name, var_type, -1, True)
            scope.add(symbol)
            # then generate the .field in the buff_fields
            self.buff_fields.append(
                self.main_emitter.emitATTRIBUTE(name, var_type, True, False, None)
            )


        elif isinstance(ast, ConstDecl):
            # note that final field in java
            # perform exactly like another field
            # but it prevents reassignment of that value
            # and if it is static, or a object field, it must
            # contain the initialization -> the expr, 
            # which can be initilize in <clinint>
            # .final, then must provide value at compiled time
            # pass
            # so quite the same as the VarDecl
            name = ast.conName
            expr = ast.iniExpr

            _, const_type = self.visitExpr(expr, (self.main_emitter, fake_frame, scope))

            # now we have the type
            # create the symbol
            symbol = Symbol(name, const_type, -1, True)
            scope.add(symbol)

            self.buff_fields.append(
                self.main_emitter.emitATTRIBUTE(name, const_type, True, True, None)
            )

        else:
            # normal logic
            self.visit(ast, o)


    def findFunction(self, name):
        # StaticMethod
        return self.functions[name]


    def findMethod(self, className, methodName):
        method_list = self.structs[className]
        return next(filter(lambda method: method.name == methodName, method_list), None)


    def findMethodI(self, interfaceName, methodName):
        method_list = self.interfaces[interfaceName]
        return next(filter(lambda method: method.name == methodName, method_list), None)


    ####################################################
    # A Frame is considered to be a stack frame in JVM
    # each method invocation, which will create a new
    # frame and push that in the current 'java stack'
    ####################################################
    def visitFuncDecl(self, ast, o):
        name    = ast.name
        params  = ast.params
        result  = ast.retType
        body    = ast.body

        # emitter -> self.main_emitter
        # frame -> create
        scope : Scope = o[2]
        
        frame = Frame(name, result)

        type_descriptor = None
        if name == 'main':
            # for array
            frame.getNewIndex()
            type_descriptor = StaticMethod('main', [ArrayType([VOID], STRTYPE)], VOID, 'MiniGoClass')
        else:
            type_descriptor = self.findFunction(name)
        
        # Starting generate code
        code = list()

        code.append(
            self.main_emitter.emitMETHOD(name, type_descriptor, True, frame)
        )

        scope.new_scope()
        frame.enterScope(True)
        # param in
        code.append(
            self.main_emitter.emitLABEL(
                frame.getStartLabel(), 
                frame
            )
        )

        # visit Parameters to add that to the Scope
        # Resolve later
        # And also create the Index to resolve to them
        [self.visit(param, (self.main_emitter, frame, scope)) for param in params]

        # Now we have to add the Symbol to be resolved later on
        # in the Scope

        # new create a new scope to visit the body
        scope.new_scope()
        frame.enterScope(False)
        # scope -- always point to the current scope
        # then we have to pop it correctly
        code.append(
            self.main_emitter.emitLABEL(
                frame.getStartLabel(),
                frame
            )
        )

        # body of the function
        code.append(
            self.visit(body, (self.main_emitter, frame, scope))
        )


        code.append(
            self.main_emitter.emitLABEL(
                frame.getEndLabel(), 
                frame
            )
        )
        # out body
        frame.exitScope()
        scope.out_scope()

        # end body
        code.append(
            self.main_emitter.emitLABEL(
                frame.getEndLabel(), 
                frame
            )
        )

        code.append(
            self.main_emitter.emitENDMETHOD(frame)
        )
        # out param
        frame.exitScope()
        scope.out_scope()

        # done func -> going into buffer
        # code of a function
        self.buff_methods.append(
            ''.join(code)
        )

        # same thing
        return
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


    def visitMethodDecl(self, ast, o):

        scope   : Scope   = o[2]

        thisVarName = ast.receiver
        thisType = self.visitType(ast.recType, o)
        className = thisType.name
        methodName = ast.fun.name
        params = ast.fun.params
        body = ast.fun.body

        # 0. get the method
        method = self.findMethod(className, methodName)

        # 1. get the correct emitter
        emitter : Emitter = self.class_emitters[thisType.name]
        code = list()
        # 2. scope and frame created
        # create a frame
        frame : Frame = Frame(methodName, method.result)

        # starting generating code

        code.append(
            emitter.emitMETHOD(methodName, method, False, frame)
        )
        # enter scope of this
        scope.new_scope()
        frame.enterScope(True)
        code.append(
            emitter.emitLABEL(frame.getStartLabel(), frame)
        )

        # must create and add the this pointer
        thisIndex = frame.getNewIndex()
        symbol = Symbol(thisVarName, thisType, thisIndex, False)
        scope.add(symbol)

        # must create and add this map for param
        scope.new_scope()
        frame.enterScope(False)
        code.append(
            emitter.emitLABEL(frame.getStartLabel(), frame)
        )

        # PARAM
        [self.visit(param, (emitter, frame, scope)) for param in params]

        # BODY
        scope.new_scope()
        frame.enterScope(False)
        code.append(
            emitter.emitLABEL(frame.getStartLabel(), frame)
        )

        # MUST VISIT BODY
        # body of the method
        code.append(
            self.visit(body, (emitter, frame, scope))
        )

        code.append(
            emitter.emitLABEL(frame.getEndLabel(), frame)
        )
        scope.out_scope()
        frame.exitScope()
        

        # param
        code.append(
            emitter.emitLABEL(frame.getEndLabel(), frame)
        )
        scope.out_scope()
        frame.exitScope()


        # this
        code.append(
            emitter.emitLABEL(frame.getEndLabel(), frame)
        )
        scope.out_scope()
        code.append(
            emitter.emitENDMETHOD(frame)
        )
        frame.exitScope()

        # buffer
        emitter.buffer(''.join(code))


    def visitBlock(self, ast, o):
        stmts = ast.member

        # emitter : Emitter = o[0]
        # frame   : Frame   = o[1]
        # scope   : Scope   = o[2]

        code = list()
        # frame.enterScope(False)

        # code.append(
        #     emitter.emitLABEL(frame.getStartLabel(), frame)
        # )

        # must generate code for each of the statement
        # inside this block
        [code.append(self.visiStmt(stmt, o)) for stmt in stmts]

        # code.append(
        #     emitter.emitLABEL(frame.getEndLabel(), frame)
        # )

        # frame.exitScope()

        return ''.join(code)

        return
        env = o.copy()
        env['env'] = [[]] + env['env']
        env['frame'].enterScope(False)
        self.emit.printout(self.emit.emitLABEL(env['frame'].getStartLabel(), env['frame']))
        env = reduce(lambda acc,e: self.visit(e,acc),ast.member,env)
        self.emit.printout(self.emit.emitLABEL(env['frame'].getEndLabel(), env['frame']))
        env['frame'].exitScope()
        return o


    def visitParamDecl(self, ast, o):
        # create the Symbol
        # and add the variable to the current scope
        # to be used later on?
        # also create the index for it as well
        # get it from the Frame, create Symbol to be used
        # and load later on

        # low level, must load using offset, not name anymore
        # NAME -> NUMBER/OFFSET

        # mapping from name and offset
        # refer to a name -> resolve to offset

        name = ast.parName
        typ = self.visitType(ast.parType, o)

        emitter : Emitter   = o[0]
        frame : Frame       = o[1]
        scope : Scope       = o[2]
        new_index = frame.getNewIndex()
        symbol = Symbol(name, typ, new_index, False)

        # for debug
        

        scope.add(symbol)

        return emitter.emitVAR(new_index, name, typ, 1, 2, frame)


    def visitVarDecl(self, ast, o):
        name    = ast.varName
        typ     = ast.varType
        expr    = ast.varInit

        emitter: Emitter = o[0]
        frame : Frame    = o[1]
        scope : Scope    = o[2]

        code = list()
        # assume local variable
        # the Global will be handled differently in .field public static I
        
        # if there is expr, then generate code of the 
        # expression and store to the local variable array

        # if there is no expr, 

        # after that create symbol to add to the scope

        # there is expression

        # type coersion as well
        # interface and struct as well
        final_type = None
        index = frame.getNewIndex()

        # var a float = 1 -> OK
        # must match?
        # var a float = 1.0

        if typ and expr:
            # always generate the type
            # based on the expr, except the case of interface
            # var a float = int_value
            result, result_type = self.visitExpr(expr, o)
            
            code.append(
                result
            )

            if isinstance(typ, FloatType) and isinstance(result_type, IntType):
                final_type = typ
                code.append(
                    emitter.emitI2F(frame)
                )

            if not isinstance(typ, Interface):
                # keep the type of the expression
                # because it must be the same
                final_type = result_type
            
            else:
                # interface must keep that Interface
                final_type = typ
            
            code.append(
                emitter.emitWRITEVAR(name, result_type, index, frame)
            )

        elif typ and not expr:
            # generate based on the type
            final_type = typ

        elif expr and not typ:
            # generate based on expression
            # getting the type from the expression

            result, result_type = self.visitExpr(expr, o)
            final_type = result_type
            code.append(
                result
            )

            code.append(
                emitter.emitWRITEVAR(name, final_type, index, frame)
            )

        # creating a new symbol
        # for other expression to resolve later
        # on, resolve -> access it again, through the index
        symbol = Symbol(name, final_type, index, False)
        scope.add(symbol)

        return ''.join(code)
    
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
        # generate a static method in MiniGoClass
        # and buffer it in the methods part
        # create the scope correctly
        # add the Scope, It won't affect the local variable array
        # the scope is abstract by using Scope
        # -> resolve differently
        return
        sym = next(filter(lambda x: x.name == ast.funName, o['env'][-1]),None)
        env = o.copy()
        env['isLeft'] = False
        [self.emit.printout(self.visit(x, env)[0]) for x in ast.args]
        self.emit.printout(self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame']))
        return o


    def generateMain(self, ast, frame):
        main = StaticMethod('main', [ArrayType([VOID], STRTYPE)], VOID, 'MiniGoClass')
        self.buff_methods.append(
            self.main_emitter.emitMETHOD('main', main, True, frame)
        )
        return


    class Operator(Enum):
        ADD     = '+'
        SUB     = '-' #
        MUL     = '*'
        DIV     = '/'
        MOD     = '%'
        EQ      = '=='
        NEQ     = '!='
        LT      = '<'
        GT      = '>'
        LTE     = '<='
        GTE     = '>='
        NOT     = '!' #
        AND     = '&&'
        OR      = '||'


    def visiStmt(self, ast, o):
        # wrapper of statements
        # just return the code
        # the parent will link that
        # to the method/function/if/for
        if isinstance(ast, FuncCall):
            pass

        elif isinstance(ast, MethCall):
            pass

        else:
            return self.visit(ast, o)
        

    def generateclinit(self):
        ast = self.astTree
        # going through VarDecl and ConstDecl
        # to create the code of expression and
        # put the value to the getstatic
        return []


    def visitExpr(self, ast, o):
        # wrapper of expression
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        scope   : Scope   = o[2]
        if isinstance(ast, Id):
            # special treat
            # must resolve using the Scope
            # Check for the type and load it from the
            # local variable array or heap if Object
            # as we are backed by JVM (OOP virtual machine)
            # then have to check it is static/local
            # local -> index
            # static -> getfield
            code = list()
            name = ast.name
            
            # check for the scope
            symbol : Symbol = scope.look_up(name)
            if symbol.is_static:
                code.append(
                    emitter.emitGETSTATIC(symbol.getStaticName(), symbol.mtype, frame)
                )

            else:
                # local variable
                # debug
                # print(symbol.name)
                # print(emitter.emitREADVAR(symbol.name, symbol.mtype, symbol.index, frame))
                code.append(
                    emitter.emitREADVAR(symbol.name, symbol.mtype, symbol.index, frame)
                )

            
            return ''.join(code), symbol.mtype

        else:
            return self.visit(ast, o)


    # normal expr
    def visitIntLiteral(self, ast, o):
        value = ast.value
        # only return the code and the type from that
        # others will buffer or printout that code for us
        # must use the current emitter (actually any)
        # must pass the current frame to simulate the operand stack
        # for type inference, used by assign or declaration to create
        # new variable, we have to return the type
        # ----------------
        # var a = 100 - 49
        # var b = a + 4
        emitter : Emitter   = o[0]
        frame : Frame       = o[1]
        # operand stack is just like registers
        return emitter.emitPUSHICONST(value, frame), INTTYPE


    # normal expr
    def visitFloatLiteral(self, ast, o):
        value = ast.value
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]

        return emitter.emitPUSHFCONST(value, frame), FLOATTYPE


    # normal expr
    def visitBooleanLiteral(self, ast, o):
        value = ast.value
        # change from True, False -> true, false
        # type descriptor is Z
        # but operate using int value iconst, iload
        value = str(value).lower()
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        return emitter.emitPUSHICONST(value, frame), BOOLTYPE
    

    # normal expr
    def visitStringLiteral(self, ast, o):
        value = ast.value
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        return emitter.emitPUSHCONST(value, STRTYPE, frame), STRTYPE
    

    # normal expr
    # don't care about the size
    # it is just the Object
    # create a new object of array literal
    # but we need either the dimen or the initialization
    # the size can be found at run-time, so
    # it is ok about that
    # [3][4][5][6]int{} -> static check would ensure
    # this is totally correct
    
    # we are sure that the type is correct
    # [5][2]int {{2, 3}, {4, 5}, {6, 7}, {3, 2}, {5, 6}}
    # Based on the dimension, and collect the list?

    # from the array literal -> deduce size -> difficult?
    # we have [expr][expr][expr]int -> create from that
    # and because the value to be corrected, then no need
    # to worry about that
    def visitArrayLiteral(self, ast, o):
        # the value is just primitive
        # int, float, boolean, String
        # not the object

        # so, there is no array of referece?
        pass


    # normal expr
    def visitNilLiteral(self, ast, o):
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        return emitter.emitNULL(frame)


    # normal expr
    def visitStructLiteral(self, ast, o):
        name = ast.name

        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        scope   : Scope   = o[2]

        # calling new to create the object
        # invokespecial to call the <init> -> default Object
        # for each of the init
        # visit the expression to get the value
        # and the value to the field

        # new
        code = list()

        code.append(
            emitter.emitNEW(
                name, 
                frame
            )
        )

        # dup and calling special
        code.append(
            emitter.emitDUP(frame)
        )

        # calling default init
        code.append(
            emitter.emitDEFAULTINIT(name, frame)
        )

        # for each of the init
        # 1. dup
        # 2. visit expr -> code
        # 3. append that code
        # 4. emit putfield
        # 5. result would be the reference object in the operand stack

        for field, expr in ast.elements:
            # SOS
            code.append(
                emitter.emitDUP(frame)
            )
            result, result_type = self.visitExpr(expr, o)
            code.append(
                result
            )

            code.append(
                emitter.emitPUTFIELD('/'.join([name, field]), result_type, frame)
            )

        return ''.join(code), Class(name)


    # normal expr
    def visitBinaryOp(self, ast, o):
        op = ast.op
        x = ast.left
        y = ast.right
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        result_x, type_x = self.visitExpr(x, o)
        result_y, type_y = self.visitExpr(y, o)
        identical = SecondPass.identical

        code = list()

        if op == CodeGenerator.Operator.ADD.value:
            # + - type check in done
            # 1 + 1
            # 1.4 + 1.5
            # 1 + 1.5
            # 1.5 + 1
            # "str" + "str"
            if identical(type_x, INTTYPE) and identical(type_y, INTTYPE):
                # just add them together, because they are the same type
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitADDOP('+', INTTYPE, frame)
                )
                return ''.join(code), INTTYPE

            elif identical(type_x, FLOATTYPE) and identical(type_x, FLOATTYPE):
                # add normal and generate the fadd
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitADDOP('+', FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE

            elif identical(type_x, STRTYPE) and identical(type_x, STRTYPE):
                # must use the StringBuilder
                code.append(
                    emitter.emitSTRINGADD(frame, result_x, result_y)
                )
                return ''.join(code), STRTYPE

            elif identical(type_x, FLOATTYPE):
                # must change the type before doing that
                # job of compiler, change y value to float
                # and perform float add
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitI2F(frame)
                )

                code.append(
                    emitter.emitADDOP('+', FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE

            elif identical(type_y, FLOATTYPE):
                # must change the type before add
                code.append(
                    result_x
                )

                code.append(
                    emitter.emitI2F(frame)
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitADDOP('+', FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE
            
        elif op == CodeGenerator.Operator.SUB.value:
            # -
            if identical(type_x, INTTYPE) and identical(type_y, INTTYPE):
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitADDOP('-', INTTYPE, frame)
                )
                return ''.join(code), INTTYPE

            elif identical(type_x, FLOATTYPE) and identical(type_x, FLOATTYPE):
                # add normal and generate the fadd
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitADDOP('-', FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE
            
            elif identical(type_x, FLOATTYPE):
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitI2F(frame)
                )

                code.append(
                    emitter.emitADDOP('-', FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE

            elif identical(type_y, FLOATTYPE):
                code.append(
                    result_x
                )

                code.append(
                    emitter.emitI2F(frame)
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitADDOP('-', FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE
            
        elif op == CodeGenerator.Operator.MUL.value or \
            op == CodeGenerator.Operator.DIV.value:
            # *, /
            if identical(type_x, INTTYPE) and identical(type_y, INTTYPE):
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitMULOP(op, INTTYPE, frame)
                )
                return ''.join(code), INTTYPE

            elif identical(type_x, FLOATTYPE) and identical(type_x, FLOATTYPE):
                # add normal and generate the fadd
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitMULOP(op, FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE
            
            elif identical(type_x, FLOATTYPE):
                code.append(
                    result_x
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitI2F(frame)
                )

                code.append(
                    emitter.emitMULOP(op, FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE

            elif identical(type_y, FLOATTYPE):
                code.append(
                    result_x
                )

                code.append(
                    emitter.emitI2F(frame)
                )

                code.append(
                    result_y
                )

                code.append(
                    emitter.emitMULOP(op, FLOATTYPE, frame)
                )
                return ''.join(code), FLOATTYPE
        
        elif op == CodeGenerator.Operator.MOD.value:
            code.append(
                result_x
            )

            code.append(
                result_y
            )

            code.append(
                emitter.emitMOD(frame)
            )

            return ''.join(code), INTTYPE
        
        elif op == CodeGenerator.Operator.EQ.value or \
            op == CodeGenerator.Operator.NEQ.value or \
            op == CodeGenerator.Operator.GT.value or \
            op == CodeGenerator.Operator.LT.value or \
            op == CodeGenerator.Operator.GTE.value or \
            op == CodeGenerator.Operator.LTE.value :
            # just handle the case of int first
            code.append(
                result_x
            )

            code.append(
                result_y
            )

            if identical(type_x, INTTYPE) and identical(type_y, INTTYPE):
                code.append(
                    emitter.emitREOP(op, INTTYPE, frame)
                )
                return ''.join(code), BOOLTYPE

            elif identical(type_x, FLOATTYPE) and identical(type_y, FLOATTYPE):
                pass

            elif identical(type_x, STRTYPE) and identical(type_y, STRTYPE):
                
                pass

        elif op == CodeGenerator.Operator.AND.value or \
            op == CodeGenerator.Operator.OR.value:

            func = emitter.emitOROP if op == '||' else emitter.emitANDOP
            code.append(
                result_x
            )

            code.append(
                result_y
            )

            code.append(
                func(frame)
            )

            return ''.join(code), BOOLTYPE


    # normal expr
    # type checking is done right now
    # no worry about that
    def visitUnaryOp(self, ast, o):
        op      = ast.op
        expr    = ast.body

        emitter : Emitter   = o[0]
        frame   : Frame     = o[1]
        result, typ = self.visitExpr(expr, o)


        if op == CodeGenerator.Operator.SUB.value:
            # - _ -type is the same
            return emitter.emitNEGOP(typ, frame), typ

        elif op == CodeGenerator.Operator.NOT.value:
            # must generate code for that boolean
            # because jvm doesn't support
            # ! _
            false_label = frame.getNewLabel()
            end_label = frame.getNewLabel()

            code = list()
            
            code.append(result)

            code.append(
                emitter.emitIFFALSE(false_label, frame)
            )

            code.append(
                emitter.emitPUSHICONST('false', frame)
            )

            code.append(
                emitter.emitGOTO(end_label, frame)
            )

            code.append(
                emitter.emitLABEL(false_label, frame)
            )

            code.append(
                emitter.emitPUSHICONST('true', frame)
            )

            code.append(
                emitter.emitLABEL(end_label, frame)
            )
            
            return ''.join(code), typ


    # expr + type (search in symbol for expr, type -> get?)
    def visitId(self, ast, o):
        return
        sym = next(filter(lambda x: x.name == ast.name, [j for i in o['env'] for j in i]),None)
        if type(sym.value) is Index:
            return self.emit.emitREADVAR(ast.name, sym.mtype, sym.value.value, o['frame']),sym.mtype
        else:         
            return self.emit.emitGETSTATIC(f"{self.className}/{sym.name}",sym.mtype,o['frame']),sym.mtype


    def visitConstDecl(self, ast, o):
        return None


    def visitType(self, ast, o):
        # wrapper for type
        if isinstance(ast, Id):
            # then we must resolve
            # using the scope
            # Var, Const, Named, Func
            # must be named -> static checking
            # it can be class, or interface
            # then we have to check for that
            # to create the correct way
            # when loading it to the operand
            # stack, we can know 
            # the type to invoke using 
            # invokeinterface or invokevirtual
            # must check if it an interface
            # or it is the struct actually

            name = ast.name
            if name in self.structs:
                # class
                return Class(name)
            else:
                # interface
                return Interface(name)

        else:
            return self.visit(ast, o)


    def visitIntType(self, ast, o):
        return INTTYPE


    def visitFloatType(self, ast, o):
        return FLOATTYPE


    def visitBoolType(self, ast, o):
        return BOOLTYPE


    def visitStringType(self, ast, o):
        return STRTYPE
    

    def visitVoidType(self, ast, o):
        return VOID


    def visitArrayType(self, ast, o):
        # [3][4][5]int?
        return ast


    # different - declaration
    def visitStructType(self, ast, o):
        return None


    # different - declaration
    def visitInterfaceType(self, ast, o):
        return None


    def visitAssign(self, ast, o):
        lhs = ast.lhs
        rhs = ast.rhs
        
        # check if the right-hand side is declared
        # declared -> get that value and modified
        # not declared -> declared that with the value of expr

        # if left-hand side is object
        # array access

        # return the code to modify the value
        return ''


    def visitIf(self, ast, o):
        return None


    def visitForBasic(self, ast, o):
        return None


    def visitForStep(self, ast, o):
        return None


    def visitForEach(self, ast, o):
        return None
    

    def visitContinue(self, param):
        return None


    def visitBreak(self, param):
        return None


    def visitReturn(self, ast, o):
        expr = ast.expr

        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        scope   : Scope   = o[2]

        code = list()
        if expr:
            result, result_type = self.visitExpr(expr, o)
            code.append(
                result
            )

            code.append(
                emitter.emitRETURN(result_type, frame)
            )
        else:
            code.append(
                emitter.emitRETURN(VOID, frame)
            )

        return ''.join(code)



    # expr + stmt
    def visitMethCall(self, param):
        return None


    # expr + stmt
    def visitArrayCell(self, param):
        return None


    # expr + stmt
    def visitFieldAccess(self, param):
        return None


    def visitPrototype(self, ast, o):
        return None