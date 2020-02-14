import java.util.*;

public class Move 
{
	public int row, col;

	public Move() 
	{
		this.col = 0;
		this.row = 0;
	}

	public Move(int col, int row) 
	{
		this.col = col;
		this.row = row;
	}

	public Move(String s)
	{
        Scanner reader = new Scanner(s);
        col = reader.nextInt();
		row = reader.nextInt();
		this.col = col;
		this.row = row;
	}

	public String toString()
	{
	    return col+" "+row;
	}
}