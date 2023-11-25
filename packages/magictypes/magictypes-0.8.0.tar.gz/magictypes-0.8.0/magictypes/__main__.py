import sys
from magictypes import annotate_types

if len(sys.argv) < 2:
    print('Try: python3 -m magictypes <script.py>')
    sys.exit()

scripts = [open(arg).read() for arg in sys.argv[1:]]
[print(annotate_types(s).replace('\n\n','')) for s in scripts]