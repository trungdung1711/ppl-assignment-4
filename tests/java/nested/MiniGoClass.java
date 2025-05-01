package nested;

public class MiniGoClass {
	public static void main(String[] args) {
		int a = 100;
		{
			int b = a + 100;
			int c = a + b;
		}
		int d = 100;
	}
}
