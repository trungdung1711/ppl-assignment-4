'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod
from functools import reduce


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

class ClassType(Type):
    def __init__(self, name):
        #value: Id
        self.name = name


####################################################
# Our task is to generate assembly-like java byte
# code which will be executed by JVM, 
# NOTE that the run-time Java Stack only comes in 
# the execution of the JVM

# 0. CodeGenerator -> .j -> (.class) -> JVM

# 1.
# Thus our task must make a function/method
# to be executed at that time
####################################################
class CodeGenerator(BaseVisitor,Utils):
    def __init__(self):
        self.className = "MiniGoClass"
        self.astTree = None
        self.path = None
        self.emit = None

    def init(self):
        mem = [
            Symbol("putInt",    MType([IntType()],      VoidType()),    CName("io", True)),
            Symbol("putIntLn",  MType([IntType()],      VoidType()),    CName("io", True)),
            Symbol('putFloat',  MType([FloatType()],    VoidType()),    CName('io', True)),
            Symbol('putFloatLn',MType([FloatType()],    VoidType()),    CName('io', True))
                ]
        return mem

    def gen(self, ast, dir_):
        gl = self.init()
        self.astTree = ast
        self.path = dir_
        self.emit = Emitter(dir_ + "/" + self.className + ".j")
        self.visit(ast, gl)

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


    def visitId(self, ast, o):
        sym = next(filter(lambda x: x.name == ast.name, [j for i in o['env'] for j in i]),None)
        if type(sym.value) is Index:
            return self.emit.emitREADVAR(ast.name, sym.mtype, sym.value.value, o['frame']),sym.mtype
        else:         
            return self.emit.emitGETSTATIC(f"{self.className}/{sym.name}",sym.mtype,o['frame']),sym.mtype


    def visitIntLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(ast.value, o['frame']), IntType()
    

    def visitFloatLiteral(self, ast, o):
        return None
    

    def visitConstDecl(self, param):
        return None


    def visitMethodDecl(self, param):
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


    def visitBinaryOp(self, param):
        return None


    def visitUnaryOp(self, param):
        return None


    def visitMethCall(self, param):
        return None


    def visitArrayCell(self, param):
        return None


    def visitFieldAccess(self, param):
        return None


    def visitBooleanLiteral(self, param):
        return None


    def visitStringLiteral(self, param):
        return None


    def visitArrayLiteral(self, param):
        return None


    def visitStructLiteral(self, param):
        return None


    def visitNilLiteral(self, param):
        return None