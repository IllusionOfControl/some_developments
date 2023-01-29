import java.util.Scanner;

/**
 * Created by ariki on 16.03.2017.
 */
public class Main {
    public static void main(String[] args) {
        Core core = new Core();
        int imageNumber;
        int imageValue;
        int upORdown;

        Scanner scanner = new Scanner(System.in);
        System.out.print("\nEnter Image Number:");
        imageNumber = scanner.nextInt();
        System.out.print("\nEnter Image Value:");
        imageValue = scanner.nextInt();
        System.out.println("\nUP or DOWN? 1-UP\t0-DOWN");
        upORdown = scanner.nextInt();
        if (upORdown == 1 ) {
            core.runUp();
        } else if (upORdown == 0) {
            core.runDown();
        } else System.exit( -1);
    }
}
