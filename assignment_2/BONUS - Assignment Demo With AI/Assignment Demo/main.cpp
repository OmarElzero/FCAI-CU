#include <iostream>
#include <bits/stdc++.h>
#include "BoardGame_Classes.h"
// #include "3x3X_O.h"
// #include "X_O_Abstract.h"
// #include "MinMaxPlayer.h"
#include "Pyramic.h"
#include "inverse.h"
#include "4x4.h"
#include "numircal_board.h"
#include "ULTIMATE_TIC_TAC_TOE.h"

using namespace std; // Proper placement

void Pyramic_1(){
    int choice;
    Player<char>* players[2];
    X_O_Board<char>* B = new Pyramic<char>();
    string playerXName, player2Name;

    cout << "Welcome to FCAI X-O Game. :)\n";

    // Set up player 1
    cout << "Enter Player X name: ";
    cin >> playerXName;
    cout << "Choose Player X type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[0] = new X_O_Player<char>(playerXName, 'X');
            break;
        case 2:
            players[0] = new X_O_Random_Player<char>('X');
            break;
        // case 3:
        //     players[0] = new X_O_MinMax_Player<char>('X');
        //     players[0]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 1. Exiting the game.\n";
            return ;
    }

    // Set up player 2
    cout << "Enter Player 2 name: ";
    cin >> player2Name;
    cout << "Choose Player 2 type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[1] = new X_O_Player<char>(player2Name, 'O');
            break;
        case 2:
            players[1] = new X_O_Random_Player<char>('O');
            break;
        // case 3:
        //     players[1] = new X_O_MinMax_Player<char>('O');
        //     players[1]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 2. Exiting the game.\n";
            return ;
    }

    // Create the game manager and run the game
    GameManager<char> x_o_game(B, players);
    x_o_game.run();

    // Clean up
    delete B;
    for (int i = 0; i < 2; ++i) {
        delete players[i];
    }
}
void Inverse_6(){
    int choice;
    Player<char>* players[2];
    X_O_Board<char>* B = new Inverse<char>();
    string playerXName, player2Name;

    cout << "Welcome to FCAI X-O Game. :)\n";

    // Set up player 1
    cout << "Enter Player X name: ";
    cin >> playerXName;
    cout << "Choose Player X type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[0] = new X_O_Player<char>(playerXName, 'X');
            break;
        case 2:
            players[0] = new X_O_Random_Player<char>('X');
            break;
        // case 3:
        //     players[0] = new X_O_MinMax_Player<char>('X');
        //     players[0]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 1. Exiting the game.\n";
            return ;
    }

    // Set up player 2
    cout << "Enter Player 2 name: ";
    cin >> player2Name;
    cout << "Choose Player 2 type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[1] = new X_O_Player<char>(player2Name, 'O');
            break;
        case 2:
            players[1] = new X_O_Random_Player<char>('O');
            break;
        // case 3:
        //     players[1] = new X_O_MinMax_Player<char>('O');
        //     players[1]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 2. Exiting the game.\n";
            return ;
    }
    

    // Create the game manager and run the game
    GameManager<char> x_o_game(B, players);
    x_o_game.run();

    // Clean up
    delete B;
    for (int i = 0; i < 2; ++i) {
        delete players[i];
    }
}
void numircal_5(){
    int choice;
    Player<char>* players[2];
    X_O_Board<char>* B = new Numerical_Tic_Tac_Toe_Board<char>();

    string playerXName, player2Name;

    cout << "Welcome to FCAI X-O Game. :)\n";

    // Set up player 1
    cout << "Enter Player X name: ";
    cin >> playerXName;
    cout << "Choose Player X type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[0] = new Numiric_Player<char>(playerXName, 'X');
            break;
        case 2:
            players[0] = new X_Random_Player<char>('X');
            break;
        // case 3:
        //     players[0] = new X_O_MinMax_Player<char>('X');
        //     players[0]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 1. Exiting the game.\n";
            return ;
    }

    // Set up player 2
    cout << "Enter Player 2 name: ";
    cin >> player2Name;
    cout << "Choose Player 2 type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[1] = new Numiric_Player<char>(player2Name, 'O');
            break;
        case 2:
            players[1] = new X_Random_Player<char>('O');
            break;
        // case 3:
        //     players[1] = new X_O_MinMax_Player<char>('O');
        //     players[1]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 2. Exiting the game.\n";
            return ;
    }
    

    // Create the game manager and run the game
    GameManager<char> x_o_game(B, players);
    x_o_game.run();

    // Clean up
    delete B;
    for (int i = 0; i < 2; ++i) {
        delete players[i];
    }
}
void x4_7(){
    int choice;
    Player<char>* players[2];
    X_O_Board<char>* B = new X_4<char>();

    string playerXName, player2Name;

    cout << "Welcome to FCAI X-O Game. :)\n";

    // Set up player 1
    cout << "Enter Player X name: ";
    cin >> playerXName;
    cout << "Choose Player X type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[0] = new X_Player<char>(playerXName, 'X');
            break;
        case 2:
            players[0] = new X_Random_Player<char>('X');
            break;
        // case 3:
        //     players[0] = new X_O_MinMax_Player<char>('X');
        //     players[0]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 1. Exiting the game.\n";
            return ;
    }

    // Set up player 2
    cout << "Enter Player 2 name: ";
    cin >> player2Name;
    cout << "Choose Player 2 type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[1] = new X_Player<char>(player2Name, 'O');
            break;
        case 2:
            players[1] = new X_Random_Player<char>('O');
            break;
        // case 3:
        //     players[1] = new X_O_MinMax_Player<char>('O');
        //     players[1]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 2. Exiting the game.\n";
            return ;
    }
    

    // Create the game manager and run the game
    GameManager<char> x_o_game(B, players);
    x_o_game.run();

    // Clean up
    delete B;
    for (int i = 0; i < 2; ++i) {
        delete players[i];
    }
}
void Ultimate_8(){
    int choice;
    Player<char>* players[2];
    X_O_Board<char>* B = new Ultimate_Board<char>();

    string playerXName, player2Name;

    cout << "Welcome to FCAI X-O Game. :)\n";

    // Set up player 1
    cout << "Enter Player X name: ";
    cin >> playerXName;
    cout << "Choose Player X type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[0] = new Ultimate_Player<char>(playerXName, 'X');
            break;
        case 2:
            players[0] = new X_Random_Player<char>('X');
            break;
        // case 3:
        //     players[0] = new X_O_MinMax_Player<char>('X');
        //     players[0]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 1. Exiting the game.\n";
            return ;
    }

    // Set up player 2
    cout << "Enter Player 2 name: ";
    cin >> player2Name;
    cout << "Choose Player 2 type:\n";
    cout << "1. Human\n";
    cout << "2. Random Computer\n";
    cout << "3. Smart Computer (AI)\n";
    cin >> choice;

    switch(choice) {
        case 1:
            players[1] = new Ultimate_Player<char>(player2Name, 'O');
            break;
        case 2:
            players[1] = new X_Random_Player<char>('O');
            break;
        // case 3:
        //     players[1] = new X_O_MinMax_Player<char>('O');
        //     players[1]->setBoard(B);
        //     break;
        default:
            cout << "Invalid choice for Player 2. Exiting the game.\n";
            return ;
    }
    

    // Create the game manager and run the game
    GameManager<char> x_o_game(B, players);
    x_o_game.run();

    // Clean up
    delete B;
    for (int i = 0; i < 2; ++i) {
        delete players[i];
    }
}


int main() {
    // Pyramic_1();
    // Inverse_6();
    // x4_7();
    // numircal_5();
    Ultimate_8();

    return 0;
}


