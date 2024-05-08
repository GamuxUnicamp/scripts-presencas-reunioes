
from math import ceil, sqrt
import pprint
import json
from pathlib import Path
from prettytable import PrettyTable 
from prettytable import MARKDOWN
import subprocess


with open("presencas-semi-estru-filtrada.md", 'r', encoding='utf-8') as md_file:
	linhas = md_file.readlines()
	strs_reunioes = "".join(linhas).split("---\n")
	desc_valor_reunioes = list(map(lambda a: a.split("[>]"), strs_reunioes))
	big_dict = {}
	for  valor in desc_valor_reunioes:
		ano, mes, nome = valor[0].split(" . ")
		dict_ano = big_dict.setdefault(ano.strip(), {})
		dict_mes = dict_ano.setdefault(mes.strip(), {})	

		str_listas = valor[1].strip().split("\n");
		listas = {}
		for str in str_listas:
			if str == "":
				continue
			nome_lista, nomes = str.split(":")
			listas[nome_lista.strip()] = nomes.split(",")
		dict_mes.setdefault(nome,listas)
#print(json.dumps(big_dict, indent=4, sort_keys=True))

print("# Detalhes:")
detalhes_finais = PrettyTable(["Ano", "Media", "DP", "CV"]) 
for (ano, valor) in big_dict.items():
	peso_valor = []
	print(f"## {ano}")
	qt_reunioes = 0;
	soma_maximos = 0;
	tabela_meses = PrettyTable(["Mes", "Qt. Reuniões", "Max. Presença ", "Max. Nome Reunião"]) 
	tabela_meses.set_style(MARKDOWN)
	tabela_meses.align["Mes"] = "l"
	tabela_meses.align["Max. Nome Reunião"] = "l";
	for (mes, valor_mes) in valor.items():
		maximo = 0
		nome_maximo=""
		for (nome, reuniao) in valor_mes.items():
			pessoas_presentes =  set()
			for lista in reuniao.values():
				for pessoa in lista:
					pessoas_presentes.add(pessoa);
			if maximo < len(pessoas_presentes):
				maximo = len(pessoas_presentes);
				nome_maximo = nome.strip()
		if(maximo == 0):
			continue
		tabela_meses.add_row([mes, len(valor_mes), maximo, nome_maximo[:-3]])

		qt_reunioes += len(valor_mes);
		soma_maximos += maximo*len(valor_mes);
		peso_valor.append([len(valor_mes), maximo])
	print(tabela_meses)
	#print(f"{ano}: {int(soma_maximos/qt_reunioes)}");
	

	media_uni = sum([ valor for (peso, valor) in  peso_valor])/len(peso_valor)
	dp_uni = sqrt(sum( [(a[1] - media_uni)**2 for a in peso_valor])/len(peso_valor))
	
	peso_total = sum([a[0] for a in  peso_valor])
	dp_factor = sqrt(sum([(peso/peso_total)**2 for (peso, _) in peso_valor])) 
	dp=dp_uni*dp_factor
	
	media = sum([ valor*peso for (peso, valor) in  peso_valor])/sum([ peso for (peso,_) in  peso_valor])
	#print(f'media: {int(round(media))}')
	#print(f'DP: {dp:.2f}')
	#print(f'CV: {dp/media*100:.2f}%')
	detalhes_finais.add_row([ano, int(round(media)),f'±{dp:.2f}',f'{dp/media*100:.2f}%'])
print()
print("# Resultado Final")
detalhes_finais.set_style(MARKDOWN)
print(detalhes_finais)