package return_;

public class Return {
    public static int getInt() {
        return 1;
    }

    public static boolean getBool() {
        return true;
    }

    public static String getString() {
        return "";
    }

    public static float getFloat() {
        return 1.0f;
    }

    public static Animal getDog() {
        return new Dog();
    }
}
