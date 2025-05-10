import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):

    def test_int_literal(self):
        input = """func main() {putInt(5);};"""
        expect = "5"
        self.assertTrue(TestCodeGen.test(input,expect,501))


    def test_local_var(self):
        input = """func main() {var a int = 20;  putInt(a);};"""
        expect = "20"
        self.assertTrue(TestCodeGen.test(input,expect,502))


    def test_gllobal_var(self):
        input = """var a int = 10; func main() { putInt(a);};"""
        expect = "10"
        self.assertTrue(TestCodeGen.test(input,expect,503))


    def test_int_ast(self):
        input = Program([FuncDecl("main",[],VoidType(),Block([FuncCall("putInt", [IntLiteral(25)])]))])
        expect = "25"
        self.assertTrue(TestCodeGen.test(input,expect,504))


    def test_local_var_ast(self):
        input = Program([FuncDecl("main",[],VoidType(),Block([VarDecl("a",IntType(),IntLiteral(500)),FuncCall("putInt", [Id("a")])]))])
        expect = "500"
        self.assertTrue(TestCodeGen.test(input,expect,505))


    def test_global_var_ast(self):  
        input = Program([VarDecl("a",IntType(),IntLiteral(5000)),FuncDecl("main",[],VoidType(),Block([FuncCall("putInt", [Id("a")])]))])
        expect = "5000"
        self.assertTrue(TestCodeGen.test(input,expect,506))


    def test_507(self):
        input = \
        '''
        type Dog struct {
            name string
            age int
            cat Cat
            attacker Attacker
        }

        func main() {
            putInt(100)
        }

        type Kikyou struct {
            name string
            age int
            weapon Weapon
            reiryoku float
        }

        type Weapon interface {
            Damage() float
        }

        type Hiraikotsu struct {
            name string
            damage float
        }

        func (h Hiraikotsu) Damage() float {
            return h.damage
        }

        type Tessaiga struct {
            name string
            damage float
        }

        func (t Tessaiga) Damage() float {
            return 10000.0
        }

        type Cat struct {
            name string
            age int
        }

        func (c Cat) getType() string {
            return "Cat"
        }

        func (c Cat) attack(h Human) boolean {
            return true;
        }

        type Attacker interface {
            attack(h Human) boolean 
        }

        func (d Dog) getType() string {
            return "Dog"
        }

        func (d Dog) getPower() float {
            return 100.100
        }

        type Human struct {
            name string
            age int
        }

        func (h Human) getType() string {
            return "Humanity"
        }

        func (h Human) attack(h Human) boolean {
            return false
        }

        func (d Dog) attack(d Human) boolean {
            return true
        }

        func (h Human) getNumber() int {
            return 100
        }

        type Entity interface {
            getNumber() int
            getPower() float
        }

        func (h Human) getPower() float {
            return 50.50
        }

        type Animal interface {
            getType() string
        }

        type Shippou struct {
            name string
            age int
        }

        func (s Shippou) getYouki() float {
            return 50.0
        }

        type ShikonNoTama struct {
            name string
            kakera int
        }

        func (s ShikonNoTama) Kakera() int {
            return 100
        }

        func (h Human) Kill(people [4]People) boolean {
            return true
        }

        type Ackujin interface {
            Kill(people [3]People) boolean
        }

        type Youkai interface {
            getYouki() float
        }
        '''
        expect = '100'

        self.assertTrue(TestCodeGen.test(input, expect, 507))


    def test_508(self):
        input = \
            '''
            func main() {
                // var name String = getString()
                // putStringLn("Your name is: " + name)
                var a int = 10
                putInt(a)
                return
            }
            '''
        expect = '10'

        self.assertTrue(TestCodeGen.test(input, expect, 508))


    def test_509(self):
        input = \
        '''
        func main() {
            var a int = 10
            var b float = 3.14

            putFloatLn(a + b)
            return
        }
        '''
        expect = '13.14\n'

        self.assertTrue(TestCodeGen.test(input, expect, 509))


    def test_510(self):
        input = \
        '''
        func main() {
            var a = true
            var b = false
            var c = true
            putBool(a && b || c)
            return
        }
        '''
        expect = 'true'

        self.assertTrue(TestCodeGen.test(input, expect, 510))


    def test_511(self):
        input = \
        '''
        func main() {
            var result boolean = true && (false || false) && ((true && false) || false) && false
            putBoolLn(result)
            return
        }
        '''
        expect = 'false\n'


        self.assertTrue(TestCodeGen.test(input, expect, 511))


    def test_512(self):
        input = \
        '''
        func main() {
            var a int = 100
            var b = 100
            putIntLn(Add(a, b))
            putIntLn(Sub(a, b))
            putIntLn(Mul(a, b))
            putIntLn(Div(a, b))

            putString("End")

            return
        }

        func Add(a int, b int) int {
            return a + b
        }

        func Sub(a int, b int) int {
            return a - b
        }

        func Mul(a int, b int) int {
            return a * b
        }

        func Div(a int, b int) int {
            return a / b
        }
        '''
        expect = '200\n0\n10000\n1\nEnd'

        self.assertTrue(TestCodeGen.test(input, expect, 512))


    def test_513(self):
        input = \
            '''
            func main() {
                var h Human = Human{name : "Dung", age : 18}
                h.print()
                return
            }

            type Human struct {
                name string
                age int
            }

            func (h Human) print() {
                putStringLn(h.name)
                putIntLn(h.age)
                
                return
            }
            '''
        expect = 'Dung\n18\n'

        self.assertTrue(TestCodeGen.test(input, expect, 513))


    def test_514(self):
        input = \
        '''
        func main() {
            var father = Animal{name : "A", father : nil}
            var d = Animal{name : "B", father : father}

            var theFather = d.getFather()

            putStringLn(d.getFather().getName())
            return
        }

        type Animal struct {
            name string 
            father Animal
        }

        func (a Animal) getName() string {
            return a.name
        }

        func (a Animal) getFather() Animal {
            return a.father
        }
        '''

        expect = 'A\n'
        
        self.assertTrue(TestCodeGen.test(input, expect, 514))


    def test_515(self):
        input = \
        '''
        func main() {
            var animal Animal = Dog{}
            var animal1 Animal = Cat{name : "Tom"}
            putStringLn(animal.getType())
            putStringLn(animal1.getType())
            return
        }

        func (c Cat) getType() string {
            return "CAT"
        }

        type Cat struct {
            name string
        }

        type Dog struct {
            name string
        }

        func (d Dog) getType() string {
            return "DOG"
        }

        type Animal interface {
            getType() string
        }
        '''

        expect = 'DOG\nCAT\n'
        
        self.assertTrue(TestCodeGen.test(input, expect, 515))


    def test_516(self):
        input = \
        '''
        func main() {
            var a int = 100
            a := 2
            b := a + 2
            putIntLn(a + b)
            return
        }
        '''

        expect = '6\n'

        self.assertTrue(TestCodeGen.test(input, expect, 516))


    def test_517(self):
        input = \
        '''
        var GLOBAL int = 100
        func main() {
            a := 1 + 2
            b := 2 + 3.4
            c := "string" + "string"
            d := true && false
            GLOBAL := 200
            putIntLn(GLOBAL)
            return
        }
        '''

        expect = '200\n'

        self.assertTrue(TestCodeGen.test(input, expect, 517))


    def test_518(self):
        input = \
        '''
        func main() {
            a := 100
            b := 3.14
            c := a + b
            d := a % 3
            d += 4
            putInt(d)
            return
        }
        '''

        expect = '5'

        self.assertTrue(TestCodeGen.test(input, expect, 518))


    def test_519(self):
        input = \
        '''
        func main() {
            var w Weapon = Tessaiga{dam : 1000.0, special : 100}
            putFloatLn(w.getDamage())
            putIntLn(w.getSpecial())

            w := Tessaiga{dam : 999.9, special : 99}
            putFloatLn(w.getDamage())
            putIntLn(w.getSpecial())
            return
        }

        type Tessaiga struct {
            dam float
            special int
        }

        func (t Tessaiga) getDamage() float {
            return t.dam
        }

        func (t Tessaiga) getSpecial() int {
            return t.special
        }

        type Weapon interface {
            getDamage() float
            getSpecial() int
        }
        '''

        expect = '1000.0\n100\n999.9\n99\n'

        self.assertTrue(TestCodeGen.test(input, expect, 519))


    def test_520(self):
        input = \
        '''
        var GLOBAL float;
        func main() {
            var a float = 10;
            putFloat(a)
            a := 20
            putFloat(a)

            GLOBAL := 200
            putFloatLn(GLOBAL)
            return
        }
        '''

        expect = '10.020.0200.0\n'

        self.assertTrue(TestCodeGen.test(input, expect, 520))


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


    def test_524(self):
        input = \
        '''
        func main() {
            var a [4]int = [4]int{1, 2, 3, 4}
            var result = a[2]
            putIntLn(result)
            return
        }
        '''

        expect = '3\n'

        self.assertTrue(TestCodeGen.test(input, expect, 524))


    def test_525(self):
        input = \
        '''
        func main() {
            a := [3][3]float {{1.0, 2.0, 3.0}, {1.0, 2.0, 3.0}, {1.0, 2.0, 3.0}}
            putFloatLn(a[1][1])
            return
        }
        '''

        expect = '2.0\n'

        self.assertTrue(TestCodeGen.test(input, expect, 525))


    def test_526(self):
        input = \
        '''
        func main() {
            ARRAY := [3][3]float {{1.0, 2.0, 3.0}, {1.0, 2.0, 3.0}, {1.0, 2.0, 3.0}}
            putFloatLn(ARRAY[2][2])
            return
        }
        '''

        expect = '3.0\n'

        self.assertTrue(TestCodeGen.test(input, expect, 526))


    def test_527(self):
        input = \
        '''
        func main() {
            var people [4]Human = [4]Human{ Human{name : "Zun"}, Human{name : "Zun"}, Human{name : "Zun"}, Human{name : "Zun"} }
            people[0] := people[1]
            people[1].name := "Changed"

            people[0] := Human{}
            people[0].name := "Kiky"
            people[0].name += "o"


            putStringLn(people[0].name)
            return
        }

        type Human struct {
            name string
        }
        '''

        expect = 'Kikyo\n'

        self.assertTrue(TestCodeGen.test(input, expect, 527))


    def test_528(self):
        input = \
        '''
        func main() {
            var youkai [2]Youkai
            youkai[0] := Naraku{damage : 100}
            youkai[1] := Jaken{damage : 50}

            // putIntLn(youkai[0].damage)

            putInt(youkai[0].attack(youkai[1]))

            return
        }

        type Naraku struct {
            damage int
        }

        type Jaken struct {
            damage int
        }

        func (j Jaken) attack(y Youkai) int {
            return 20
        }

        func (n Naraku) attack(y Youkai) int {
            return 1000
        }

        type Youkai interface {
            attack(y Youkai) int
        }
        '''

        expect = '1000'

        self.assertTrue(TestCodeGen.test(input, expect, 528))


    def test_529(self):
        input = \
        '''
        func main() {
            var arr [5][5]int
            arr[0][0] := 100
            arr[4][4] := 500

            arr[2][2] := arr[0][0] + arr[4][4]
            putInt(arr[2][2])

            var index = 2
            arr[2-1*2][4-3] := 99

            putInt(arr[0][1])
            return
        }
        '''

        expect = '60099'

        self.assertTrue(TestCodeGen.test(input, expect, 529))


    def test_530(self):
        input = \
        '''
        func main() {
            var arr [4]string
            arr[0] := "This"
            arr[1] := " is"
            arr[2] := " a"
            arr[3] := " string"

            putStringLn(arr[0] + arr[1] + arr[2] + arr[3])
            return
        }

        func getRandom(seed int) int {
            return ((seed*2)-(seed*3))%(seed-44)*(22)-(43 * 23)
        }
        '''

        expect = 'This is a string\n'

        self.assertTrue(TestCodeGen.test(input, expect, 530))


    def test_531(self):
        input = \
        '''
        func main() {
            var demons [2]Youkai

            demons[0] := Naraku{damage: 999}
            demons[1] := Jaken{damage: 1}

            // change damage using method call
            demons[1] := demons[1].evolve(10)

            putIntLn(demons[0].attack(demons[1]))  // Expect 9990
            // putIntLn(demons[1].damage)             // Expect 11

            var names [3]string
            names[0] := "Inu"
            names[1] := "Yasha"
            names[2] := "!"

            putStringLn(names[0] + names[1] + names[2]) // InuYasha!

            var grid [2][2]int
            grid[1][1] := 100
            grid[0][0] := 50
            putIntLn(grid[0][0] + grid[1][1]) // 150

            return
        }

        type Youkai interface {
            attack(y Youkai) int
            evolve(amount int) Youkai
        }

        type Naraku struct {
            damage int
        }

        type Jaken struct {
            damage int
        }

        func (n Naraku) attack(y Youkai) int {
            return n.damage * 10
        }

        func (n Naraku) evolve(a int) Youkai {
            return Naraku{damage: n.damage + a}
        }

        func (j Jaken) attack(y Youkai) int {
            return j.damage * 2
        }

        func (j Jaken) evolve(a int) Youkai {
            return Jaken{damage: j.damage + a}
        }
        '''

        expect = '9990\nInuYasha!\n150\n'

        self.assertTrue(TestCodeGen.test(input, expect, 531))


    def test_532(self):
        input = \
        '''
        func main() {
            var w Weapon = Tenseiga{dam: 888.8, heal: 42}
            putFloatLn(w.getDamage())    // 888.8
            putIntLn(w.getSpecial())     // 42

            w := Bakusaiga{dam: 1000.5, poison: 3}
            putFloatLn(w.getDamage())    // 1000.5
            putIntLn(w.getSpecial())     // 300

            // Struct-specific method not in interface
            var b Bakusaiga = Bakusaiga{dam: 900.0, poison: 4}
            putFloatLn(b.getPoisonedDamage()) // 3600.0

            return
        }

        type Tenseiga struct {
            dam float
            heal int
        }

        func (t Tenseiga) getDamage() float {
            return t.dam
        }

        func (t Tenseiga) getSpecial() int {
            return t.heal
        }

        type Bakusaiga struct {
            dam float
            poison int
        }

        func (b Bakusaiga) getDamage() float {
            return b.dam
        }

        func (b Bakusaiga) getSpecial() int {
            return b.poison * 100
        }

        func (b Bakusaiga) getPoisonedDamage() float {
            var poison float = b.poison
            return b.dam * poison
        }

        type Weapon interface {
            getDamage() float
            getSpecial() int
        }
        '''

        expect = '888.8\n42\n1000.5\n300\n3600.0\n'

        self.assertTrue(TestCodeGen.test(input, expect, 532))



    def test_533(self):
        input = \
        '''
        func main() {
            const a = 100
            const b = 200
            var a int = ((a + b)/3)%2
            putInt(a)
            return
        }
        '''

        expect = '0'

        self.assertTrue(TestCodeGen.test(input, expect, 533))


    def test_534(self):
        input = \
        '''
        var a int = 100
        const PI = 3.14
        var seed int = 2
        const NAME = "NAME"
        var value = getRan(seed)


        func main() {
            putInt(a)
            putFloat(PI)
            return
        }

        func getRan(seed int) int {
            return (100*6)*seed%(seed-400)
        }
        '''

        expect = '1003.14'

        self.assertTrue(TestCodeGen.test(input, expect, 534))


    def test_535(self):
        input = \
        '''
        var a int = getInt1()
        var b float = getFloat1()
        const C = a + b
        const D = C + 13.2

        func getInt1() int {
            return 5
        }

        func getFloat1() float {
            return 3 - 5 + 10 - 5.0
        }

        func main() {
            a := 99
            b := 100.0
            putInt(a)
            putFloat(b)
            putFloat(C)
            putFloat(D)
            return
        }
        '''

        expect = '99100.08.021.2'

        self.assertTrue(TestCodeGen.test(input, expect, 535))


    def test_536(self):
        input = \
        '''
        var a = GetShikonNoTama()

        func main() {
            putInt(a.youryoku)
            a.youryoku += 100
            putInt(a.youryoku)

            Run()

            return
        }

        func Run() {
            var a = 100
            var b = 200
            var c = a + b

            var arr = [5]int{1, 2, 3, 4, 5}
            arr[0] := a
            arr[1] := b
            arr[2] := c
            putInt(arr[0] + arr[1] + arr[2])
        }

        func GetShikonNoTama() ShikonNoTama {
            return ShikonNoTama{youryoku : 100}
        }

        type ShikonNoTama struct {
            youryoku int
        }
        '''

        expect = '100200600'

        self.assertTrue(TestCodeGen.test(input, expect, 536))


    def test_537(self):
        input = \
        '''
        func main() {
            var a boolean = ( true && false ) || false && false && (false || false && true)

            if (!a) {
                putStringLn("false")
            }

            var a int = 100

            if (a == (100 + 100 - 100)) {
                putStringLn("Value a = 100")
            }

            return
        }
        '''

        expect = 'false\nValue a = 100\n'

        self.assertTrue(TestCodeGen.test(input, expect, 537))


    def test_538(self):
        input = \
        '''
        func main() {
            var a int = 50
            if (a > 1) {
                putInt(a)
            }
            return
        }
        '''

        expect = '50'

        self.assertTrue(TestCodeGen.test(input, expect, 538))


    def test_539(self):
        input = \
        '''
        func returnInt() int {
            // var a int = getInt()
            return 100
        }

        func main() {
            var a int = returnInt()
            if (a < 100) {
                putStringLn("<100")
            } else if (a == 100) {
                putStringLn("==100")
            } else if (a > 100) {
                putStringLn(">100")
            } else {
                putStringLn("else")
            }
            return
        }
        '''

        expect = '==100\n'

        self.assertTrue(TestCodeGen.test(input, expect, 539))


    def test_540(self):
        input = \
        '''
        func main() {
            var a int = 100
            if (a == 100) {
                var b int = 200
                a := b
            }

            putIntLn(a)
            return
        }
        '''

        expect = '200\n'

        self.assertTrue(TestCodeGen.test(input, expect, 540))


    def test_541(self):
        input = \
        '''
        func main() {
            var score int = 85
            var grade string

            if (score >= 90) {
                grade := "A"
                putStringLn(grade)
            } else if (score >= 80) {
                grade := "B"
                putStringLn(grade)
            } else if (score >= 70) {
                grade := "C"
                putStringLn(grade)
            } else {
                grade := "F"
                putStringLn(grade)
            }

            // Confirm outer variable remains unaffected
            putStringLn(grade)

            return
        }
        '''
        expect = 'B\nB\n'
        self.assertTrue(TestCodeGen.test(input, expect, 541))


    def test_542(self):
        input = \
        '''
        func main() {
            var x int = 10
            var y int = 20
            var result string

            if (x + y > 25) {
                if (y - x == 10) {
                    result := "Perfect match"
                    putStringLn(result)
                } else {
                    result := "Close"
                    putStringLn(result)
                }
            } else {
                result := "Too small"
                putStringLn(result)
            }

            putIntLn(x + y)

            var condition boolean = true
            if (condition) {
                var status Status = Status{ok: true}
                if (status.ok) {
                    putStringLn("Status OK")
                }
            }

            return
        }

        type Status struct {
            ok boolean
        }
        '''

        expect = 'Perfect match\n30\nStatus OK\n'

        self.assertTrue(TestCodeGen.test(input, expect, 542))


    def test_543(self):
        input = \
        '''
        func main() {
            var a int = 5
            var b int = 10
            var msg string = ""

            if (a < b) {
                if (b - a > 3) {
                    if ((a * 2) == b) {
                        msg := "Deep Match"
                        putStringLn(msg)
                    } else {
                        msg := "Level 3 mismatch"
                        putStringLn(msg)
                    }
                } else {
                    msg := "Level 2 condition failed"
                    putStringLn(msg)
                }
            } else {
                msg := "Top-level condition failed"
                putStringLn(msg)
            }

            putStringLn("Done")
            return
        }
        '''

        expect = 'Deep Match\nDone\n'

        self.assertTrue(TestCodeGen.test(input, expect, 543))


    def test_544(self):
        input = \
        '''
        func main() {
            var a int = 0
            var sum int = 0
            for (a <= 100) {
                sum := sum + a
                a += 1
            }

            putInt(sum)
            return
        }
        '''

        expect = '5050'

        self.assertTrue(TestCodeGen.test(input, expect, 544))


    def test_545(self):
        input = \
        '''
        func main() {
            var arr [3][3]int = [3][3]int{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
            i := 0

            sum := 0
            for (i < 3) {
                j := 0
                for (j < 3) {
                    sum += arr[i][j]
                    j += 1
                }
                i += 1
            }

            putInt(sum)
            return
        }
        '''

        expect = '45'

        self.assertTrue(TestCodeGen.test(input, expect, 545))

    
    def test_546(self):
        input = \
        '''
        func main() {
            var arr [10]int = [10]int{10, 9, 8, 7, 6, 5, 4, 3, 2, 1}
            const len = 10

            i := 0
            for (i < len - 1) {
                j := i + 1
                for (j < len) {
                    if (arr[j] < arr[i]) {
                        // find new min, swap
                        temp := arr[i]
                        arr[i] := arr[j]
                        arr[j] := temp
                    }
                    j += 1
                }
                i += 1
            }

            PrintArray(arr, len)
            return
        }

        func PrintArray(arr [10]int, len int) {
            i := 0
            for (i < len) {
                putInt(arr[i])
                putString(" ")
                i += 1
            }
        }
        '''

        expect = '1 2 3 4 5 6 7 8 9 10 '

        self.assertTrue(TestCodeGen.test(input, expect, 546))


    def test_547(self):
        input = \
        '''
        func main() {
            var matrix [3][3]int = [3][3]int{ {2, 4, 6}, {1, 3, 5}, {7, 9, 11}}

            sum_main := 0
            sum_anti := 0

            i := 0
            for (i < 3) {
                sum_main += matrix[i][i]                  // main diagonal
                sum_anti += matrix[i][2 - i]              // anti-diagonal
                i += 1
            }

            putString("Main Diagonal Sum: ")
            putInt(sum_main)
            putString("\\n")

            putString("Anti Diagonal Sum: ")
            putInt(sum_anti)
            putString("\\n")

            return
        }
        '''

        expect = "Main Diagonal Sum: 16\nAnti Diagonal Sum: 16\n"

        self.assertTrue(TestCodeGen.test(input, expect, 547))


    def test_548(self):
        input = \
        '''
        func main() {
            var arr [6]int = [6]int{10 , 8 ,2, 3, 1, 2}
            const len = 6

            mergeSort(arr, 0, len - 1)

            printArray(arr, len)
            return
        }

        func mergeSort(arr [6]int, left int, right int) {
            if (left < right) {
                mid := (left + right) / 2

                mergeSort(arr, left, mid)
                mergeSort(arr, mid + 1, right)
                merge(arr, left, mid, right)
            }
        }

        func merge(arr [6]int, left int, mid int, right int) {
            n1 := mid - left + 1
            n2 := right - mid

            var L [3]int
            var R [3]int

            i := 0
            for (i < n1) {
                L[i] := arr[left + i]
                i += 1
            }

            j := 0
            for (j < n2) {
                R[j] := arr[mid + 1 + j]
                j += 1
            }

            i := 0
            j := 0
            k := left

            for (i < n1 && j < n2) {
                if (L[i] <= R[j]) {
                    arr[k] := L[i]
                    i += 1
                } else {
                    arr[k] := R[j]
                    j += 1
                }
                k += 1
            }

            for (i < n1) {
                arr[k] := L[i]
                i += 1
                k += 1
            }

            for (j < n2) {
                arr[k] := R[j]
                j += 1
                k += 1
            }
        }

        func printArray(arr [6]int, len int) {
            i := 0
            for (i < len) {
                putInt(arr[i])
                putString(" ")
                i += 1
            }
        }
        '''

        expect = "1 2 2 3 8 10 "

        self.assertTrue(TestCodeGen.test(input, expect, 548))


    def test_549(self):
        input = \
        '''
        func main() {
            i := 0
            for (i < 10) {
                i += 1
                if (i % 2 == 0) {
                    continue
                }
                putInt(i)
                putString(" ")
            }
        }
        '''

        expect = "1 3 5 7 9 "

        self.assertTrue(TestCodeGen.test(input, expect, 549))


    def test_550(self):
        input = \
        '''
        func main() {
            i := 1
            sum := 0
            for (i <= 10) {
                if (i > 5) {
                    break
                }
                sum += i
                i += 1
            }
            putString("Sum till 5: ")
            putInt(sum)
        }
        '''

        expect = "Sum till 5: 15"

        self.assertTrue(TestCodeGen.test(input, expect, 550))


    def test_551(self):
        input = \
        '''
        func main() {
            Print(50)
        }

        func Print(value int) {
            i := 0
            for (i < value) {
                i += 1
                if ( i % 2 == 0) {
                    continue
                } else if (i == 9) {
                    putString("Invalid")
                } else if ( i == 20) {
                    break
                } else {
                    putInt(i)
                }
            }
        }
        '''

        expect = '1357Invalid1113151719212325272931333537394143454749'

        self.assertTrue(TestCodeGen.test(input, expect, 551))


    def test_551(self):
        input = \
        '''
        func main() {
            for i := 0 ; i < 10 ; i += 1 {
                putInt(i)
            }
            return
        }
        '''

        expect = '0123456789'

        self.assertTrue(TestCodeGen.test(input, expect, 551))


    def test_552(self):
        input = \
        '''
        const LEN = 10
        func main() {
            arr := [LEN]int {9, 2, 3, 4, 5, 6, 100, 8, 9, 777}
            putInt(Max(arr, LEN))
            return
        }

        func Max(arr [10]int, len int) int {
            var i int = 0
            max := arr[0]
            for i := 0 ; i < LEN ; i += 1 {
                if (arr[i] >= max) {
                    max := arr[i]
                }
            }
            return max
        }
        '''

        expect = '777'

        self.assertTrue(TestCodeGen.test(input, expect, 552))


    def test_553(self):
        input = \
        '''
        func main() {
            for i := 9 ; i >= 0 ; i -= 1 {
                if (i == 5) {
                    break
                }
                putInt(i)
            }
        }
        '''
        # Expect output: 9876 (stops before printing 5)
        expect = '9876'
        self.assertTrue(TestCodeGen.test(input, expect, 553))



    def test_554(self):
        input = \
        '''
        func main() {
            sum := 0
            for i := 0 ; i < 10 ; i += 1 {
                if (i % 3 != 0) {
                    continue
                }
                sum += i
            }
            putInt(sum)
        }
        '''
        # 0 + 3 + 6 + 9 = 18
        expect = '18'
        self.assertTrue(TestCodeGen.test(input, expect, 554))


    def test_555(self):
        input = \
        '''
        func main() {
            var a int = 0
            var b int = 1
            putInt(a)
            putString(" ")
            putInt(b)
            putString(" ")

            for i := 2 ; i < 7 ; i += 1 {
                c := a + b
                putInt(c)
                putString(" ")
                a := b
                b := c
            }
        }
        '''
        # Fibonacci sequence: 0 1 1 2 3 5 8
        expect = '0 1 1 2 3 5 8 '
        self.assertTrue(TestCodeGen.test(input, expect, 555))


    def test_556(self):
        input = \
        '''
        func main() {
            // Test array of structs with interface and method calls
            var vehicles [3]Vehicle = [3]Vehicle{Car{speed: 120, model: "Sedan"}, Bike{speed: 30, brand: "Mountain"}, Truck{speed: 80, capacity: 5000}}

            // Print all vehicle info
            i := 0
            for (i < 3) {
                putStringLn(vehicles[i].getInfo())
                i += 1
            }

            // Find fastest vehicle
            fastest := vehicles[0]
            j := 1
            for (j < 3) {
                if (vehicles[j].getSpeed() > fastest.getSpeed()) {
                    fastest := vehicles[j]
                }
                j += 1
            }
            putString("Fastest: ")
            putStringLn(fastest.getModel())
            return
        }

        type Car struct {
            speed int
            model string
        }

        type Bike struct {
            speed int
            brand string
        }

        type Truck struct {
            speed int
            capacity int
        }

        func (c Car) getInfo() string {
            return "Car: " + c.model + ", speed: " + "1"
        }

        func (b Bike) getInfo() string {
            return "Bike: " + b.brand + ", speed: " + "1"
        }

        func (t Truck) getInfo() string {
            return "Truck: capacity " + "1" + ", speed: " + "1"
        }

        func (c Car) getSpeed() int {
            return c.speed
        }

        func (b Bike) getSpeed() int {
            return b.speed
        }

        func (t Truck) getSpeed() int {
            return t.speed
        }

        func (c Car) getModel() string {
            return c.model
        }

        func (b Bike) getModel() string {
            return b.brand
        }

        func (t Truck) getModel() string {
            return "Truck"
        }

        type Vehicle interface {
            getInfo() string
            getSpeed() int
            getModel() string
        }
        '''

        expect = '''Car: Sedan, speed: 1\nBike: Mountain, speed: 1\nTruck: capacity 1, speed: 1\nFastest: Sedan\n'''
        self.assertTrue(TestCodeGen.test(input, expect, 556))


    def test_557(self):
        input = \
        '''
        func main() {
            putInt(Fibonancci(19))
        }

        func Fibonancci(a int) int {
            if (a == 0) {
                return 0
            } else if (a == 1) {
                return 1
            } else {
                return Fibonancci(a - 1) + Fibonancci(a - 2)
            }
        }
        '''

        expect = '4181'

        self.assertTrue(TestCodeGen.test(input, expect, 557))


    def test_557(self):
        input = \
        '''
        func main() {
            var x boolean = true
            var y boolean = false
            var result boolean = (x && !y) || (!x && y)
            if (result) {
                putStringLn("Complex logic passed")
            }
            return
        }
        '''
        expect = 'Complex logic passed\n'
        self.assertTrue(TestCodeGen.test(input, expect, 557))


    def test_558(self):
        input = \
        '''
        var globalInt int = 10
        var globalStr string = "MiniGo"
        const PI = 3.14
        const AUTHOR = "CompilerBot"

        func getGlobalInt() int {
            return globalInt
        }

        func getPI() float {
            return PI
        }

        func main() {
            putIntLn(globalInt)
            putStringLn(globalStr)
            putFloatLn(PI)
            putStringLn(AUTHOR)

            globalInt := getGlobalInt() + 5
            putIntLn(globalInt)

            result := getPI() * 2
            putFloatLn(result)

            return
        }
        '''
        expect = '10\nMiniGo\n3.14\nCompilerBot\n15\n6.28\n'
        self.assertTrue(TestCodeGen.test(input, expect, 558))


    def test_559(self):
        input = \
        '''
        type Student struct {
            name string
            age int
            gpa float
        }

        var defaultStudent = Student{name: "Alice", age: 20, gpa: 3.5}

        func main() {
            putStringLn(defaultStudent.name)
            putIntLn(defaultStudent.age)
            putFloatLn(defaultStudent.gpa)

            defaultStudent := UpdateStudent(defaultStudent)
            putStringLn(defaultStudent.name)
            putIntLn(defaultStudent.age)
            putFloatLn(defaultStudent.gpa)

            return
        }

        func UpdateStudent(s Student) Student {
            s.name := "Bob"
            s.age := s.age + 1
            s.gpa := 3.9
            return s
        }
        '''
        expect = 'Alice\n20\n3.5\nBob\n21\n3.9\n'
        self.assertTrue(TestCodeGen.test(input, expect, 559))


    def test_560(self):
        input = \
        '''
        type Speaker interface {
            speak() string
        }

        type Person struct {
            name string
        }

        type Robot struct {
            model string
        }

        var p = Person{name: "John"}
        var r = Robot{model: "R2D2"}

        func main() {
            putStringLn(p.speak())  // John says hello
            putStringLn(r.speak())  // R2D2 says beep boop

            return
        }

        func (p Person) speak() string {
            return p.name + " says hello"
        }

        func (r Robot) speak() string {
            return r.model + " says beep boop"
        }
        '''
        expect = 'John says hello\nR2D2 says beep boop\n'
        self.assertTrue(TestCodeGen.test(input, expect, 560))


    def test_561(self):
        input = \
        '''
        func main() {
            var arr [5]int = [5]int{1, 2, 3, 4, 5}

            // Update array
            arr[0] := arr[1] + arr[2]    // arr[0] = 2 + 3 = 5
            arr[3] := arr[0] * 2         // arr[3] = 5 * 2 = 10
            arr[4] := arr[3] - arr[2]    // arr[4] = 10 - 3 = 7

            var sum int = 0
            i := 0
            for (i < 5) {
                sum += arr[i]
                i += 1
            }

            putIntLn(sum)  // Expected: 5 + 2 + 3 + 10 + 7 = 27
            return
        }
        '''
        expect = '27\n'
        self.assertTrue(TestCodeGen.test(input, expect, 561))


    def test_562(self):
        input = \
        '''
        type Person struct {
            name string
            age int
        }

        func main() {
            // Struct literal initialization
            var p Person = Person{name: "Alice", age: 25}
            
            putString(p.name)
            putString(" is ")
            putInt(p.age)
            putStringLn(" years old")

            // Update fields
            p.name := "Bob"
            p.age := p.age + 5

            putString(p.name)
            putString(" is now ")
            putInt(p.age)
            putStringLn(" years old")
            return
        }
        '''
        expect = 'Alice is 25 years old\nBob is now 30 years old\n'
        self.assertTrue(TestCodeGen.test(input, expect, 562))


    def test_563(self):
        input = \
        '''
        var x int = 10       // Global variable
        var msg string = "Global"

        func main() {
            putIntLn(x)       // 10
            putStringLn(msg)  // Global

            x := 20           // Shadows global x
            msg := "Local"    // Shadows global msg

            putIntLn(x)       // 20
            putStringLn(msg)  // Local

            if (true) {
                x := 30       // New block scope, shadows previous x
                putIntLn(x)   // 30
            }

            putIntLn(x)       // 20 (previous block x is gone)
            putStringLn(msg)  // Local

            callFunc()

            return
        }

        func callFunc() {
            putIntLn(x)       // 10 (global x is still accessible)
            putStringLn(msg)  // Global (global msg is still accessible)
        }
        '''
        expect = '10\nGlobal\n20\nLocal\n30\n30\nLocal\n30\nLocal\n'
        self.assertTrue(TestCodeGen.test(input, expect, 563))


    def test_struct_interface_564(self):
        input = '''
        type Animal interface {
            Speak() string
        }

        type Dog struct {
            name string
        }

        func NewDog(n string) Dog {
            var d Dog = Dog{}
            d.name := n
            return d
        }

        func (d Dog) Speak() string {
            return "Woof from " + d.name
        }

        func Talk(a Animal) {
            putStringLn(a.Speak())
        }

        func main() {
            var dog Dog = NewDog("Buddy")
            Talk(dog)
            return
        }
        '''

        expect = 'Woof from Buddy\n'

        self.assertTrue(TestCodeGen.test(input, expect, 564))


    def test_565_function_calls_method(self):
        input = '''
        type Person struct {
            name string
        }

        func (p Person) Greet() string {
            return "Hello, " + p.name
        }

        func greetPerson(p Person) {
            msg := p.Greet()
            putStringLn(msg)
        }

        func NewPerson(n string) Person {
            var p Person = Person{}
            p.name := n
            return p
        }

        func main() {
            person := NewPerson("Alice")
            greetPerson(person)
            return
        }
        '''
        expect = 'Hello, Alice\n'
        self.assertTrue(TestCodeGen.test(input, expect, 565))


    def test_566_deeply_nested_calls(self):
        input = '''
        type Calc struct {
            base int
        }

        func (c Calc) Add(x int) int {
            return c.base + x
        }

        func (c Calc) Mul(x int) int {
            return c.base * x
        }

        func NewCalc(b int) Calc {
            var c Calc = Calc{}
            c.base := b
            return c
        }

        func main() {
            calc := NewCalc(3)
            result := calc.Add(calc.Mul(4)) // 3 + (3 * 4) = 3 + 12 = 15
            putInt(result)
            return
        }
        '''
        expect = '15'
        self.assertTrue(TestCodeGen.test(input, expect, 566))


    def test_567_basic_io(self):
        input = '''
        func main() {
            putInt(123)
            putFloatLn(456.789)
            putBoolLn(true)
            putStringLn("Hello, MiniGo!")
            putLn()
            return
        }
        '''
        expect = '123456.789\ntrue\nHello, MiniGo!\n\n'
        self.assertTrue(TestCodeGen.test(input, expect, 567))



    def test_568_complex_condition(self):
        input = '''
        func main() {
            var x int = 5
            var y int = 10
            var z int = 15

            if ((x < y) && (z > y) || (x == 5)) {
                putStringLn("Condition true")
            }
            return
        }
        '''
        expect = 'Condition true\n'
        self.assertTrue(TestCodeGen.test(input, expect, 568))


    def test_628_all_else_paths(self):
        input = '''
        func main() {
            var a int = 100
            var b int = 50

            if (a < b) {
                putStringLn("Branch 1")
            } else {
                if (a == b) {
                    putStringLn("Branch 2")
                } else {
                    if (a > b) {
                        putStringLn("Branch 3")
                    } else {
                        putStringLn("Default")
                    }
                }
            }

            return
        }
        '''
        expect = 'Branch 3\n'
        self.assertTrue(TestCodeGen.test(input, expect, 569))


    def test_633_const_in_multiple_funcs(self):
        input = '''
        const greeting = "Hello, MiniGo!"

        func sayHello() {
            putStringLn(greeting)
        }

        func main() {
            sayHello()
            putStringLn(greeting)
            return
        }
        '''
        expect = 'Hello, MiniGo!\nHello, MiniGo!\n'
        self.assertTrue(TestCodeGen.test(input, expect, 570))


    def test_632_update_global_var(self):
        input = '''
        var counter int = 0

        func increment() {
            counter := counter + 1
            putIntLn(counter)
        }

        func main() {
            increment()
            increment()
            increment()
            return
        }
        '''
        expect = '1\n2\n3\n'
        self.assertTrue(TestCodeGen.test(input, expect, 571))


    def test_572_input_output(self):
        input = '''
        func main() {
            // var a = getInt()
            // var b = getFloat()
            // var c = getBool()
            // var d = getString()
            a := 100
            b := 3.14
            c := true
            d := "Zun"
            putInt(a)
            putFloat(b)
            putBool(c)
            putString(d)
            putLn()
        }
        '''
        expect = '1003.14trueZun\n'
        self.assertTrue(TestCodeGen.test(input, expect, 572))


    def test_639_boolean_assignment(self):
        input = '''
        func main() {
            var flag boolean = true
            putBoolLn(flag)
            flag := false
            putBoolLn(flag)
            return
        }
        '''
        expect = 'true\nfalse\n'
        self.assertTrue(TestCodeGen.test(input, expect, 573))


    def test_638_assign_func_return(self):
        input = '''
        func getValue() int {
            return 42
        }

        func main() {
            var a int
            a := getValue()
            putIntLn(a)
            return
        }
        '''
        expect = '42\n'
        self.assertTrue(TestCodeGen.test(input, expect, 574))


    def test_643_struct_field_assignment_with_expression(self):
        input = '''
        type Rectangle struct {
            width  int
            height int
        }

        func main() {
            var r Rectangle = Rectangle{}
            r.width := 5
            r.height := r.width * 2
            putIntLn(r.height)  // should be 10
            return
        }
        '''
        expect = '10\n'  # height = width * 2 = 5 * 2 = 10
        self.assertTrue(TestCodeGen.test(input, expect, 575))


    def test_658_for_loop_with_early_exit(self):
        input = '''
        func main() {
            var sum int = 0
            for var i int = 1; i <= 5; i := i + 1 {
                if (i == 3) {
                    break
                }
                sum := sum + i
            }
            putIntLn(sum)
            return
        }
        '''
        expect = '3\n'  # sum = 1 + 2 = 3, loop breaks before adding 3
        self.assertTrue(TestCodeGen.test(input, expect, 576))


    def test_657_for_loop_with_init_conditional_multiple_statements(self):
        input = '''
        func main() {
            var result int = 0
            for var i int = 1; i <= 3; i := i + 1 {
                if (i == 2) {
                    result := result + 10
                } else {
                    result := result + 5
                }
            }
            putIntLn(result)
            return
        }
        '''
        expect = '20\n'  # result = 5 + 10 + 5 = 20
        self.assertTrue(TestCodeGen.test(input, expect, 577))


    def test_665_array_of_objects_loop(self):
        input = '''
        type Student struct {
            name string
            grade int
        }

        func main() {
            var students [3]Student
            students[0] := Student{name: "Tom", grade: 85}
            students[1] := Student{name: "Jerry", grade: 90}
            students[2] := Student{name: "Spike", grade: 80}

            var i int
            for i := 0; i < 3; i := i + 1 {
                putStringLn(students[i].name)
                putIntLn(students[i].grade)
            }

            return
        }
        '''
        expect = 'Tom\n85\nJerry\n90\nSpike\n80\n'
        self.assertTrue(TestCodeGen.test(input, expect, 578))


    def test_664_array_of_objects_with_dynamic_assignment(self):
        input = '''
        type Product struct {
            name string
            price float
        }

        func main() {
            var products [2]Product
            var product1 Product
            product1 := Product{name: "Laptop", price: 999.99}
            products[0] := product1
            products[1] := Product{name: "Phone", price: 699.99}

            putStringLn(products[0].name)
            putFloatLn(products[0].price)
            putStringLn(products[1].name)
            putFloatLn(products[1].price)

            return
        }
        '''
        expect = 'Laptop\n999.99\nPhone\n699.99\n'
        self.assertTrue(TestCodeGen.test(input, expect, 579))


    def test_663_array_of_objects_with_methods(self):
        input = '''
        type Person struct {
            name string
            age int
        }

        func (p Person) greet() string {
            return "Hello, my name is " + p.name
        }

        func main() {
            var people [2]Person
            people[0] := Person{name: "Alice", age: 25}
            people[1] := Person{name: "Bob", age: 30}

            putStringLn(people[0].greet())
            putStringLn(people[1].greet())

            return
        }
        '''
        expect = 'Hello, my name is Alice\nHello, my name is Bob\n'
        self.assertTrue(TestCodeGen.test(input, expect, 580))


    def test_700_general_purpose_program(self):
        input = '''
        type Person struct {
            name string
            age int
        }

        type Product struct {
            name string
            price float
        }

        func (p Person) greet() string {
            return "Hello, my name is " + p.name
        }

        func (p Product) discount() float {
            return p.price * 0.1
        }

        func main() {
            // Array of Person objects
            var people [3]Person
            people[0] := Person{name: "Alice", age: 25}
            people[1] := Person{name: "Bob", age: 30}
            people[2] := Person{name: "Charlie", age: 35}

            // Greet each person
            var i int
            for i := 0; i < 3; i := i + 1 {
                putStringLn(people[i].greet())
            }

            // Array of Product objects
            var products [2]Product
            products[0] := Product{name: "Laptop", price: 999.99}
            products[1] := Product{name: "Smartphone", price: 699.99}

            // Apply discount on each product
            var j int
            for j := 0; j < 2; j := j + 1 {
                putStringLn(products[j].name)
                putFloatLn(products[j].discount())
            }

            // Modify one person's age and show updated info
            people[0].age := 26
            putStringLn("Updated Info:")
            putStringLn(people[0].name)
            putIntLn(people[0].age)

            // Show the total cost of all products after discount
            var totalCost float = 0.0
            for j := 0; j < 2; j := j + 1 {
                totalCost := totalCost + (products[j].price - products[j].discount())
            }
            putFloatLn(totalCost)

            return
        }
        '''
        expect = '''Hello, my name is Alice
Hello, my name is Bob
Hello, my name is Charlie
Laptop
99.999
Smartphone
69.999
Updated Info:
Alice
26
1529.9819
'''
        self.assertTrue(TestCodeGen.test(input, expect, 581))


    def test_801_complex_arithmetic_array(self):
        input = '''
        func main() {
            var arr [5]int
            arr[0] := 10
            arr[1] := 20
            arr[2] := 30
            arr[3] := 40
            arr[4] := 50

            var total int
            total := 0

            var i int
            for i := 0; i < 5; i := i + 1 {
                total := total + (arr[i] * 2) - (arr[i] / 2)
            }

            putStringLn("Total: ")
            putIntLn(total)

            return
        }
        '''
        expect = '''Total: \n225\n'''
        self.assertTrue(TestCodeGen.test(input, expect, 582))


    def test_802_nested_conditionals(self):
        input = '''
        func main() {
            var a int = 50
            var b int = 100
            var c int = 150
            var result string

            if (a > b && b < c) {
                result := "a is less than b and b is less than c"
            } else if (a == 50 || c == 150) {
                result := "a is 50 or c is 150"
            } else {
                result := "Condition not met"
            }

            putStringLn(result)
            return
        }
        '''
        expect = '''a is 50 or c is 150\n'''
        self.assertTrue(TestCodeGen.test(input, expect, 583))


    def test_803_method_call_complex_args(self):
        input = '''
        type Circle struct {
            radius float
        }

        func (c Circle) area() float {
            return 3.14 * c.radius * c.radius
        }

        func main() {
            var c Circle
            c := Circle{radius: 7}

            var result float
            result := c.area() + (c.area() / 2) - (3.14 * 2)

            putString("Complex calculation: ")
            putFloatLn(result)

            return
        }
        '''
        expect = '''Complex calculation: 224.51003
'''
        self.assertTrue(TestCodeGen.test(input, expect, 584))


    def test_804_complex_nested_loops(self):
        input = '''
        func main() {
            var arr1 [3]int
            var arr2 [3]int
            arr1[0] := 5
            arr1[1] := 10
            arr1[2] := 15

            arr2[0] := 20
            arr2[1] := 25
            arr2[2] := 30

            var sum int
            sum := 0

            var i int
            var j int
            for i := 0; i < 3; i := i + 1 {
                for j := 0; j < 3; j := j + 1 {
                    sum := sum + (arr1[i] * arr2[j]) + (arr1[i] / arr2[j])
                }
            }

            putStringLn("Final sum: ")
            putIntLn(sum)

            return
        }
        '''
        expect = '''Final sum: 
2250
'''
        self.assertTrue(TestCodeGen.test(input, expect, 585))


    def test_810_break_simple(self):
        input = '''
        func main() {
            var sum int
            sum := 0

            var i int
            for i := 0; i < 10; i := i + 1 {
                if (i == 5) {
                    break
                }
                sum := sum + i
            }

            putStringLn("Sum before break: ")
            putIntLn(sum)

            return
        }
        '''
        expect = '''Sum before break: \n10
'''
        self.assertTrue(TestCodeGen.test(input, expect, 586))


    def test_817_break_continue_nested_loops(self):
        input = '''
        func main() {
            var sum int
            sum := 0

            var i int
            var j int
            for i := 0; i < 5; i := i + 1 {
                for j := 0; j < 5; j := j + 1 {
                    if (i == 2 && j == 2) {
                        continue
                    }
                    if (i == 3 && j == 3) {
                        break
                    }
                    sum := sum + (i * j)
                }
            }

            putStringLn("Sum with break and continue in nested loops: ")
            putIntLn(sum)

            return
        }
        '''
        expect = '''Sum with break and continue in nested loops: \n75\n'''
        self.assertTrue(TestCodeGen.test(input, expect, 587))


    def test_830_recursive_function(self):
        input = '''
        func factorial(n int) int {
            if (n == 0) {
                return 1
            }
            return n * factorial(n - 1)
        }

        func main() {
            var result int
            result := factorial(5)
            putIntLn(result)
            return
        }
        '''
        expect = '''120
'''
        self.assertTrue(TestCodeGen.test(input, expect, 588))


    def test_828_function_multiple_returns(self):
        input = '''
        func checkNumber(a int) string {
            if (a > 0) {
                return "Positive"
            } else if (a < 0) {
                return "Negative"
            }
            return "Zero"
        }

        func main() {
            var result string
            result := checkNumber(10)
            putStringLn(result)
            
            result := checkNumber(5)
            putStringLn(result)
            
            result := checkNumber(0)
            putStringLn(result)
            
            return
        }
        '''
        expect = '''Positive
Positive
Zero
'''
        self.assertTrue(TestCodeGen.test(input, expect, 589))


    def test_827_nested_function_calls(self):
        input = '''
        func multiply(a int, b int) int {
            return a * b
        }

        func add(a int, b int) int {
            return a + b
        }

        func main() {
            var result int
            result := add(multiply(2, 3), multiply(4, 5))
            putIntLn(result)
            return
        }
        '''
        expect = '''26\n'''
        self.assertTrue(TestCodeGen.test(input, expect, 590))


    def test_843_function_call_with_complex_args(self):
        input = '''
        type Data struct {
            x int
            y int
        }

        func calculate(a int, b float, c boolean, msg string) {
            if (c) {
                putStringLn(msg)
            }
            putIntLn(a)
            putFloatLn(b)
        }

        func main() {
            var d Data = Data{}
            d.x := 10
            d.y := 5

            var flag boolean
            flag := (d.x > d.y) && !(d.x == 0)

            var message string
            message := "Complex Call"

            calculate((d.x + d.y * 2) - 3, 10.5 * 2.0 + 1.5, flag, message)

            return
        }
        '''
        expect = '''Complex Call
17
22.5
'''
        self.assertTrue(TestCodeGen.test(input, expect, 591))


    def test_842_compare_struct_fields(self):
        input = '''
        type Box struct {
            width int
            height int
        }

        func compareArea(a Box, b Box) {
            var area1 int
            var area2 int
            area1 := a.width * a.height
            area2 := b.width * b.height
            if (area1 > area2) {
                putStringLn("A is larger")
            } else {
                putStringLn("B is larger or equal")
            }
        }

        func main() {
            var b1 Box = Box{}
            var b2 Box = Box{}
            b1.width := 3
            b1.height := 4
            b2.width := 2
            b2.height := 8
            compareArea(b1, b2)
            return
        }
        '''
        expect = '''B is larger or equal
'''
        self.assertTrue(TestCodeGen.test(input, expect, 592))


    def test_841_sum_field_in_struct_array(self):
        input = '''
        type Item struct {
            price int
        }

        func total(items [3]Item) {
            var sum int
            sum := items[0].price + items[1].price + items[2].price
            putIntLn(sum)
        }

        func main() {
            var items [3]Item = [3]Item{Item{}, Item{}, Item{}}
            items[0].price := 10
            items[1].price := 15
            items[2].price := 20
            total(items)
            return
        }
        '''
        expect = '''45
'''
        self.assertTrue(TestCodeGen.test(input, expect, 593))


    def test_840_function_returns_struct(self):
        input = '''
        type Result struct {
            sum int
            product int
        }

        func compute(a int, b int) Result {
            var r Result = Result{}
            r.sum := a + b
            r.product := a * b
            return r
        }

        func main() {
            var r Result = Result{}
            r := compute(3, 4)
            putIntLn(r.sum)
            putIntLn(r.product)
            return
        }
        '''
        expect = '''7
12
'''
        self.assertTrue(TestCodeGen.test(input, expect, 594))


    def test_839_struct_containing_struct(self):
        input = '''
        type Address struct {
            city string
            zip int
        }

        type User struct {
            name string
            addr Address
        }

        func printUser(u User) {
            putStringLn(u.name)
            putStringLn(u.addr.city)
            putIntLn(u.addr.zip)
        }

        func main() {
            var u User = User{}
            d := Address{}
            u.addr := d
            u.name := "John"
            u.addr.city := "NYC"
            u.addr.zip := 10001
            printUser(u)
            return
        }
        '''
        expect = '''John
NYC
10001
'''
        self.assertTrue(TestCodeGen.test(input, expect, 595))


    def test_838_nested_array_in_struct_param(self):
        input = '''
        type Matrix struct {
            data [2][2]int
        }

        func printMatrix(m Matrix) {
            putIntLn(m.data[0][0])
            putIntLn(m.data[0][1])
            putIntLn(m.data[1][0])
            putIntLn(m.data[1][1])
        }

        func main() {
            var mat Matrix = Matrix{}
            var arr [2][2]int
            mat.data := arr
            mat.data[0][0] := 1
            mat.data[0][1] := 2
            mat.data[1][0] := 3
            mat.data[1][1] := 4
            printMatrix(mat)
            return
        }
        '''
        expect = '''1
2
3
4
'''
        self.assertTrue(TestCodeGen.test(input, expect, 596))


    def test_838_nested_array_in_str9uct_param(self):
        input = '''
        func main() {
            var arr [3][3]int = [3][3]int{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
            var arr1 = [3]int{1, 2, 3}
            var arr2 = [3]int{4, 5, 6}
            var arr3 = [3]int{7, 8, 9}

            arr[0] := arr1
            arr[1] := arr2
            arr[2] := arr3

            putInt(arr[2][2])
        }
        '''
        expect = '''9'''
        self.assertTrue(TestCodeGen.test(input, expect, 597))


    def test_847_nested_function_calls(self):
        input = '''
        func double(n int) int {
            return n * 2
        }

        func add(a int, b int) int {
            return a + b
        }

        func main() {
            var result int
            result := add(double(3), double(4))  // (6 + 8)

            putIntLn(result)
            return
        }
        '''
        expect = '14\n'
        self.assertTrue(TestCodeGen.test(input, expect, 598))


    def test_846_struct_implements_interface(self):
        input = '''
        type Speaker interface {
            speak() string
        }

        type Dog struct {
            name string
        }

        func (d Dog) speak() string {
            return d.name
        }

        func main() {
            var dog Dog = Dog{}
            dog.name := "Bark"

            var s Speaker = dog

            putStringLn(s.speak())
            return
        }
        '''
        expect = 'Bark\n'
        self.assertTrue(TestCodeGen.test(input, expect, 599))


    def test_845_loop_with_break_continue(self):
        input = '''
        func main() {
            var i int
            for i := 0; i < 10; i := i + 1 {
                if (i == 3) {
                    continue
                }
                if (i == 6) {
                    break
                }
                putInt(i)
            }
            return
        }
        '''
        expect = '01245'
        self.assertTrue(TestCodeGen.test(input, expect, 600))