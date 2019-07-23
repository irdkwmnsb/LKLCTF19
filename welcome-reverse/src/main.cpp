#include <iostream>
#include <string>


const char* x = "LKLCTF{bb6a6e787b4c94c5c760751680e7aa6c9cb4a4d7a5726c5d99c42a555b8b7d5b}";


int main()
{
    std::cout << "Enter username" << std::endl;
    std::string username;
    std::getline(std::cin, username);
    std::cout << "Enter password" << std::endl;
    std::string password;
    std::getline(std::cin, password);

    std::cout << "Bad username or password" << std::endl;
    return 1;
}
