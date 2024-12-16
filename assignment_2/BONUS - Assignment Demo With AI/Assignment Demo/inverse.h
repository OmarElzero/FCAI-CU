
#ifndef _INVERSE_H
#define _INVERSE_H

#include "BoardGame_Classes.h"
#include "X_O_Abstract.h"
int loss_count = 0;
template <typename T>
class Inverse:public X_O_Board <T> {
    private:
    string name;
    public:

    bool is_win();    
};







//--------------------------------------- IMPLEMENTATION

#include <iostream>
#include <iomanip>
#include <cctype>  // for toupper()

using namespace std;

// Returns true if there is any winner
template <typename T>
bool Inverse<T>::is_win() {
    if(loss_count)
    {
        return true;
    }
     // Check rows and columns
    for (int i = 0; i < this->rows; i++) {
        if ((this->board[i][0] == this->board[i][1] && this->board[i][1] == this->board[i][2] && this->board[i][0] != 0) ||
            (this->board[0][i] == this->board[1][i] && this->board[1][i] == this->board[2][i] && this->board[0][i] != 0)) {
           loss_count++;
        }
        
    }

    // Check diagonals
    if ((this->board[0][0] == this->board[1][1] && this->board[1][1] == this->board[2][2] && this->board[0][0] != 0) ||
        (this->board[0][2] == this->board[1][1] && this->board[1][1] == this->board[2][0] && this->board[0][2] != 0)) {
        loss_count++;
    }
    return false;

}










#endif 

