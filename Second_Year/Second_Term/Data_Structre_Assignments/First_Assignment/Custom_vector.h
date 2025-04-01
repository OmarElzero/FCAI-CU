#ifndef C_U_S_T_O_M__V_E_C_T_O_R__H
#define C_U_S_T_O_M__V_E_C_T_O_R__H

#include <bits/stdc++.h>
#include <string>
#include <curl/curl.h>
using namespace std;

    


class Guest {
    
    public:
    string name;
    string contact;
    string iftar_date;
    Guest(){
        name = "";
        contact = "";
        iftar_date = "";
    }
    Guest(string name, string contact, string iftar_date){
        this->name = name;
        this->contact = contact;
        this->iftar_date = iftar_date;
    }
    void display_guest();
    string update_invitation(string new_date);

    void send_reminder(string date);

    Guest(const Guest &guest){
        this->name = guest.name;
        this->contact = guest.contact;
        this->iftar_date = guest.iftar_date;
    }
    Guest& operator=(const Guest &guest){
        if (this != &guest) {
            this->name = guest.name;
            this->contact = guest.contact;
            this->iftar_date = guest.iftar_date;
        }
        return *this;
    }
};

class Node{

    Node *next;
    Node *prev;
    Guest value;
    public:
    Node(){
        next = NULL;
        prev = NULL;
    }

void add_at_begining(Guest value, Node **head, Node **tail);
void add_at_end(Guest value, Node **head, Node **tail);
void add_at_index(Guest value, int index, Node **head, Node **tail);
void free_list(Node **head);
void print_list(Node *head);
void update_date(string new_date,Node *head);
void remove_at_index(int index, Node **head, Node **tail);
void remove_with_name(Guest guest, Node **head, Node **tail);
void print_specific_guest(Guest guest, Node *head);
void update_specific_date(Guest guest, string new_date, Node *head);
void send_reminder_node(string date, Node *head);
void sort_guest_list(Node *head);



friend class Guest;



};




///////////////////////////////////////////////////////Class IftarManager Functions/////////////////////////////////////////

////////////////////////////////////////// node implemntition ////////////////////////////////////



void Node::add_at_begining(Guest value, Node **head, Node **tail) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node == NULL) {
        return;
    }


    new_node->value = value;
    new_node->next = NULL;
    new_node->prev = NULL;

    if (*head == NULL) {
       
        *head = new_node;
        *tail = new_node;
    } else {
       
        new_node->next = *head;
        (*head)->prev = new_node;
        new_node->prev = NULL; 
        *head = new_node;      
    }
}
void Node::add_at_end(Guest value, Node **head, Node **tail) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node == NULL) {
        return;
    }


    new_node->value = value;
    new_node->next = NULL;
    new_node->prev = NULL;

    if (*head == NULL) {
       
        *head = new_node;
        *tail = new_node;
    } else {
       
        new_node->next = NULL;
        (*tail)->next = new_node;
        new_node->prev = *tail; 
        *tail = new_node;      
    }
}

void Node::add_at_index(Guest value, int index, Node **head, Node **tail) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node == NULL) {
        return;
    }

    new_node->value = value;
    new_node->next = NULL;
    new_node->prev = NULL;

    if (*head == NULL) {
        *head = new_node;
        *tail = new_node;
    } else {
        Node *temp = *head;
        for (int i = 0; i < index - 1; i++) {
            if (temp->next == NULL) {
                return;
            }
            temp = temp->next;
        }
        new_node->next = temp->next;
        new_node->prev = temp;
        temp->next = new_node;
        if (new_node->next != NULL) {
            new_node->next->prev = new_node;
        }
    }
}

void Node::free_list(Node **head) {
    Node *temp = *head;
    while (temp != NULL) {
        Node *next = temp->next;
        free(temp);
        temp = next;
    }
    *head = NULL;
}

void Node::print_list(Node *head) {
    Node *temp = head;
    while (temp != NULL) {
        cout << "Name: " << temp->value.name << endl;
        cout << "Contact: " << temp->value.contact << endl;
        cout << "Iftar Date: " << temp->value.iftar_date << endl;
        temp = temp->next;
    }
    printf("\n");
}

void Node::update_date(string new_date,Node *head) {
    Node *temp = head;
    while (temp != NULL) {
        temp->value.iftar_date = new_date;
        temp = temp->next;
    }
    printf("\n");
}

