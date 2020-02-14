public abstract class AI {
    int col, row, p,g, player;
    Board board;
    public AI(int col, int row, int p,int g) {
        this.col = col;
        this.row = row;
        this.p = p;
        this.g = g;
    }

    public abstract Move GetMove(Move opponentMove) throws InvalidMoveError;
}
