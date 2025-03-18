#include <bits/stdc++.h>
#include <curl/curl.h>

#include "Custom_vector.h"
using namespace std;
Node *head = NULL;
Node *tail = NULL;

class IftarManager{
   
    public:
    IftarManager(){
        head = NULL;
        tail = NULL;
    }
    Node guest_list = *head;
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
    guest_list.add_at_begining(guest, &head, &tail);
}
void IftarManager::display_all_guests(){
    guest_list.print_list(head);
    
}
void IftarManager::update_guest_invitation(string name, string new_date){
guest_list.update_specific_date(Guest(name,"hh","ff"), new_date, head);

}
void IftarManager::send_reminder(string date){
    guest_list.send_reminder_node(date, head);
}
void IftarManager::sort_guest_list(){
    // guest_list.sort_guest_list(head);
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
    cout << "2.Exit\n";
    int x;
    cin >> x;
    if (x==1){
        cout << "What do you wanna do ?\n";
        cout << "1.add a guest\n";
        cout << "2.delete a guest\n";
        cout << "3.print all guests\n";
        cout << "4.print specific guest details\n";
        cout << "5.ubdate date for all guests\n";
        cout << "6.ubdate date for specific guest\n";
        cout << "7.send a reminder to all guests\n";
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
            iftarManager.add_guest(Guest(name,"df","df"));       
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
            head->send_reminder_node(iftar_date, head);
            break;
        default:
            cout << "Invalid choice! Please enter a valid number.\n";
            break;
        }
        continue;
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