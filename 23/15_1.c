#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    uint64_t label;
    uint8_t focal_length;
    void *next;
} Box;

static uint8_t current_value = 0;

void hash(uint8_t in){
    current_value += in;
    current_value *= 17;

}

void reset(){
    current_value = 0;
}

void task_1(){
    FILE *fptr;
    fptr = fopen("15", "r");

    uint64_t sum = 0;

    char c = '_';
    do
    {
        c = fgetc(fptr);
        // printf("%c", c);
        if ((c == ',') | (c == '\n')){
            // printf("\n%i\n", current_value);
            sum += current_value;
            reset();
        }
        else {
            hash(c);
        }
    } while (c != '\n');
    
    fclose(fptr);

    printf("\n%i\n", sum);

    reset();
}

void task_2(){

    Box boxes[256];
    for (int i = 0; i < 256; i++){
        boxes[i].label = 0;
        boxes[i].focal_length = 0;
        boxes[i].next = NULL;
    }

    FILE *fptr;
    fptr = fopen("15_test", "r");

    char c = '_';
    uint64_t label = 0;
    do
    {
        c = fgetc(fptr);
        if (c == '='){
            c = fgetc(fptr);
            Box *box = &boxes[current_value];
            int found = 0;
            while (box->next != NULL){
                if (box->label == label){
                    box->focal_length = c - '0';
                    found = 1;
                    break;
                }
                box = box->next;
            }
            if (!found){
                Box new;
                new.label = label;
                new.focal_length = c - '0';
                new.next = NULL;
                box->next = &new;
            }
        }
        else if (c == '-'){
            Box *box = &boxes[current_value];
            Box *prev = box;
            while (box->next != NULL){
                if (box->label == label){
                    prev->next = box->next;
                    break;
                }
                prev = box;
                box = box->next;
            }
        }
        else if ((c == ',') | (c == '\n')){
            reset();
            label = 0;
        }
        else {
            label <<= 8;
            label += c;
            hash(c);
        }
    } while (c != '\n');
    
    fclose(fptr);

    printf("Made it\n");

    uint64_t sum = 0;
    for (int i = 0; i < 256; i++){
        Box box = boxes[i];
        int ind = 0;
        while (box.next != NULL){
            sum += (i + 1) * box.focal_length;
            box = *(Box *)box.next;
        }
    }

    printf("\n%i\n", sum);
}

int main(){
    task_1();
    // task_2();
    return 0;
}
