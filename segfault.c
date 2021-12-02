int main() {
  asm(	"li a1,0xFFFF;"
  	    "lw a2,0(a1);"
  );
  return 0;
}
