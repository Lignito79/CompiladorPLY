#
# José Ángel Rentería Campos // A00832436
#

from collections import defaultdict

semanticCube = defaultdict(lambda: defaultdict(dict))

# Solo enteros
semanticCube['int']['int']['*'] = 'int'
semanticCube['int']['int']['/'] = 'int'
semanticCube['int']['int']['+'] = 'int'
semanticCube['int']['int']['-'] = 'int'
semanticCube['int']['int']['>'] = 'bool'
semanticCube['int']['int']['<'] = 'bool'
semanticCube['int']['int']['!='] = 'bool'

# Flotante
semanticCube['float']['float']['*'] = 'float'
semanticCube['float']['float']['/'] = 'float'
semanticCube['float']['float']['+'] = 'float'
semanticCube['float']['float']['-'] = 'float'
semanticCube['float']['float']['>'] = 'bool'
semanticCube['float']['float']['<'] = 'bool'
semanticCube['float']['float']['!='] = 'bool'

# Entero y flotante
semanticCube['int']['float']['*'] = 'float'
semanticCube['float']['int']['*'] = 'float'
semanticCube['int']['float']['/'] = 'float'
semanticCube['float']['int']['/'] = 'float'
semanticCube['int']['float']['+'] = 'float'
semanticCube['float']['int']['+'] = 'float'
semanticCube['int']['float']['-'] = 'float'
semanticCube['float']['int']['-'] = 'float'
semanticCube['int']['float']['>'] = 'bool'
semanticCube['float']['int']['>'] = 'bool'
semanticCube['int']['float']['<'] = 'bool'
semanticCube['float']['int']['<'] = 'bool'
semanticCube['int']['float']['!='] = 'bool'
semanticCube['float']['int']['!='] = 'bool'