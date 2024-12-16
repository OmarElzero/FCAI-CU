#ifndef _ULTIMATE_TIC_TAC_TOE_H
#define _ULTIMATE_TIC_TAC_TOE_H

#include "BoardGame_Classes.h"
#include <iostream>
#include <vector>

using namespace std;
int indexx=0;
int x_wins=0;
int o_wins=0;
char currentPlayer;

template <typename T>
class Ultimate_Board:public X_O_Board<T>{
public:
    Ultimate_Board ();
    bool update_board (int x , int y , T symbol) override;
    void display_board () override;
    bool is_win() override;
    bool is_draw() override;
    bool game_is_over() override;
    protected:
    bool validate_move(int x, int y);
    static const int SIZE = 9; 
    char boards[SIZE][3][3];  
};

template <typename T>
class Ultimate_Player : public X_O_Player<T> {
public:
    Ultimate_Player (string name, T symbol);
    void getmove(int& x, int& y);

};

// template <typename T>
// class X_O_Random_Player : public RandomPlayer<T>{
// public:
//     X_O_Random_Player (T symbol);
//     void getmove(int &x, int &y) ;
// };





//--------------------------------------- IMPLEMENTATION

#include <iostream>
#include <iomanip>
#include <cctype>  // for toupper()

using namespace std;

// Constructor for Ultimate_Board
template <typename T>
Ultimate_Board<T>::Ultimate_Board() {
    rows = 3; // Ultimate board is 3x3
    columns = 3;

        // Allocate memory for the ultimate board (3x3 grid of 3x3 boards)
        for(int i = 0; i <SIZE; i++){
        this->rows = 3;
        this->columns = 3;
        this->board = new char*[this->rows];
        for (int i = 0; i < this->rows; i++) {
        this->board[i] = new char[this->columns];
        for (int j = 0; j < this->columns; j++) {
            this->board[i][j] = 0;
        }
    }
            
        }     
    
    this->n_moves = 0;
}


template <typename T>
bool Ultimate_Board<T>::update_board(int x, int y, T mark) {
    // Only update if move is valid
    if((!(x < 0 || x >= this->rows || y < 0 || y >= this->columns)) && (this->board[x][y] == 0|| mark == 0) && this->validate_move(x,y) ) {
        
        if (mark == 0){
            this->n_moves--;
            this->board[x][y] = 0;
        }
        else {
            this->n_moves++;
            boards[indexx][x][y] = toupper(mark);
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';

        }

        return true;
    }

    return false;
}

// Display the board and the pieces on it
template <typename T>
void Ultimate_Board<T>::display_board() {
for (int i = 0; i < SIZE; i++) {  // Iterate over the rows of the ultimate board
        for (int j = 0; j < SIZE; j++) {  // Iterate over the columns of the ultimate board
            // Print each small 3x3 board within the ultimate board
            cout << "Board (" << i << "," << j << "):\n";
            for (int sub_row = 0; sub_row < 3; sub_row++) {
                for (int sub_col = 0; sub_col < 3; sub_col++) {
                    // Print each position within the small 3x3 board
                    cout << setw(2) << this->boards[i * 3 + j][sub_row][sub_col] << " ";
                }
                cout << endl;
            }
            cout << endl;  // Space between boards for readability
        }
        cout << "===========================\n";  // Separator between rows of boards
    }
}



// Returns true if there is any winner
template <typename T>
bool Ultimate_Board<T>::is_win() {
    // Check rows and columns
    for (int i = 0; i < this->rows; i++) {
        if ((this->board[i][0] == this->board[i][1] && this->board[i][1] == this->board[i][2] && this->board[i][0] != 0) ||
            (this->board[0][i] == this->board[1][i] && this->board[1][i] == this->board[2][i] && this->board[0][i] != 0)) {
            if(currentPlayer== 'X')
            {
                x_wins++;
            }
            else{
                o_wins++;
            }
        }
    }

    // Check diagonals
    if ((this->board[0][0] == this->board[1][1] && this->board[1][1] == this->board[2][2] && this->board[0][0] != 0) ||
        (this->board[0][2] == this->board[1][1] && this->board[1][1] == this->board[2][0] && this->board[0][2] != 0)) {
        if(currentPlayer== 'X')
            {
                x_wins++;
            }
            else{
                o_wins++;
            }
    }


    return false;
}

// Return true if 9 moves are done and no winner
template <typename T>
bool Ultimate_Board<T>::is_draw() {
    return (this->n_moves == 20 && !is_win());
}

template <typename T>
bool Ultimate_Board<T>::game_is_over() {
    return is_win() || is_draw();
}
// Return True if move is valid
// Draft to override
template <typename T>
bool Ultimate_Board<T>::validate_move(int x, int y) {
    if((!(x < 0 || x >= this->rows || y < 0 || y >= this->columns)))
    {
        return true;
    }
    return false;
}

