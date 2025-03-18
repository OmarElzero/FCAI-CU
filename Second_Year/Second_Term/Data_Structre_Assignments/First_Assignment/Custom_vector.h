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
    Guest() {
        name = "";
        contact = "";
        iftar_date = "";
    }
    Guest(string name, string contact, string iftar_date) {
        this->name = name;
        this->contact = contact;
        this->iftar_date = iftar_date;
    }
    void display_guest();
    string update_invitation(string new_date);
    void send_reminder(string date);
};

class Node {
    Node *next;
    Node *prev;
    Guest value;
public:
    Node() {
        next = NULL;
        prev = NULL;
    }

    void add_at_begining(Guest value, Node **head, Node **tail);
    void add_at_end(Guest value, Node **head, Node **tail);
    void add_at_index(Guest value, int index, Node **head, Node **tail);
    void free_list(Node **head);
    void print_list(Node *head);
    void update_date(string new_date, Node *head);
    void remove_at_index(int index, Node **head, Node **tail);
    void remove_with_name(Guest guest, Node **head, Node **tail);
    void print_specific_guest(Guest guest, Node *head);
    void update_specific_date(Guest guest, string new_date, Node *head);
    void send_reminder_node(string date, Node *head);
    void send_email(const std::string& recipient, const std::string& subject, const std::string& message);

    friend class Guest;
};

void Node::add_at_begining(Guest value, Node **head, Node **tail) {
    Node *new_node = new Node();
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
    Node *new_node = new Node();
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
    Node *new_node = new Node();
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
        delete temp;
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

void Node::update_date(string new_date, Node *head) {
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
        delete temp;
        return;
    }
    for (int i = 0; temp != NULL && i < index - 1; i++) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    Node *next = temp->next->next;
    delete temp->next;
    temp->next = next;
    if (next != NULL) {
        next->prev = temp;
    }
}

void Node::remove_with_name(Guest guest, Node **head, Node **tail) {
    if (*head == NULL) {
        return;
    }
    Node *temp = *head;
    if (guest.name == temp->value.name) {
        *head = temp->next;
        delete temp;
        return;
    }
    if (guest.name == temp->value.name && temp->next == NULL) {
        *head = NULL;
        *tail = NULL;
        delete temp;
        return;
    }
    for (int i = 0; temp != NULL && guest.name != (temp->next)->value.name; i++) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    Node *next = temp->next->next;
    delete temp->next;
    temp->next = next;
    if (next != NULL) {
        next->prev = temp;
    }
}

void Node::update_specific_date(Guest guest, string new_date, Node *head) {
    if (head == NULL) {
        return;
    }
    Node *temp = head;
    if (guest.name == temp->value.name) {
        temp->value.iftar_date = new_date;
        return;
    }
    for (int i = 0; temp != NULL && guest.name != (temp->next)->value.name; i++) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    temp->next->value.iftar_date = new_date;
}

void Node::print_specific_guest(Guest guest, Node *head) {
    if (head == NULL) {
        return;
    }
    Node *temp = head;
    if (guest.name == temp->value.name) {
        cout << "Name: " << temp->value.name << endl;
        cout << "Contact: " << temp->value.contact << endl;
        cout << "Iftar Date: " << temp->value.iftar_date << endl;
        return;
    }
    for (int i = 0; temp != NULL && guest.name != (temp->next)->value.name; i++) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        return;
    }
    cout << "Name: " << temp->next->value.name << endl;
    cout << "Contact: " << temp->next->value.contact << endl;
    cout << "Iftar Date: " << temp->next->value.iftar_date << endl;
}

void Node::send_reminder_node(string date, Node *head) {
    if (head == NULL) {
        return;
    }
    Node *temp = head;
    while (temp != NULL) {
        if (temp->value.iftar_date == date) {
            string message = "Dear " + temp->value.name + ",\nYou are invited to the iftar on " + temp->value.iftar_date + ".\nPlease make sure to be on time.";
            string recipient_email = temp->value.contact;
            string subject = "Iftar Invitation";
            send_email(recipient_email, subject, message);
        }
        temp = temp->next;
    }
}

void Node::send_email(const std::string& recipient, const std::string& subject, const std::string& message) {
    CURL* curl;
    CURLcode res;
    struct curl_slist* recipients = NULL;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "smtp://smtp.example.com:587");
        curl_easy_setopt(curl, CURLOPT_USE_SSL, CURLUSESSL_ALL);
        curl_easy_setopt(curl, CURLOPT_USERNAME, "your_email@example.com");
        curl_easy_setopt(curl, CURLOPT_PASSWORD, "your_password");

        curl_easy_setopt(curl, CURLOPT_MAIL_FROM, "your_email@example.com");

        recipients = curl_slist_append(recipients, recipient.c_str());
        curl_easy_setopt(curl, CURLOPT_MAIL_RCPT, recipients);

        std::string email_body = "To: " + recipient + "\r\n"
                                 "From: your_email@example.com\r\n"
                                 "Subject: " + subject + "\r\n"
                                 "\r\n" +
                                 message + "\r\n";

        curl_easy_setopt(curl, CURLOPT_READDATA, email_body.c_str());

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Failed to send email: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "Email sent successfully to " << recipient << std::endl;
        }

        curl_slist_free_all(recipients);
        curl_easy_cleanup(curl);
    }
}

#endif //C_U_S_T_O_M__V_E_C_T_O_R__H
