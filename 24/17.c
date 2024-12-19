#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COMBO(op) ((op) < (4) ? (op) : (((op) < (5) ? (A) : (((op) < (6) ? (B) : (C))))))

static unsigned long long A = 0;
static unsigned long long B = 0;
static unsigned long long C = 0;
static unsigned long long I = 0;
static uint8_t OUTPUT[256];
static uint8_t OUTPUT_IND = 0;
static uint8_t PROGRAM[] = {
    2,4, // bst A   |  B = (A & 0b111)
    1,3, // bxl 3   |  B = (B ^ 0b011)
    7,5, // cdv B   |  C = (A >> B)
    4,1, // bxc     |  B = (B ^ C)
    1,3, // bxl 3   |  B = (B ^ 0b011)
    0,3, // adv 3   |  A = (A >> 3)
    5,5, // out B   |  print(B & 0b111)
    3,0  // jnz 0   |  loop to start
};
// print((((((A & 0b111)) ^ 0b011) ^ (A >> (((A & 0b111)) ^ 0b011))) ^ 0b011) & 0b111)
// print((A3 ^ (A >> (A3 ^ 0b011))) & 0b111), where A3 is the final 3 bits of A

inline void adv(uint8_t operand){
    A >>= COMBO(operand);
}

inline void bxl(uint8_t operand){
    B ^= operand;
}

inline void bst(uint8_t operand){
    B = COMBO(operand) & 0b111;
}

inline void jnz(uint8_t operand){
    if (A){
        I = operand;
    }
}

inline void bxc(uint8_t operand){
    B ^= C;
}

inline void out(uint8_t operand){
    OUTPUT[OUTPUT_IND++] = COMBO(operand) & 0b111;
}

inline void bdv(uint8_t operand){
    B = A >> COMBO(operand);
}

inline void cdv(uint8_t operand){
    C = A >> COMBO(operand);
}

static void (*INSTRUCTIONS[8])(uint8_t) = {&adv, &bxl, &bst, &jnz, &bxc, &out, &bdv, &cdv};

void run(){
    uint8_t opc, opr;
    while (I < sizeof(PROGRAM)){
        opc = PROGRAM[I++];
        opr = PROGRAM[I++];
        INSTRUCTIONS[opc](opr);
    }
}

void reset(){
    A = 0;
    B = 0;
    C = 0;
    I = 0;
    OUTPUT_IND = 0;
}

void print_output(){
    for(int i = 0; i < OUTPUT_IND; i++){
        printf("%u,", OUTPUT[i]);
    }
    printf("\n");
}

int main(){
    reset();
    A = 37283687;
    run();
    print_output();

    reset();
    // This number is found by analyzing the bytecode, and using the script below
    A = 108107566389757;
    run();
    print_output();
    return 0;
}

/*
def merge_bits(a: bool, b: bool, c: bool) -> int:
    return (a << 2) + (b << 1) + (c)

def test(A: int, target: int):
    out = []
    for a in [False, True]:
        for b in [False, True]:
            for c in [False, True]:
                # Analyzing the bytecode gave this equation
                val = merge_bits(a, b, c) ^ (((A << 3) + merge_bits(a, b, c)) >> merge_bits(a, not b, not c))
                val &= 7
                if val == target:
                    out.append(merge_bits(a, b, c))
    return out

q = [(0, [2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0][::-1])]
while q:
    A, targets = q.pop(0)
    potential = test(A, targets[0])
    if not potential:
        continue
    if len(targets) == 1:
        for p in potential:
            print("Done", (A << 3) + p)
    else:
        for p in potential:
            q.append((
                (A << 3) + p,
                targets[1:]
            ))
*/
