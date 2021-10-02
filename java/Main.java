public class Main {
    public static void main(String[] args) {
        bouncingBall(3.0, 0.66, 1.5);
        bouncingBall(30.0, 0.66, 1.5);
        bouncingBall(70.0, 0.75, 1);
        bouncingBall(50.0, 0.3, 3);

        Log(reverse("Hello "));
    }

    public static void Log(String logtxt) {
        System.out.println(logtxt);   
    }

    public static int bouncingBall(double h, double bounce, double window) {
            int times = 0;
            boolean isFailling = true;
            double heightBall = h;
          
            while (true) {
                if (isFailling) times++;
                if (!isFailling) {
                    heightBall*=bounce;
                    if (heightBall<window) return times;
                    times++;
                }
                isFailling=!isFailling;
            }
    }

    public static string reverse(String s) {
        String r = new String(s.lenght);
        for (int i = 0; i < s.lenght; i++) {
            r[i] = s[s.lenght -1 -i];
        }
    }
}