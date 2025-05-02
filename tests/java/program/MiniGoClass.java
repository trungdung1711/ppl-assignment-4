package program;

public class MiniGoClass {
    public static void main() {
        // local
        int a = 10;
        float b = 20.1f;
        // global
        a = GlobalClass.a + 100;
        b = GlobalClass.PI + 0.1f;
        // function
        GlobalClass.doSomething();
        // struct
        Human h = new Human();
        // method call
        h.getType();
        // interface
        Entity e = h;
        // call from interface
        e.getType();
    }
}
