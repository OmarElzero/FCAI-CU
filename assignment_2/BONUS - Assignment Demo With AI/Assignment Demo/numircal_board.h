#ifndef NUMERICAL_TIC_TAC_TOE_BOARD_H
#define NUMERICAL_TIC_TAC_TOE_BOARD_H

#include "BoardGame_Classes.h"
#include <iostream>
#include <iomanip>
char currentPlayer;
using namespace std;
int num_for_board;
template <typename T>
class Numerical_Tic_Tac_Toe_Board : public X_O_Board<T> {  // الوراثة من Board<T>
public:
    Numerical_Tic_Tac_Toe_Board();

    bool update_board(int x, int y, T symbol);
    void display_board();
    bool is_win();
    bool is_draw();
    bool game_is_over();

private:
    bool validate_move(int x, int y);
};

template <typename T>
class Numiric_Player : public X_O_Player<T> {
public:
    Numiric_Player (string name, T symbol);
    void getmove(int& x, int& y);

};



///////////////// implemntation//////////////////////


template <typename T>
Numerical_Tic_Tac_Toe_Board<T>::Numerical_Tic_Tac_Toe_Board() {
    this->rows = 3;
    this->columns = 3;
    this->board = new T*[this->rows];
    for (int i = 0; i < this->rows; i++) {
        this->board[i] = new T[this->columns]{0};
    }
    this->n_moves = 0;
    currentPlayer = 'X';
}

template <typename T>
bool Numerical_Tic_Tac_Toe_Board<T>::update_board(int x, int y, T mark) {
    // Only update if move is valid
    if((!(x < 0 || x >= this->rows || y < 0 || y >= this->columns)) && (this->board[x][y] == 0|| mark == 0) && this->validate_move(x,y) ) {
        
        if (mark == 0){
            this->n_moves--;
            this->board[x][y] = 0;
        }
        else {
            this->n_moves++;
            this->board[x][y] = num_for_board;
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
        }

        return true;
    }

    return false;
}

template <typename T>
void Numerical_Tic_Tac_Toe_Board<T>::display_board() {

    for (int i = 0; i < this->rows; i++) {
        cout << "\n| ";
        for (int j = 0; j < this->columns; j++) {
            cout << "(" << i << "," << j << ")";
            cout << setw(2) << to_string(this->board[i][j]) << " |";
        }
        cout << "\n-----------------------------";
    }
    cout << endl;
}

template <typename T>
bool Numerical_Tic_Tac_Toe_Board<T>::is_win() {
    for (int i = 0; i < this->rows; i++) {
        if (this->board[i][0] + this->board[i][1] + this->board[i][2] == 15 || 
            this->board[0][i] + this->board[1][i] + this->board[2][i] == 15) {
            return true;
        }
    }
    return (this->board[0][0] + this->board[1][1] + this->board[2][2] == 15 || 
            this->board[0][2] + this->board[1][1] + this->board[2][0] == 15);
}

template <typename T>
bool Numerical_Tic_Tac_Toe_Board<T>::is_draw() {
    return this->n_moves == 9 && !is_win();
}

template <typename T>
bool Numerical_Tic_Tac_Toe_Board<T>::game_is_over() {
    return is_win() || is_draw();
}

template <typename T>
bool Numerical_Tic_Tac_Toe_Board<T>::validate_move(int x, int y) {
 if((!(x < 0 || x >= this->rows || y < 0 || y >= this->columns)))
    {
        if (currentPlayer=='X' && num_for_board%2!=0 && num_for_board<10)
        {
            return true;
        }
        else if(currentPlayer=='X' && (num_for_board%2==0 || num_for_board>=10)){
            cout << "Please Enter An odd number ";
            return false;
        }
        if(currentPlayer=='O' && num_for_board%2==0 && num_for_board<10){
            return true;
        }
       else {
        cout << "Please Enter An even number ";
        return false;
        }
        
    }
    return false;
    }

template <typename T>
Numiric_Player<T>::Numiric_Player(string name, T symbol) : X_O_Player<T>(name, symbol) {}

template <typename T>
void Numiric_Player<T>::getmove(int& x, int& y){
cout << "\nPlease enter the position you want to put your number on it (0 to 2 ) separated by spaces: ";
    cin >> x >> y;
    cout << "Please enter your number: ";
    cin >> num_for_board;
    this->symbol = num_for_board;
    cout << "Move: (" << x << ", " << y << "), Number: " << num_for_board << endl;
    cout << currentPlayer <<endl;
}

#endif