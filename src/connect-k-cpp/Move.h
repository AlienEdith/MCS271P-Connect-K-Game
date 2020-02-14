#ifndef MOVE_H
#define MOVE_H
#include <string>
#include <sstream>
#pragma once
class Move
{
public:
	int row; //the row to move to. 
	int col; //the col to move to.
	Move();
	Move(int col, int row);
	Move(std::string s);
	std::string toString();
};

#endif //MOVE_H
