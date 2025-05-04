package interface_;

public class Dog implements Animal, Mammal{

	public String name;
	public int age;
	
	@Override
	public String getType() {
		return "Dog";
	}

	@Override
	public void giveBirth() {
		return;
	}
}
