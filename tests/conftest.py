import os
import sys

# Adicionar o diretório raiz ao path para que pytest encontre os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
