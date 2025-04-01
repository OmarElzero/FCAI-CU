#include <bits/stdc++.h>
using namespace std;

class Polynomial {
private:
    int order;
    int equality;
    int* coefficients;


public:
    Polynomial(int degree) {
        order = degree;
        coefficients = new int[order + 1]();
        equality = 0;
    }

    ~Polynomial() {
        delete[] coefficients;
    }

    void input_coff() {
        cout<<"Enter Polynomial: ";
        for (int i = 0; i <= order; i++) {
            if (i==0){
                cin >> equality;
            }
            cin >> coefficients[i];
        }
    }

    void display_poly() const {
        bool flag = true;
        for (int i = order; i >= 0; i--) {
            if (flag || coefficients[i] != 0 || i == 0) {
                if (!flag){
                    if(coefficients[i]>=0){
                        cout<<" + ";
                    }
                    else{
                        cout<<" - ";
                    }
                }
                else if(coefficients[i]<0){
                    cout<<" - ";
                }

                cout << abs(coefficients[i]);
                if (i > 1) cout << "x^" << i;
                else if (i == 1) cout << "x";

                flag = false;
            }
        }
        cout << " = " << equality << endl;
    }

    Polynomial operator+(const Polynomial& other)  {
        int deg_final;
        if(order >= other.order){
            deg_final=order;
        }
        else{
            deg_final=other.order;
        }
        Polynomial final_equ(deg_final);
        final_equ.equality = equality + other.equality;

        for (int i = 0; i <= deg_final; i++) {
            int poly_1 , poly_2;
            if(i<=order){
                poly_1 = coefficients[i];
            }
            else{
                poly_1 = 0;
            }
            if (i <= other.order) {
                poly_2 = other.coefficients[i];
            }
            else{
                poly_2 =0;
            }
            final_equ.coefficients[i] = poly_1 + poly_2;
        }
        return final_equ;
    }

    Polynomial operator-(const Polynomial& other) {
        int deg_final;
        if(order >= other.order){
            deg_final=order;
        }
        else{
            deg_final=other.order;
        }
        Polynomial final_equ(deg_final);
        final_equ.equality = other.equality - equality;

        for (int i = 0; i <= deg_final; i++) {
            int poly_1 , poly_2;
            if(i<=order){
                poly_1 = coefficients[i];
            }
            else{
                poly_1 = 0;
            }
            if (i <= other.order) {
                poly_2 = other.coefficients[i];
            }
            else{
                poly_2 =0;
            }
            final_equ.coefficients[i] = poly_2 - poly_1;
        }
        return final_equ;
    }

    static bool readPolynomialsFromFile(const string& filePath, Polynomial*& poly1, Polynomial*& poly2) {
        ifstream file(filePath);
        if (!file) {
            cerr << "Error: Unable to open file.\n";
            return false;
        }

        int deg1, deg2, eq1, eq2;

        file >> deg1;
        poly1 = new Polynomial(deg1);
        for (int i = 0; i <= deg1; i++) {
            file >> poly1->coefficients[i];
        }
        file >> poly1->equality;

        file >> deg2;
        poly2 = new Polynomial(deg2);
        for (int i = 0; i <= deg2; i++) {
            file >> poly2->coefficients[i];
        }
        file >> poly2->equality;

        file.close();
        return true;
    }
};

int main() {

    Polynomial* poly1 = nullptr;
    Polynomial* poly2 = nullptr;

    string filePath = "/root/FCAI-CU/Second_Year/Second_Term/Data_Structre_Assignments/First_Assignment/example.txt";

    if (Polynomial::readPolynomialsFromFile(filePath, poly1, poly2)) {
        cout << "Polynomial 1: ";
        poly1->display_poly();

        cout << "Polynomial 2: ";
        poly2->display_poly();

        Polynomial sum = *poly1 + *poly2;
        cout << "Sum: ";
        sum.display_poly();

        Polynomial diff = *poly1 - *poly2;
        cout << "Difference: ";
        diff.display_poly();
    }

    delete poly1;
    delete poly2;


    return 0;
}
