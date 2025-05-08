import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # def test_int_literal(self):
    #     input = """func main() {putInt(5);};"""
    #     expect = "5"
    #     self.assertTrue(TestCodeGen.test(input,expect,501))


    # def test_local_var(self):
    #     input = """func main() {var a int = 20;  putInt(a);};"""
    #     expect = "20"
    #     self.assertTrue(TestCodeGen.test(input,expect,502))


    # def test_gllobal_var(self):
    #     input = """var a int = 10; func main() { putInt(a);};"""
    #     expect = "10"
    #     self.assertTrue(TestCodeGen.test(input,expect,503))


    # def test_int_ast(self):
    #     input = Program([FuncDecl("main",[],VoidType(),Block([FuncCall("putInt", [IntLiteral(25)])]))])
    #     expect = "25"
    #     self.assertTrue(TestCodeGen.test(input,expect,504))


    # def test_local_var_ast(self):
    #     input = Program([FuncDecl("main",[],VoidType(),Block([VarDecl("a",IntType(),IntLiteral(500)),FuncCall("putInt", [Id("a")])]))])
    #     expect = "500"
    #     self.assertTrue(TestCodeGen.test(input,expect,505))


    # def test_global_var_ast(self):  
    #     input = Program([VarDecl("a",IntType(),IntLiteral(5000)),FuncDecl("main",[],VoidType(),Block([FuncCall("putInt", [Id("a")])]))])
    #     expect = "5000"
    #     self.assertTrue(TestCodeGen.test(input,expect,506))


    # def test_507(self):
    #     input = \
    #     '''
    #     type Dog struct {
    #         name string
    #         age int
    #         cat Cat
    #         attacker Attacker
    #     }

    #     type Kikyou struct {
    #         name string
    #         age int
    #         weapon Weapon
    #         reiryoku float
    #     }

    #     type Weapon interface {
    #         Damage() float
    #     }

    #     type Hiraikotsu struct {
    #         name string
    #         damage float
    #     }

    #     func (h Hiraikotsu) Damage() float {
    #         return h.damage
    #     }

    #     type Tessaiga struct {
    #         name string
    #         damage float
    #     }

    #     func (t Tessaiga) Damage() float {
    #         return 10000.0
    #     }

    #     type Cat struct {
    #         name string
    #         age int
    #     }

    #     func (c Cat) getType() string {
    #         return "Cat"
    #     }

    #     func (c Cat) attack(h Human) boolean {
    #         return true;
    #     }

    #     type Attacker interface {
    #         attack(h Human) boolean 
    #     }

    #     func (d Dog) getType() string {
    #         return "Dog"
    #     }

    #     func (d Dog) getPower() float {
    #         return 100.100
    #     }

    #     type Human struct {
    #         name string
    #         age int
    #     }

    #     func (h Human) getType() string {
    #         return "Humanity"
    #     }

    #     func (h Human) attack(h Human) boolean {
    #         return false
    #     }

    #     func (d Dog) attack(d Human) boolean {
    #         return true
    #     }

    #     func (h Human) getNumber() int {
    #         return 100
    #     }

    #     type Entity interface {
    #         getNumber() int
    #         getPower() float
    #     }

    #     func (h Human) getPower() float {
    #         return 50.50
    #     }

    #     type Animal interface {
    #         getType() string
    #     }

    #     type Shippou struct {
    #         name string
    #         age int
    #     }

    #     func (s Shippou) getYouki() float {
    #         return 50.0
    #     }

    #     type ShikonNoTama struct {
    #         name string
    #         kakera int
    #     }

    #     func (s ShikonNoTama) Kakera() int {
    #         return 100
    #     }

    #     func (h Human) Kill(people [4]People) boolean {
    #         return True
    #     }

    #     type Ackujin interface {
    #         Kill(people [3]People) boolean
    #     }

    #     type Youkai interface {
    #         getYouki() float
    #     }
    #     '''
    #     expect = '100'

    #     self.assertTrue(TestCodeGen.test(input, expect, 507))


    def test_508(self):
        input = \
            '''
            const PI = 3.14
            func main() {
                var a int;
                return
            }

            func Calculate(a boolean, b boolean) boolean{
                return a && b
            }
            '''
        expect = ''

        self.assertTrue(TestCodeGen.test(input, expect, 508))


    # def test_509(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 509))


    # def test_510(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 510))

    # def test_511(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 511))

    # def test_512(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 512))

    # def test_513(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 513))

    # def test_514(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 514))

    # def test_515(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 515))

    # def test_516(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))

    # def test_517(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 517))

    # def test_518(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 518))

    # def test_519(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 519))

    # def test_520(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 520))

    # def test_521(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 521))

    # def test_522(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 522))

    # def test_523(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 523))

    # def test_524(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 524))

    # def test_525(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 525))

    # def test_526(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 526))

    # def test_527(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 527))

    # def test_528(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 528))

    # def test_529(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 529))

    # def test_530(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 530))

    # def test_531(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 531))

    # def test_532(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 532))

    # def test_533(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 533))

    # def test_534(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 534))

    # def test_535(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 535))

    # def test_536(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 536))

    # def test_537(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 537))

    # def test_538(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 538))

    # def test_539(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 539))

    # def test_540(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 540))

    # def test_541(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 541))

    # def test_542(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 542))

    # def test_543(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 543))

    # def test_544(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 544))

    # def test_545(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 545))

    # def test_546(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 546))

    # def test_547(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 547))

    # def test_548(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 548))

    # def test_549(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 549))

    # def test_550(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 550))

    # def test_551(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 551))

    # def test_552(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 552))

    # def test_553(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 553))

    # def test_554(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 554))

    # def test_555(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 555))

    # def test_556(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 556))

    # def test_557(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 557))

    # def test_558(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 558))

    # def test_559(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 559))

    # def test_560(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 560))

    # def test_561(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 561))

    # def test_562(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 562))

    # def test_563(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 563))

    # def test_564(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 564))

    # def test_565(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 565))

    # def test_566(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 566))

    # def test_567(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 567))

    # def test_568(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 568))

    # def test_569(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 569))

    # def test_570(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 570))

    # def test_571(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 571))

    # def test_572(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 572))

    # def test_573(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 573))

    # def test_574(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 574))

    # def test_575(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 575))

    # def test_576(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 576))

    # def test_577(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 577))

    # def test_578(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 578))

    # def test_579(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 579))

    # def test_580(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 580))

    # def test_581(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 581))

    # def test_582(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 582))

    # def test_583(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 583))

    # def test_584(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 584))

    # def test_585(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 585))

    # def test_586(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 586))

    # def test_587(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 587))

    # def test_588(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 588))

    # def test_589(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 589))

    # def test_590(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 590))

    # def test_591(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 591))

    # def test_592(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 592))

    # def test_593(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 593))

    # def test_594(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 594))

    # def test_595(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 595))

    # def test_596(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 596))

    # def test_597(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 597))

    # def test_598(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 598))

    # def test_599(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 599))


    # def test_600(self):
    #     input = Program(
    #         [
    #             FuncDecl(
    #                 'main',
    #                 [],
    #                 VoidType(),
    #                 Block(
    #                     [
                            
    #                     ]
    #                 )
    #             )
    #         ]
    #     )
    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 600))