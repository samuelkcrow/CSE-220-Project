int main() {
  asm(	"li a1,0x10000;"
  	    "lw a2,0(a1);"
  );
  return 0;
}
