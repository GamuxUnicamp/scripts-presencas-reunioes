from pathlib import Path
import subprocess
mydir = Path(".")

with open("./saida.md", 'w', encoding='utf-8') as arquivo_saida:
	for file in mydir.glob('pautas-md/*.md'):
		file = file.absolute()
		print(f"{file}")

		with open(str(file), 'r', encoding='utf-8') as md_file:
			linhas = md_file.readlines()[:10]
			
		#arquivo_saida.write(f'[=]=====================================================================\n')
		arquivo_saida.write(f'[>] {file.name}\n')
		#arquivo_saida.write(f'[=].....................................................................\n')
		arquivo_saida.writelines(linhas)
		arquivo_saida.write('\n\n')  
		print()