//--------------------------------------

// Constructor for X_O_Player
template <typename T>
Ultimate_Player<T>::Ultimate_Player(string name, T symbol) : X_O_Player<T>(name, symbol) {}

template <typename T>
void Ultimate_Player<T>::getmove(int& x, int& y) {
    cout << "Please Enter The Board Indexx ";
    cin >> indexx;
    cout << "\nPlease enter your move x and y(0 to 2 ) separated by spaces: ";
    cin >> x >> y;
}

// // Constructor for X_O_Random_Player
// template <typename T>
// X_O_Random_Player<T>::X_O_Random_Player(T symbol) : RandomPlayer<T>(symbol) {
//     this->dimension = 3;
//     this->name = "Random Computer Player";
//     srand(static_cast<unsigned int>(time(0)));  // Seed the random number generator
// }

// template <typename T>
// void X_O_Random_Player<T>::getmove(int& x, int& y) {
//     x = rand() % this->dimension;  // Random number between 0 and 2
//     y = rand() % this->dimension;
// }


// template <typename T>
// class UltimateTicTacToe : public Board<T> {
// private:
//     int current_board_x, current_board_y; // Track where the next move should go
//     bool winner_found;

// public:
//     UltimateTicTacToe(int size = 3) {
//         this->rows = this->columns = size; // Main board is 3x3
//         this->n_moves = 0;
//         this->winner_found = false;

//         // Initialize the main board with smaller TicTacToe boards
//         mainBoard.resize(3, vector<Board<T>*>(3, nullptr));
//         for (int i = 0; i < 3; i++) {
//             for (int j = 0; j < 3; j++) {
//                 mainBoard[i][j] = new Board<T>();
//             }
//         }
//     }

//     bool update_board(int x, int y, T symbol) override {
//         // Ensure the move is on the correct small board as determined by the main board
//         if (current_board_x >= 0 && current_board_y >= 0 && current_board_x < 3 && current_board_y < 3) {
//             Board<T>* smallBoard = mainBoard[current_board_x][current_board_y];
//             if (smallBoard->update_board(x, y, symbol)) {
//                 this->n_moves++;
//                 return true;
//             }
//         }
//         return false;
//     }

//     void display_board() override {
//         // Display all small boards inside the main board
//         for (int i = 0; i < 3; i++) {
//             for (int j = 0; j < 3; j++) {
//                 mainBoard[i][j]->display_board();
//                 cout << (j == 2 ? "" : " | ");
//             }
//             cout << endl;
//             if (i != 2) {
//                 cout << "---------------------" << endl;  // Separator between rows of boards
//             }
//         }
//     }

//     bool is_win() override {
//         // Check if any row, column, or diagonal of the main board has won
//         for (int i = 0; i < 3; i++) {
//             // Check rows
//             if (mainBoard[i][0]->is_win() && mainBoard[i][1]->is_win() && mainBoard[i][2]->is_win()) {
//                 winner_found = true;
//                 return true;
//             }
//             // Check columns
//             if (mainBoard[0][i]->is_win() && mainBoard[1][i]->is_win() && mainBoard[2][i]->is_win()) {
//                 winner_found = true;
//                 return true;
//             }
//         }
//         // Check diagonals
//         if (mainBoard[0][0]->is_win() && mainBoard[1][1]->is_win() && mainBoard[2][2]->is_win()) {
//             winner_found = true;
//             return true;
//         }
//         if (mainBoard[0][2]->is_win() && mainBoard[1][1]->is_win() && mainBoard[2][0]->is_win()) {
//             winner_found = true;
//             return true;
//         }

//         return false;
//     }

//     bool is_draw() override {
//         // If all smaller boards are filled and no winner, it's a draw
//         for (int i = 0; i < 3; i++) {
//             for (int j = 0; j < 3; j++) {
//                 if (!mainBoard[i][j]->is_draw()) {
//                     return false;
//                 }
//             }
//         }
//         return true;
//     }

//     bool game_is_over() override {
//         return winner_found || is_draw();
//     }

//     void set_next_board(int x, int y) {
//         current_board_x = x;
//         current_board_y = y;
//     }
// };

// template <typename T>
// class HumanPlayer : public Player<T> {
// public:
//     HumanPlayer(string name, T symbol) : Player<T>(name, symbol) {}

//     void getmove(int& x, int& y) override {
//         cout << this->getname() << ", Enter the row and column (0-2) of the small board where you want to play: ";
//         cin >> x >> y;
//     }
// };

// template <typename T>
// class RandomPlayer : public Player<T> {
// public:
//     RandomPlayer(T symbol) : Player<T>(symbol) {}

//     void getmove(int& x, int& y) override {
//         // Generate random move
//         x = rand() % 3;
//         y = rand() % 3;
//         cout << this->getname() << " (Random) chooses: " << x << ", " << y << endl;
//     }
// };


#endif
