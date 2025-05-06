package init;

public class Main {
    public void run() {
        // var d Dog; -> no stored
        // var d Dog = Dog{} -> called the <int> default, method
        // putField, getField, to put the value without to
        // generate a new whole constructor?
        Dog dog = new Dog();
    }


    public static void main(String[] args) {
        Main main = new Main();
        main.run();
    }
}
