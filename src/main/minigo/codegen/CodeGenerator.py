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
from Emitter import Emitter, MType, ClassType, Method
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
        method = Method(fun.name, param_types, fun.retType)
        self.structs[class_name].append(method)


    def visitFuncDecl(self, ast, o):
        param_types = [self.visit(param, None) for param in ast.params]
        self.functions[ast.name] = Method(ast.name, param_types, ast.retType)


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
        return Method(ast.name, ast.params, ast.retType)


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
        self.structs            = None
        self.interfaces         = None
        self.functions          = None
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


    def visit_global_declaration(self, ast, o):
        # wrapper of global declarations

        # global variable, const
        # 1. add to the current scope
        # 2. generate .field static in GlobalClass
        # jvm provides us with getstatic and putstatic <class>/name type
        # we could store the buffer in different place, before rearrange them
        # must follow the scoping rules for program correctness
        # jvm allows, but minigo doesn't allow
        # we know that minigo doesn't do that, but it could
        # lead to confusion?

        # or NOTE:
        # we can generate all static fields in the first place
        # along with the <clinit> and <init>
        # then for this pass, we just create Symbol and
        # add that to the scope, this allows the program correctness
        # as we would resolve to the correct Symbol
        # and java allows we can access to any static in any order

        # in MiniGoClass.j
        # [static]-[init]-///-[function]-[clinit]
        # must follow the scope rule for correctly resolve

        # for the <clinit>, visit the static field again
        # if there are expression in init part, visit that part
        # to genrate the value and putstatic
        
        # we require to resolve the id, to check that
        # if it is declared locally (stored in the local variable array)
        # if it is declared globally (must access using getStatic and putStatic)
        # different from Object, defined by type?
        # pass 5?

        # struct/interface
        # skip

        # method
        # 1. use class_emitters -> class
        # 2. create a new frame to pass
        # 3. pass the scope to that (chain)
        # 4. just buffer the code normally

        # function
        # 1. create a new frame to pass
        # 2. pass the scope to that (chain)
        # 3. special treat for <main>
        # not really?
        pass


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


    def visitExpr(self, ast, o):
        # wrapper of expression
        pass


    def visiStmt(self, ast, o):
        # wrapper of statements
        pass


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
        return None


    # normal expr
    def visitStructLiteral(self, ast, o):
        return None


    # normal expr
    def visitBinaryOp(self, ast, o):
        op = ast.op
        x = ast.left
        y = ast.right
        emitter : Emitter = o[0]
        frame   : Frame   = o[1]
        result_x, type_x = self.visitExpr(x, (emitter, frame))
        result_y, type_y = self.visitExpr(y, (emitter, frame))
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
        result, typ = self.visitExpr(expr, (emitter, frame))


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
        sym = next(filter(lambda x: x.name == ast.name, [j for i in o['env'] for j in i]),None)
        if type(sym.value) is Index:
            return self.emit.emitREADVAR(ast.name, sym.mtype, sym.value.value, o['frame']),sym.mtype
        else:         
            return self.emit.emitGETSTATIC(f"{self.className}/{sym.name}",sym.mtype,o['frame']),sym.mtype
    

    def visitConstDecl(self, ast, o):
        return None


    def visitMethodDecl(self, ast, o):
        # emitter .method .end
        # frame
        # scope

        return None


    def visitPrototype(self, ast, o):
        return None


    def visitIntType(self, ast, o):
        return None


    def visitFloatType(self, ast, o):
        return None


    def visitBoolType(self, ast, o):
        return None


    def visitStringType(self, ast, o):
        return None
    

    def visitVoidType(self, ast, o):
        return None


    def visitArrayType(self, ast, o):
        return None


    def visitStructType(self, ast, o):
        return None


    def visitInterfaceType(self, ast, o):
        return None


    def visitAssign(self, ast, o):
        return None


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