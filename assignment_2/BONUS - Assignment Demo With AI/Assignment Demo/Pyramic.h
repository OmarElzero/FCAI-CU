
#ifndef _PYRAMIC_H
#define _PYRAMIC_H

#include "BoardGame_Classes.h"
#include "X_O_Abstract.h"

template <typename T>
class Pyramic:public X_O_Board <T> {
public:
    Pyramic();
    void display_board ();
    bool is_win();
    protected:
    bool validate_move(int x, int y);

};






//--------------------------------------- IMPLEMENTATION

#include <iostream>
#include <iomanip>
#include <cctype>  // for toupper()

using namespace std;

// Constructor for Pyramic
template <typename T>   
Pyramic<T>::Pyramic() {
    this->rows = 3; 
    this->columns = 5;
    this->board = new char*[this->rows];

    for (int i = 0; i < this->rows; i++) {
        int cols_in_row = this->columns - (i * 2); 
        this->board[i] = new char[cols_in_row];
        for (int j = 0; j < cols_in_row; j++) {
            this->board[i][j] = 0; 
        }
    }
    this->n_moves = 0;
}


// Display the board and the pieces on it
template <typename T>
void Pyramic<T>::display_board() {
   for (int i = 0; i < 3; ++i) {
        if (i==0) cout <<"              ";
        if (i==1) cout <<"    ";
        for (int j = 0; j < 3 + i; ++j) {
            if (j >= 3 - 1 - i && j <= 3 - 1 + i) {
                cout << "(" << i << "," << j << ")";          
                cout<<"| ";
                cout <<this->board [i][j];
                cout<<" |";
            } else {
                cout <<setw(7);
            }
        }
        cout << "\n";
    }
    cout << endl;
}

// Returns true if there is any winner
template <typename T>
bool Pyramic<T>::is_win() {
     char row_win[4], col_win[1], diag_win[2];

    row_win [0] = this->board[1][1] & this->board[1][2] & this->board[1][3];
    row_win [1] = this->board[2][1] & this->board[2][2] & this->board[2][3];
    row_win [2] = this->board[2][0] & this->board[2][1] & this->board[2][2];
    row_win [3] = this->board[2][2] & this->board[2][3] & this->board[2][4];
    col_win [0] = this->board[0][2] & this->board[1][2] & this->board[2][2];
    diag_win[0] = this->board[0][2] & this->board[1][3] & this->board[2][4];
    diag_win[1] = this->board[0][2] & this->board[1][1] & this->board[2][0];


    if ( (row_win[0] && (row_win[0] == this->board[1][2]))) return true;
    if ( (row_win[1] && (row_win[1] == this->board[2][2]))) return true;
    if ( (row_win[2] && (row_win[2] == this->board[2][1]))) return true;
    if ( (row_win[3] && (row_win[3] == this->board[2][3]))) return true;
    if ( (col_win[0] && (col_win[0] == this->board[0][2]))) return true;
    if ((diag_win[0] && diag_win[0] == this->board[0][2]) ||
        (diag_win[1] && diag_win[1] == this->board[0][2]))
    {return true;}

    return false;
}

template <typename T>
bool Pyramic<T>::validate_move(int x, int y){
    if(((x==0&&y==2)||(x==1&&y==1)||(x==1&&y==2)||(x==1&&y==3)||(x==2&&y==0)||(x==2&&y==1)||(x==2&&y==2)||(x==2&&y==3)||(x==2&&y==4))&&this->board[x][y]==0)
    {
        return true;

    }
    return false;
}











#endif 

