package program;

public class Human implements Entity{
    public String name;
    public int age;

    @Override
    public String getType() {
        return "Human";
    }
}
