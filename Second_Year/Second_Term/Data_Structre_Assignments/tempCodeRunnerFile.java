#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;

void readFile(const string& filePath, int& degree1, vector<int>& coefficients1, int& degree2, vector<int>& coefficients2) {
    ifstream file(filePath);
    if (!file) {
        cerr << "Error: File not found.\n";
        return;
    }

    string content, line;
    while (getline(file, line)) {
        content += line + "\n";  // Read file content into a string
    }

    if (content.empty()) {
        cerr << "Error: File content is empty.\n";
        return;
    }

    istringstream iss(content);
    
    // Extract first polynomial
    iss >> degree1;
    coefficients1.resize(degree1 + 1);
    for (int i = 0; i <= degree1; i++) {
        iss >> coefficients1[i];
    }

    // Extract second polynomial
    iss >> degree2;
    coefficients2.resize(degree2 + 1);
    for (int i = 0; i <= degree2; i++) {
        iss >> coefficients2[i];
    }

    file.close();
}

int main() {
    string filePath = "example.txt";
    int degree1, degree2;
    vector<int> coefficients1, coefficients2;

    readFile(filePath, degree1, coefficients1, degree2, coefficients2);

    // Output the extracted data
    cout << "First polynomial degree: " << degree1 << "\nCoefficients: ";
    for (int coeff : coefficients1) {
        cout << coeff << " ";
    }
    cout << "\n";

    cout << "Second polynomial degree: " << degree2 << "\nCoefficients: ";
    for (int coeff : coefficients2) {
        cout << coeff << " ";
    }
    cout << "\n";

    return 0;
}
