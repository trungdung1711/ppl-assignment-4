### Instructions

1. Navigate to the `initial/src` directory where the `run.py` file is located.
2. To generate code, execute the following command:
	```bash
	python run.py gen
	```
3. To test the `CodeGenSuite`, you can use one of the following methods:
	- Run the command:
		```bash
		python run.py test CodeGenSuite
		```
	- Alternatively, use the shell script:
		```bash
		./src/run.sh
		```
	- Or use the Makefile with the command:
		```bash
		make code
		```

---

### Additional Utility

A utility is provided in the `./tests` directory that uses the `classfileanalyzer.jar` tool to analyze Java programs and generate assembly-like Java bytecode. This bytecode can be used to map MiniGo programs to their corresponding Java implementations.

Refer to `./tests/run.sh` for details on how to use this utility.

### Sample MiniGo Code and Mappings

#### MiniGo Code Example
```go
var a int = 100
const b = 100

func main() {
	 // Main function
}

func (h Human) eat(a int) {
	 // Method for Human
}

type struct Human {
	 name string
	 age int
	 money float
}

func (h Human) work(b float) {
	 // Another method for Human
}

type Entity interface {
	 isExist() boolean
}

// Implicit inheritance example:
// Human can implement Entity

func DoSomething() {
	 // Example function
}
```

#### Mapping from MiniGo to Java
- **main**:
	For the program to run, there must be a class contain the starting point main() named MiniGoClass
- **Global Variable**:  
  Mapped to `.field public static global I` (value initialized using `<clinit>`).
- **Global Constant**:  
  Mapped to `.field public static final I = <value>`.
- **Function**:
	Function defined in the global scope, would be best map to the concept of public static method of a class in java, with `.method public static` of a GlobalClass?
- **Struct**:  
	Mapped to another *.j file with `.class`, with field `.field public` and method mapped to `.method public`, must import.
- **Interface**:
	Mapped to another *.j file, with `.interface`, prototype would be mapped to `.method public abstract`, must import.