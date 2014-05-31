"Pastabin, mmm pasta"

import sys

# Add extras to sys.path:
#  - lib/: our code
#  - distlib/: 3rd party code (buildout)
#  - distlib.zip: 3rd party code w/ zipimport
sys.path[:0] = [v for v in ('lib', 'distlib', 'distlib.zip')
                if v not in sys.path]
