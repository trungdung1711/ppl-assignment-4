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


    # def test_508(self):
    #     input = \
    #         '''
    #         func main() {
    #             // var name String = getString()
    #             // putStringLn("Your name is: " + name)
    #             var a int = 10
    #             putInt(a)
    #             return
    #         }
    #         '''
    #     expect = '10'

    #     self.assertTrue(TestCodeGen.test(input, expect, 508))


    # def test_509(self):
    #     input = \
    #     '''
    #     func main() {
    #         var a int = 10
    #         var b float = 3.14

    #         putFloatLn(a + b)
    #         return
    #     }
    #     '''
    #     expect = '13.14\n'

    #     self.assertTrue(TestCodeGen.test(input, expect, 509))


    # def test_510(self):
    #     input = \
    #     '''
    #     func main() {
    #         var a = true
    #         var b = false
    #         var c = true
    #         putBool(a && b || c)
    #         return
    #     }
    #     '''
    #     expect = 'true'

    #     self.assertTrue(TestCodeGen.test(input, expect, 510))


    # def test_511(self):
    #     input = \
    #     '''
    #     func main() {
    #         var result boolean = true && (false || false) && ((true && false) || false) && false
    #         putBoolLn(result)
    #         return
    #     }
    #     '''
    #     expect = 'false\n'


    #     self.assertTrue(TestCodeGen.test(input, expect, 511))


    # def test_512(self):
    #     input = \
    #     '''
    #     func main() {
    #         var a int = 100
    #         var b = 100
    #         putIntLn(Add(a, b))
    #         putIntLn(Sub(a, b))
    #         putIntLn(Mul(a, b))
    #         putIntLn(Div(a, b))

    #         putString("End")

    #         return
    #     }

    #     func Add(a int, b int) int {
    #         return a + b
    #     }

    #     func Sub(a int, b int) int {
    #         return a - b
    #     }

    #     func Mul(a int, b int) int {
    #         return a * b
    #     }

    #     func Div(a int, b int) int {
    #         return a / b
    #     }
    #     '''
    #     expect = '200\n0\n10000\n1\nEnd'

    #     self.assertTrue(TestCodeGen.test(input, expect, 512))


    # def test_513(self):
    #     input = \
    #         '''
    #         func main() {
    #             var h Human = Human{name : "Dung", age : 18}
    #             h.print()
    #             return
    #         }

    #         type Human struct {
    #             name string
    #             age int
    #         }

    #         func (h Human) print() {
    #             putStringLn(h.name)
    #             putIntLn(h.age)
                
    #             return
    #         }
    #         '''
    #     expect = 'Dung\n18\n'

    #     self.assertTrue(TestCodeGen.test(input, expect, 513))


    # def test_514(self):
    #     input = \
    #     '''
    #     func main() {
    #         var father = Animal{name : "A", father : nil}
    #         var d = Animal{name : "B", father : father}

    #         var theFather = d.getFather()

    #         putStringLn(d.getFather().getName())
    #         return
    #     }

    #     type Animal struct {
    #         name string 
    #         father Animal
    #     }

    #     func (a Animal) getName() string {
    #         return a.name
    #     }

    #     func (a Animal) getFather() Animal {
    #         return a.father
    #     }
    #     '''

    #     expect = 'A\n'
        
    #     self.assertTrue(TestCodeGen.test(input, expect, 514))


    # def test_515(self):
    #     input = \
    #     '''
    #     func main() {
    #         var animal Animal = Dog{}
    #         var animal1 Animal = Cat{name : "Tom"}
    #         putStringLn(animal.getType())
    #         putStringLn(animal1.getType())
    #         return
    #     }

    #     func (c Cat) getType() string {
    #         return "CAT"
    #     }

    #     type Cat struct {
    #         name string
    #     }

    #     type Dog struct {
    #         name string
    #     }

    #     func (d Dog) getType() string {
    #         return "DOG"
    #     }

    #     type Animal interface {
    #         getType() string
    #     }
    #     '''

    #     expect = 'DOG\nCAT\n'
        
    #     self.assertTrue(TestCodeGen.test(input, expect, 515))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         var a int = 100
    #         a := 2
    #         b := a + 2
    #         putIntLn(a + b)
    #         return
    #     }
    #     '''

    #     expect = '6\n'

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_517(self):
    #     input = \
    #     '''
    #     var GLOBAL int = 100
    #     func main() {
    #         a := 1 + 2
    #         b := 2 + 3.4
    #         c := "string" + "string"
    #         d := true && false
    #         GLOBAL := 200
    #         putIntLn(GLOBAL)
    #         return
    #     }
    #     '''

    #     expect = '200\n'

    #     self.assertTrue(TestCodeGen.test(input, expect, 517))


    # def test_518(self):
    #     input = \
    #     '''
    #     func main() {
    #         a := 100
    #         b := 3.14
    #         c := a + b
    #         d := a % 3
    #         d += 4
    #         putInt(d)
    #         return
    #     }
    #     '''

    #     expect = '5'

    #     self.assertTrue(TestCodeGen.test(input, expect, 518))


    # def test_519(self):
    #     input = \
    #     '''
    #     func main() {
    #         var w Weapon = Tessaiga{dam : 1000.0, special : 100}
    #         putFloatLn(w.getDamage())
    #         putIntLn(w.getSpecial())

    #         w := Tessaiga{dam : 999.9, special : 99}
    #         putFloatLn(w.getDamage())
    #         putIntLn(w.getSpecial())
    #         return
    #     }

    #     type Tessaiga struct {
    #         dam float
    #         special int
    #     }

    #     func (t Tessaiga) getDamage() float {
    #         return t.dam
    #     }

    #     func (t Tessaiga) getSpecial() int {
    #         return t.special
    #     }

    #     type Weapon interface {
    #         getDamage() float
    #         getSpecial() int
    #     }
    #     '''

    #     expect = '1000.0\n100\n999.9\n99\n'

    #     self.assertTrue(TestCodeGen.test(input, expect, 519))


    # def test_520(self):
    #     input = \
    #     '''
    #     var GLOBAL float;
    #     func main() {
    #         var a float = 10;
    #         putFloat(a)
    #         a := 20
    #         putFloat(a)

    #         GLOBAL := 200
    #         putFloatLn(GLOBAL)
    #         return
    #     }
    #     '''

    #     expect = '10.020.0200.0\n'

    #     self.assertTrue(TestCodeGen.test(input, expect, 520))


    def test_521(self):
        input = \
        '''
        func main() {
            var h = Human {name : "Zun", age : 18}
            putStringLn(h.name)
            h.name := "Changed"
            h.age := 100
            putStringLn(h.name)
            putIntLn(h.age)

            h.name := "Dung" + " " + "Le"

            putStringLn(h.name)
            return
        }

        type Human struct {
            name string
            age int
            parents [4]Human
        }
        '''

        expect = 'Zun\nChanged\n100\nDung Le\n'

        self.assertTrue(TestCodeGen.test(input, expect, 521))


    def test_522(self):
        input = \
        '''
        func main() {
            return
        }
        '''

        expect = ''

        self.assertTrue(TestCodeGen.test(input, expect, 522))


    def test_523(self):
        input = \
        '''
        func main() {
            // var arr [3]int = [3]int{1, 2, 3}
            // var arr [4]float = [4]float{3.4, 3.2, 3.4, 5.6}
            // var arr [3]boolean = [3]boolean{true, false, true, false}
            // var arr [2]string = [2]string{"This", "is"}
            // var arr [5]int = [5]int{1, 2, 3, 4, 5}

            var arr [2][2][2]float = [2][2][2]float {{{1.6, 2.1}, {3.3, 4.4}}, {{5.6, 6.7}, {7.4, 8.3}}}
            return
        }
        '''

        expect = ''

        self.assertTrue(TestCodeGen.test(input, expect, 523))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))


    # def test_516(self):
    #     input = \
    #     '''
    #     func main() {
    #         return
    #     }
    #     '''

    #     expect = ''

    #     self.assertTrue(TestCodeGen.test(input, expect, 516))