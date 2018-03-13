for i in {1..21}; do python3 Parser.py t$i-correct.c; done
for i in {1..21}; do ./Parser t$i-correct.c; done
rm *.ast
rm Parser_ast_t*
for i in {1..21}; do diff -u cfg_filet$i-correct.c.txt t$i-correct.c.cfg | wc -l; done
