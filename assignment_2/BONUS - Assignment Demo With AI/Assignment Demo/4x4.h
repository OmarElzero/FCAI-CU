
#ifndef _4X4_H
#define _4X4_H

#include "BoardGame_Classes.h"
#include "X_O_Abstract.h"
int x_1=-1,y_1=-1;
bool flag = false;
template <typename T>
class X_4:public X_O_Board <T> {
public:
    X_4();
    bool is_win();
    bool update_board(int x2, int y2, T mark);
    bool validate_move(int x, int y,int x1, int y1);
    private:
    T currentPlayer;
};
X_4<char>* globalBoard;

template <typename T>
class X_Player : public Player<T> {
public:
    X_Player (string name, T symbol);
    void getmove(int& x, int& y);

};

template <typename T>
class X_Random_Player : public RandomPlayer<T>{
public:
    X_Random_Player (T symbol);
    void getmove(int& x, int& y) ;
    
    };









//--------------------------------------- IMPLEMENTATION

#include <iostream>
#include <iomanip>
#include <cctype>  // for toupper()

using namespace std;


// Constructor for X_O_Board
template <typename T>
X_4<T>::X_4() {
    this->rows = 4;
    this->columns = 4;
    this->board = new char*[this->rows];
    for (int i = 0; i < this->rows; i++) {
        this->board[i] = new char[this->columns];
        for (int j = 0; j < this->columns; j++) {
            this->board[i][j] = 0;
        }
    }
    this->n_moves = 0;
    this->board[0][0]='O';
    this->board[0][1]='X';
    this->board[0][2]='O';
    this->board[0][3]='X';
    this->board[3][3]='O';
    this->board[3][1]='O';
    this->board[3][0]='X';
    this->board[3][2]='X';
    globalBoard = this;
    currentPlayer = 'X';
}

// Returns true if there is any winner
template <typename T>
bool X_4<T>::is_win() {
   
     // Check rows and columns
    for (int i = 0; i < this->rows; i++) {
        if ((this->board[i][0] == this->board[i][1] && this->board[i][1] == this->board[i][2] && this->board[i][0] != 0) ||
            (this->board[i][1] == this->board[i][2] && this->board[i][2] == this->board[i][3] && this->board[i][1] != 0) ||
            (this->board[0][i] == this->board[1][i] && this->board[1][i] == this->board[2][i] && this->board[0][i] != 0) ||
            (this->board[1][i] == this->board[2][i] && this->board[2][i] == this->board[3][i] && this->board[1][i] != 0)
            ) {
           return true;
        }
        
    }

    // Check diagonals
    // Top-left to bottom-right (primary diagonals)
    if ((this->board[0][0] == this->board[1][1] && this->board[1][1] == this->board[2][2] && this->board[0][0] != 0) ||
        (this->board[1][1] == this->board[2][2] && this->board[2][2] == this->board[3][3] && this->board[1][1] != 0) ||
        (this->board[0][1] == this->board[1][2] && this->board[1][2] == this->board[2][3] && this->board[0][1] != 0) ||
        (this->board[1][0] == this->board[2][1] && this->board[2][1] == this->board[3][2] && this->board[1][0] != 0)) {
        return true;
    }

    // Top-right to bottom-left (secondary diagonals)
    if ((this->board[0][3] == this->board[1][2] && this->board[1][2] == this->board[2][1] && this->board[0][3] != 0) ||
        (this->board[1][2] == this->board[2][1] && this->board[2][1] == this->board[3][0] && this->board[1][2] != 0) ||
        (this->board[0][2] == this->board[1][1] && this->board[1][1] == this->board[2][0] && this->board[0][2] != 0) ||
        (this->board[1][3] == this->board[2][2] && this->board[2][2] == this->board[3][1] && this->board[1][3] != 0)) {
        return true;
    }

    return false;

     
}


template <typename T>
bool X_4<T>::update_board(int x2, int y2, T mark) {
    
    if (currentPlayer != mark) {
        cout << "It's not " << mark << "'s turn!\n";
        return false;
    }
    // Only update if move is valid
    if((!(x2 < 0 || x2 >= this->rows || y2 < 0 || y2 >= this->columns)) && (this->board[x2][y2] == 0|| mark == 0) && this->validate_move(x_1,y_1,x2,y2) ) {
        
        this->board[x_1][y_1]=0;
        this->board[x2][y2]=toupper(mark);
        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';

        return true;
    }

    return false;
}






template <typename T>
bool X_4<T>::validate_move(int x_1, int y_1, int x, int y) {
    if(flag){
        if(this->board[x_1][y_1]!=currentPlayer)
        {
            return false;
        }
    }
    else{
        if(this->board[x_1][y_1]!=currentPlayer)
        {
            cout << "it's not your peace!";
            return false;
        }
    }
    if (1) {
        x_1 = ::x_1; 
        y_1 = ::y_1;
    }
    // Check if the destination square is open
    if (this->board[x][y] != 0) {
        return false;
    }

    // Check if the move is to an adjacent square
    int dx = abs(x - x_1);
    int dy = abs(y - y_1);

    // Allow only horizontal or vertical moves (not diagonal)
    if ((dx == 1 && dy == 0) || (dx == 0 && dy == 1)) {
        return true;
    }

    return false; // Invalid move if none of the above conditions are met
}


// Constructor for X_Player
template <typename T>
X_Player<T>::X_Player(string name, T symbol) : Player<T>(name, symbol) {}

template <typename T>
void X_Player<T>::getmove(int& x, int& y) {
    cout << "\nPlease enter the position of the peace you want to move";
    cin>> x_1>>y_1;
    cout << "\nPlease enter your move x and y(0 to 2 ) separated by spaces: ";
    cin >> x >> y;
}

// Constructor for X_Random_Player
template <typename T>
X_Random_Player<T>::X_Random_Player(T symbol) 
    : RandomPlayer<T>(symbol) {  // Initialize gameBoard reference here
    this->dimension = 3;  // Adjust dimension if needed
    this->name = "Random Computer Player";
    srand(static_cast<unsigned int>(time(0)));  // Seed the random number generator
}
template <typename T>
void X_Random_Player<T>::getmove(int& x, int& y) {
    do {
        x = rand() % this->dimension;  // Random number between 0 and 2 
        x_1 = rand() % this->dimension;  // Random number between 0 and 2
        y = rand() % this->dimension;
        y_1 = rand() % this->dimension;
        flag = true;
    } while (!globalBoard->validate_move(x_1,y_1,x,y));  // Validate move against the game board
}




#endif 

