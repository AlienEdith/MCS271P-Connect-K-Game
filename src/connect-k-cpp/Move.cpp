#include "Move.h"


Move::Move()
{
	row = 0;
	col = 0;
}
Move::Move(int col, int row){
	this->row=row;
	this->col=col;
}

Move::Move(std::string s)
{
    std::stringstream ss;
    int c,r;
    ss<<s;
    ss>>c>>r;
    this->row=r;
	this->col=c;

}
std::string Move::toString()
{
    std::string c,r;
    std::stringstream ss;
    ss<<col;
    c = ss.str();
    ss.str("");
    ss<<row;
    r = ss.str();
    return c+" "+r;
}



