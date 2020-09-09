#include <stdio.h>
#include <stdlib.h>

void readStrF(char * data, int size, char *filename) {
    FILE * file;
    data = malloc(sizeof(char)*size);
    if ((file=fopen(filename, "rb"))!=NULL)
        fgets(data, size, file);
    fclose(file);
}

int main(int argc, char const *argv[])
{
    char * text;
    readStrF(text, 256, "text.txt");
    for (int i=0; (sizeof(text)/sizeof(char))>i; i++)
        printf("%c", text[i]);
    return 0;
}

#define true 1
#define bool int




bool getWIFI() {
    printf("I NEED WIFI");
    printf("I NEED HABR");
    printf("I NEED CODE </>");
    return true;
}