void Node::remove_at_index(int index, Node **head, Node **tail) {
    if (*head == NULL) {
        return;
    }
    Node *temp = *head;
    if (index == 0) {
        *head = temp->next;
        free(temp);
        return;
    }
    for (int i = 0; temp != NULL && i < index - 1; i++) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    Node *next = temp->next->next;
    free(temp->next);
    temp->next = next;
}
void Node::remove_with_name(Guest guest, Node **head, Node **tail) {
    if (*head == NULL) {
        return;
    }
    Node *temp = *head;
// if head and there more than one node
    if (guest.name == temp->value.name) {
        *head = temp->next;
        free(temp);
        return;
    }
    // if head and there is only one node
    if (guest.name == temp->value.name && temp->next == NULL) {
        *head = NULL;
        *tail = NULL;
        free(temp);
        return;
    }
    
    for (int i = 0; temp != NULL && guest.name != (temp->next)->value.name; i++ ) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    Node *next = temp->next->next;
    free(temp->next);
    temp->next = next;
    next->prev = temp;
    
}
void Node::update_specific_date(Guest guest, string new_date, Node *head) {
    if (head == NULL) {
        return;
    }
    Node *temp = head;
    
// if head
    if (guest.name == temp->value.name) {
        temp->value.iftar_date = new_date;
        return;
    }
   
    //else 
    for (int i = 0; temp != NULL && guest.name != (temp->next)->value.name; i++ ) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    Node *next = temp->next->next;
    temp->next->value.iftar_date = new_date;    
}
void Node::print_specific_guest(Guest guest, Node *head) {
    if (head == NULL) {
        return;
    }
    Node *temp = head;
    
// if head
    if (guest.name == temp->value.name) {
       cout << "Name: " << temp->value.name << endl;
        cout << "Contact: " << temp->value.contact << endl;
        cout << "Iftar Date: " << temp->value.iftar_date << endl;
        return;
    }
   
    //else 
    for (int i = 0; temp != NULL && guest.name != (temp->next)->value.name; i++ ) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    Node *next = temp->next->next;
   cout << "Name: " << temp->next->value.name << endl;
        cout << "Contact: " << temp->next->value.contact << endl;
        cout << "Iftar Date: " << temp->next->value.iftar_date << endl;    
}

void Node::send_reminder_node(string date, Node *head) {
    if (head == NULL) {
        return;
    }
    Node *temp = head;
    cout << "----------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
    cout << "| Guest Name | Iftar_Date for this guest| Message                                                                                                   |" << endl;                 
    cout << "----------------------------------------------------------------------------------------------------------------------------------------------------" << endl; 
    while (temp != NULL) {
        if (temp->value.iftar_date == date) {
            string message = "Dear " + temp->value.name + ",You are invited to the iftar on " + temp->value.iftar_date + ".Please make sure to be on time.";
            int name_length = temp->value.name.length();
            int date_length = temp->value.iftar_date.length();
            int message_length = message.length();

            int max_name_length = 0;
            int max_date_length = 0;
            int max_message_length = 0;

            // Determine the maximum lengths
            Node *temp_max = head;
            while (temp_max != NULL) {
                int name_length = temp_max->value.name.length();
                int date_length = temp_max->value.iftar_date.length();
                string message = "Dear " + temp_max->value.name + ",You are invited to the iftar on " + temp_max->value.iftar_date + ".Please make sure to be on time.";
                int message_length = message.length();

                if (name_length > max_name_length) {
                    max_name_length = name_length;
                }
                if (date_length > max_date_length) {
                    max_date_length = date_length;
                }
                if (message_length > max_message_length) {
                    max_message_length = message_length;
                }

                temp_max = temp_max->next;
            }

            cout << "| " << temp->value.name << string(max_name_length - name_length, ' ')
                 << " | " << temp->value.iftar_date << string(max_date_length - date_length, ' ')
                 << " | " << message << string(max_message_length - message_length, ' ')
                 << " |" << endl;
        }
        temp = temp->next;
    }
    cout << "----------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
}

void Node::sort_guest_list(Node* head) {
    if (!head) return;

    Node* current = head;
    while (current) {
        Node* next = current->next;
        while (next) {
            if (current->value.iftar_date > next->value.iftar_date) {
                // swap(current->value, next->value);
                Guest temp = current->value;
                current->value = next->value;
                next->value = temp;
            }
            next = next->next;
        }
        current = current->next;
    }
}



#endif //C_U_S_T_O_M__V_E_C_T_O_R__H