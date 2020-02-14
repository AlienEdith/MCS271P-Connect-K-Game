 public class Main {
    public static void main (String[] args) throws InvalidMoveError, InvalidParameterError {
        if (args.length <  5) {
            System.out.println("Invalid Parameters");
            System.exit(0);
        }
        // mode = "m" -> manual / "t" -> tournament
        int col = Integer.parseInt(args[0]),
            row = Integer.parseInt(args[1]),
            k = Integer.parseInt(args[2]),
            g = Integer.parseInt(args[3]),
            order = 0;
        String mode = args[4];
        if ("m".equals(mode) || "manual".equals(mode)|| "s".equals(mode) || "self".equals(mode))
            order = Integer.parseInt(args[5]);
        GameLogic main = new GameLogic(col, row, k,g, mode, order);
        main.Run();
    }
}