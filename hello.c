int main() {
  asm(	"li a1,0x100000;"
  	"lw a2,0(a1);"
  );
  return 0;
}
