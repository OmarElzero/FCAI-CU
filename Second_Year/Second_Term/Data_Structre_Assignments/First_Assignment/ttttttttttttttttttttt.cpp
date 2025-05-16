//ibrahim ayman ibrahim saif      الاحصاء الرياضي وعلوم الحاسب

#include <stack>
#include <queue>
#include <string>
#include <cctype>
#include <iostream>
using namespace std;

bool is_palindrome(const std::string &str) {
    std::stack<char> s;
    std::queue<char> q;

    // Push and enqueue only alphanumeric characters, ignoring case
    for (char ch : str) {
        if (std::isalnum(ch)) {
            char lower_ch = std::tolower(ch);
            s.push(lower_ch);
            q.push(lower_ch);
        }
    }

    // Compare stack and queue
    while (!s.empty() && !q.empty()) {
        if (s.top() != q.front()) {
            return false;
        }
        s.pop();
        q.pop();
    }

    return true;
}

class Node {
    public:
        int value;
        Node *next;
        Node *prev;
    
        Node() : value(0), next(nullptr), prev(nullptr) {}
    
        void add_at_beginning(int value, Node **head, Node **tail);
        void add_at_end(int value, Node **head, Node **tail);
        void remove_at_index(int index, Node **head, Node **tail);
        void print_list(Node *head);
    };
    
    void Node::add_at_beginning(int value, Node **head, Node **tail) {
        Node *new_node = new Node();
        new_node->value = value;
    
        if (*head == nullptr) {
            *head = new_node;
            *tail = new_node;
            new_node->next = new_node;
            new_node->prev = new_node;
        } else {
            new_node->next = *head;
            new_node->prev = (*tail);
            (*head)->prev = new_node;
            (*tail)->next = new_node;
            *head = new_node;
        }
    }
    
    void Node::add_at_end(int value, Node **head, Node **tail) {
        Node *new_node = new Node();
        new_node->value = value;
    
        if (*head == nullptr) {
            *head = new_node;
            *tail = new_node;
            new_node->next = new_node;
            new_node->prev = new_node;
        } else {
            new_node->next = *head;
            new_node->prev = *tail;
            (*tail)->next = new_node;
            (*head)->prev = new_node;
            *tail = new_node;
        }
    }
    
    void Node::remove_at_index(int index, Node **head, Node **tail) {
        if (*head == nullptr) return;
    
        Node *temp = *head;
    
        if (index == 0) {
            if (*head == *tail) {
                delete temp;
                *head = nullptr;
                *tail = nullptr;
            } else {
                *head = temp->next;
                (*head)->prev = *tail;
                (*tail)->next = *head;
                delete temp;
            }
            return;
        }
    
        for (int i = 0; temp != nullptr && i < index; i++) {
            temp = temp->next;
        }
    
        if (temp == nullptr) return;
    
        temp->prev->next = temp->next;
        temp->next->prev = temp->prev;
    
        if (temp == *tail) {
            *tail = temp->prev;
        }
    
        delete temp;
    }
    
    void Node::print_list(Node *head) {
        if (head == nullptr) return;
    
        Node *temp = head;
        do {
            cout << temp->value << " ";
            temp = temp->next;
        } while (temp != head);
        cout << endl;
    }

int main() {
    Node *head = NULL;
    Node *tail = NULL;



    Node().add_at_end(1, &head, &tail);
    Node().add_at_end(5, &head, &tail);
    Node().add_at_end(6, &head, &tail);

    // Make the queue circular
    if (head != NULL && tail != NULL) {
        tail->next = head;
        head->prev = tail;
    }

    // Print the circular queue
    cout << "Circular Queue:" << endl;
    Node *temp = head;
    if (temp != NULL) {
        do {
            cout << "data: " << temp->value << endl;
            temp = temp->next;
        } while (temp != head);
    }

    // Remove a guest from the circular queue
    cout << "\nRemoving Bob from the queue..." << endl;
    Node().remove_at_index(0, &head, &tail);
    // alwayes removes at 0 cause ist's a queue 

    // Update the circular links after removal
    if (head != NULL && tail != NULL) {
        tail->next = head;
        head->prev = tail;
    }

    // Print the updated circular queue
    cout << "\nUpdated Circular Queue:" << endl;
    temp = head;
    if (temp != NULL) {
        do {
            cout << "data: " << temp->value << endl;
            temp = temp->next;
        } while (temp != head);
    }

    // Free the circular queue
    cout << "\nFreeing the circular queue..." << endl;
    if (head != NULL) {
        Node *current = head;
        do {
            Node *next = current->next;
            free(current);
            current = next;
        } while (current != head);
    }
    head = NULL;
    tail = NULL;



    cout <<"Testing palindrome function" << endl;
    cout << "Enter a string: ";
    std::string input;
    std::getline(std::cin, input);
    if (is_palindrome(input)) {
        std::cout << "The string is a palindrome." << std::endl;
    } else {
        std::cout << "The string is not a palindrome." << std::endl;
    }
    cout << "----------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
    cout << "----------------------------------------------------------------------------------------------------------------------------------------------------" << endl; 

    return 0;
}
