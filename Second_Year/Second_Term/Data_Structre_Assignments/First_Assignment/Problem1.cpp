#include <bits/stdc++.h>
#include <curl/curl.h>

#include "Custom_vector.h"
using namespace std;
Node *head = NULL;
Node *tail = NULL;
const int MAX_TOKENS = 10;  
const int MAX_STRING_LENGTH = 100; 

class IftarManager{
   
    public:
    IftarManager(){
        head = NULL;
        tail = NULL;
    }
    // Node guest_list = *head;
    void add_guest(Guest guest);
    void display_all_guests();
    void update_guest_invitation(string name, string new_date);
    void send_reminder(string date);
    void sort_guest_list();
};

/////////////////////////////////////////Guest Class Functions/////////////////////////////////////////
/////////////////////////////////////////Guest Class Functions/////////////////////////////////////////
void Guest::display_guest(){
    head->print_list(head);
 }
 string Guest::update_invitation(string new_date){
     head->update_date(new_date, head);
     return "Invitation updated successfully!";
 }
    void Guest::send_reminder(string date){
        head->send_reminder_node(date, head);
    }

///////////////////////////////////////////////////////Class IftarManager Functions/////////////////////////////////////////
void IftarManager::add_guest(Guest guest){
    head->add_at_begining(guest, &head, &tail);
}
void IftarManager::display_all_guests(){
    head->print_list(head);
    
}
void IftarManager::update_guest_invitation(string name, string new_date){
    head->update_specific_date(Guest(name,"hh","ff"), new_date, head);

}
void IftarManager::send_reminder(string date){
    head->send_reminder_node(date, head);
}
void IftarManager::sort_guest_list(){
    head->sort_guest_list(head);
}


    
int main(){
    IftarManager iftarManager;
    //test that custom vector is working
// IftarManager iftarManager;
// iftarManager.add_guest(Guest("Ali", "03001234567", "12-05-2021"));
// iftarManager.add_guest(Guest("Ahmed", "03001234567", "12-05-2021"));
// iftarManager.add_guest(Guest("Asad", "03001234567", "12-05-2021"));
// iftarManager.guest_list.print_list(head);
// iftarManager.guest_list.free_list(&head);


while(true){
    cout << "Welcome to Iftar Manager!\n";
    cout << "1.Start\n";
    cout << "2.Exit\n:";
    int x;
    cin >> x;
    if (x==1){
        cout << "Welcome to Iftar Manager!\n";
        cout << "What method do you want to use !\n";
        cout << "1.cin\n";
        cout << "2.file\n:";
        cout << "Please enter your choice: ";
        int choice;
        cin >> choice;
        if (choice == 1) {
            cout << "You chose cin method.\n";
        
        
        while(true){
        cout << "What do you wanna do ?\n";
        cout << "1.add a guest\n";
        cout << "2.delete a guest\n";
        cout << "3.print all guests\n";
        cout << "4.print specific guest details\n";
        cout << "5.ubdate date for all guests\n";
        cout << "6.ubdate date for specific guest\n";
        cout << "7.send a reminder to all guests\n";
        cout << "8.sort guest list\n";
        cout << "9.Exit\n";
        cout << "10.Manual Tests\n";
        int choice2;
        cin >> choice2;
        string name;
        string contact;
        string iftar_date;
        switch (choice2)
        {
        case 1:
            cout << "please enter the following data\n";
            cout << "Guest name: ";
            cin >> name;
            cout << "\nGuest Contact: ";
            cin >> contact;
            cout << "\nIftar date: ";
            cin >> iftar_date;
            iftarManager.add_guest(Guest(name,contact,iftar_date));       
            break;
        case 2:
            cout << "Enter the name of the guest you want to delete\n";
            cin >> name;
            head->remove_with_name(Guest(name,"df","df"),&head,&tail);
            break;
        case 3:
            cout << "here are all of your guests\n";
            iftarManager.display_all_guests();
            break;
        case 4:
            cout << "Enter the name of the guest you want to view: ";
            cin >> name;
            head->print_specific_guest(Guest(name,"hh","ff"), head);
            break;
        case 5:
            cout << "Enter the new date for all guests: ";
            cin >> iftar_date;
            Guest("","","").update_invitation(iftar_date);
            break;
        case 6:
            cout << "Enter the name of the guest you want to update: ";
            cin >> name;
            cout << "Enter the new date: ";
            cin >> iftar_date;
            iftarManager.update_guest_invitation(name,iftar_date);
            break;
        case 7:
            cout << "Enter the date to send reminders for: ";
            cin >> iftar_date;
            // head->send_reminder_node(iftar_date, head);
            iftarManager.send_reminder(iftar_date);
            // head->send_email();
            break;
        default:
            cout << "Invalid choice! Please enter a valid number.\n";
            break;
        case 8:
            iftarManager.sort_guest_list();
            break;
        case 9:
            head->free_list(&head);
            break;
        case 10:
        iftarManager.add_guest(Guest("omar","0114551455","2004-11-05"));
        iftarManager.add_guest(Guest("Mohamed","0114551455","2007-11-05"));
        iftarManager.add_guest(Guest("Ahmed","0114551455","1999-11-05"));
        iftarManager.add_guest(Guest("SAyed","0114551455","3050-11-05"));
        iftarManager.add_guest(Guest("Moo","0114551455","2015-11-05"));
        cout << "Before sorting : \n";
        iftarManager.display_all_guests();
        cout << "\nAfter Sorting: \n";
        iftarManager.sort_guest_list();
        iftarManager.display_all_guests();
        }
        if (choice2==9){
            cout << "Goodbye!\n";
            break;
        }
        else{

        
        continue;
    }
    }
}

else if (choice == 2) {
    cout << "You chose file method.\n";
    cout << "Please enter the file name: ";
    char filename[MAX_STRING_LENGTH];
    cin >> filename;
    
    ifstream file(filename);
    if (!file) {
        cout << "Error opening file.\n";
        continue;
    }
    
    char line[256];  
    while (file.getline(line, sizeof(line))) {
        char* tokens[MAX_TOKENS];  
        int token_count = 0;

       
        char* token = strtok(line, ",");
        while (token != nullptr && token_count < MAX_TOKENS) {
            tokens[token_count] = token;
            token_count++;
            token = strtok(nullptr, ",");
        }

        if (token_count == 0) {
            continue;
        }

        int instruction = atoi(tokens[0]);  

        switch (instruction) {
        case 1: // Add guest
            if (token_count == 4) {
                char name[MAX_STRING_LENGTH], contact[MAX_STRING_LENGTH], iftar_date[MAX_STRING_LENGTH];
                strcpy(name, tokens[1]);
                strcpy(contact, tokens[2]);
                strcpy(iftar_date, tokens[3]);
                iftarManager.add_guest(Guest(name, contact, iftar_date));
            } else {
                cout << "Invalid format for adding a guest.\n";
            }
            break;

        case 2: // Delete guest
            if (token_count == 2) {
                char name[MAX_STRING_LENGTH];
                strcpy(name, tokens[1]);
                head->remove_with_name(Guest(name, "", ""), &head, &tail);
            } else {
                cout << "Invalid format for deleting a guest.\n";
            }
            break;

        case 3: // Display all guests
            iftarManager.display_all_guests();
            break;

        case 4: // Display specific guest
            if (token_count == 2) {
                char name[MAX_STRING_LENGTH];
                strcpy(name, tokens[1]);
                head->print_specific_guest(Guest(name, "", ""), head);
            } else {
                cout << "Invalid format for displaying a specific guest.\n";
            }
            break;

        case 5: // Update date for all guests
            if (token_count == 2) {
                char new_date[MAX_STRING_LENGTH];
                strcpy(new_date, tokens[1]);
                Guest("", "", "").update_invitation(new_date);
            } else {
                cout << "Invalid format for updating date for all guests.\n";
            }
            break;

        case 6: // Update date for specific guest
            if (token_count == 3) {
                char name[MAX_STRING_LENGTH], new_date[MAX_STRING_LENGTH];
                strcpy(name, tokens[1]);
                strcpy(new_date, tokens[2]);
                iftarManager.update_guest_invitation(name, new_date);
            } else {
                cout << "Invalid format for updating date for a specific guest.\n";
            }
            break;

        case 7: // Send reminder to all guests
            if (token_count == 2) {
                char date[MAX_STRING_LENGTH];
                strcpy(date, tokens[1]);
                iftarManager.send_reminder(date);
            } else {
                cout << "Invalid format for sending reminders.\n";
            }
            break;

        case 8: // Sort guest list
            iftarManager.sort_guest_list();
            break;

        default:
            cout << "Invalid instruction in file: " << instruction << "\n";
            break;
        }
    }
    file.close();
}

        else {
            cout << "Invalid choice! Please enter a valid number.\n";
            continue;
        }
        
}
    else if (x==2){
        cout << "Goodbye!\n";
        break;
    }
    else{
        cout << "Invalid choice! Please enter a valid number.\n";
        continue;
    }

}

    return 0;
}