#include <stdio.h>
int main(){
    getLast1byte(0x89ABCDEF);
    getFirst3bytes(0x76543210);
}
void getLast1byte(unsigned int hex){
    printf("%02x", hex & 0x000000FF);

}
void getFirst3bytes(unsigned int hex){
    printf("%02x", hex & 0xFFFFFF00);
}