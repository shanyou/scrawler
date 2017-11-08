import re
import os

text = """
\nsetTimeout("ajax_post(\'book\',\'ajax\',\'pinyin\',\'zhaogenanguidangxifu\',\'id\',\'156\',\'sky\',\'441d4901047fa09f5ce01acaa441fdf1\',\'t\',\'1510117382\')","1000");\n
"""

pattern = re.compile(r'pinyin\',\'([^\']+)')
match = pattern.findall(text)
print match


d = os.path.join(os.getcwd(), "a", "b")
print d