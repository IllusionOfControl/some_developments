#include <stdio.h>

int summ(int*);

int main() {

}

int summ(int* n) {
    int summ;
    for (int i = 0; i<&n; i++)
        summ+=&n * (n-1)+1+2*i;
    return summ;
}