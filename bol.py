import sys
import nltk
import math
import operator
import time

import numpy as np
import matplotlib.pyplot as plt

inicio = time.time()

def estruturar(ListaA,ListaDep):

	ListaB= []
	for j in range(0,len(ListaA)):
		if ListaA[j] not in ListaB:
			ListaB.insert(j,  ListaA[j])
	for j in range(0,len(ListaB)):
		if ListaB[j] not in ListaDep:
			ListaDep.append(ListaB[j])
	ListaDep.sort()		
	return ListaDep  

def aniquiladora(Lista,caracter,caracter2):
	x=0
	listaB = Lista[:]
	while(x < len(Lista)):
		if Lista[x] in caracter:
			listaB.remove(Lista[x])
		elif Lista[x] in caracter2:
			listaB.remove(Lista[x])
		x=x+1
	return listaB
def removeRadical(Lista):
	radical = nltk.stem.SnowballStemmer("english")
	p=0
	ListaB =[]
	while(p < len(Lista)):
		x= Lista[p]
		ListaB.insert(p, radical.stem(Lista[p]))
		p=p+1
	return ListaB

def consulta(arquivo):

	arquivo = open(arquivo,'r')
	linha = arquivo.read()
	arquivo.close()

	consulta = linha.split("NUMBER:")
	del consulta[0]
		
	for k in range(len(consulta)):
		lista=[]
		c = consulta[k].strip()
		indiceCorpo=c.find('TEXT:') + len("TEXT")
		fimCorpo = c.find('NUMBER OF RELEVANT DOCS:')
		indiceCorpo2= fimCorpo + len('NUMBER OF RELEVANT DOCS:')
		fimCorpo2 = c.find('RELEVANT DOCS AND SCORES:')
		indiceCorpo3 = fimCorpo2 + len('RELEVANT DOCS AND SCORES:')

		corpo = c[indiceCorpo:fimCorpo]
		for i in corpo:
			if i in ['1','2','3','4','5','6','7','8','9','0']:
				corpo = corpo.replace(i,' ')
		corpo = removeRadical(aniquiladora((nltk.word_tokenize (corpo.strip().lower().replace('\n',''))),caracters,stopwords))
		corpo2 = c[indiceCorpo2:fimCorpo2]
		corpo2 = corpo2.strip().lower().replace('\n','')
		corpo3 = c[indiceCorpo3:]
		
		corpo3 = corpo3.strip().lower().replace('\n','')
		
		corpo3 = corpo3.replace(' ','@').split('@@')
		for l in range(len(corpo3)):
			corpo3[l] = corpo3[l].replace(',1','').replace(',2','').replace(',3','').replace(',4','').replace(',5','').replace(',6','').replace(',7','').replace(',8','')
		
		dic_consulta[k]={'NUMBER': k+1 ,'TEXT':corpo,'NUMBER OF RELEVANT DOCS:':corpo2 ,'RELEVANT DOCS AND SCORES:':corpo3 }
		
def peso(palavras):
	MediaP0=MediaP10=MediaP20=MediaP30=MediaP40=MediaP50=MediaP60=MediaP70=MediaP80=MediaP90=MediaP100=0
	for i in range(len(dic_consulta)):#obter o vetor de peso de cada consulta.
		listaB=[]
		for k in range(len(dic_base)):
			lista=[]
			for j in dic_consulta[i]['TEXT']:
					if j in dic_base[k]:
						lista.append(1)
					else:
						lista.append(0)
			pesoq=sum(lista)/len(lista)
			if pesoq > 0.2:
				dic_peso[k]=pesoq
				tupla=(k+1,pesoq)
				listaB.append(tupla)
		listaB.sort(key=lambda x: x[1],reverse=True)		
		dic_pesofinal[i] = listaB
		x=1
		#print(listaB)
		for t in range(len(listaB)): #fazer a precisao e revocação
			numero=str(listaB[t][0])
			if numero in dic_consulta[i]['RELEVANT DOCS AND SCORES:']:
				precisao=round((x/(t+1))*100,1)
				revocacao=round((x/int(dic_consulta[i]['NUMBER OF RELEVANT DOCS:']))*100,1)
				x=x+1
				#print('\n')
				#print(precisao)
				#print(revocacao)
				if revocacao == 0:
					MediaP0+=(precisao/len(dic_consulta))
				elif revocacao == 10:
					MediaP10+=(precisao/len(dic_consulta))
				elif revocacao == 20:
					MediaP20+=(precisao/len(dic_consulta))
				elif revocacao == 30:
					MediaP30+=(precisao/len(dic_consulta))
				elif revocacao == 40:
					MediaP40+=(precisao/len(dic_consulta))
				elif revocacao == 50:
					MediaP50+=(precisao/len(dic_consulta))
				elif revocacao == 60:
					MediaP60+=(precisao/len(dic_consulta))
				elif revocacao == 70:
					MediaP70+=(precisao/len(dic_consulta))
				elif revocacao == 80:
					MediaP80+=(precisao/len(dic_consulta))
				elif revocacao == 90:
					MediaP90+=(precisao/len(dic_consulta))
				elif revocacao == 100:
					MediaP100+=(precisao/len(dic_consulta))

	#print(str(round((MediaP0),1))+' '+str(round(MediaP10,1))+' '+str(round(MediaP20,1))+' '+str(round(MediaP30,1))+' '+str(round(MediaP40,1))+' '+str(round(MediaP50,1))+' '+str(round(MediaP60,1))+' '+str(round(MediaP70,1))+' '+str(round(MediaP80,1))+' '+str(round(MediaP90,1))+' '+str(round(MediaP100,1)))				
	
	#plotando o grafico da funÃ§Ã£o exponencial no intervalo
	# 1 <= x <= 5
	#para isso, vamos construir um grafico linear por partes
	#com passo 0.1

	x = np.arange(0,110,10) #gera array onde elementos
	#seguem uma PA que comeÃ§a em 1.0 e vai atÃ© 5.1 (sem inlcuir
	#o 5.1) com passo 0.1

	y = np.array([round((MediaP0),1),round((MediaP10),1),round((MediaP20),1),round((MediaP30),1),round((MediaP40),1),round((MediaP50),1),round((MediaP60),1),round((MediaP70),1),round((MediaP80),1),round((MediaP90),1),round((MediaP100),1)])
	plt.xlabel('Revocação')
	plt.ylabel('Precisão')
	plt.title('Médias Precisão por Revocação')
	plt.legend(loc='best')
	plt.plot(x, y,'g.-') #a opÃ§Ã£o `g` faz a linha ficar verde
	plt.show()

def base(arquivo):
	arquivoX = open(arquivo,'r')
	arquivo = arquivoX.readlines()
	arquivoX.close()
	#abre a base e pega todas as palavras menos numeros e stopwords e add em uma lista o nome de cada arquivo 

	for i in range(len(arquivo)):
		arquivoR = open(arquivo[i].strip(),'r')
		linha = arquivoR.read()
		for k in linha:
			if k in ['1','2','3','4','5','6','7','8','9','0']:
				linha = linha.replace(k,' ')
		corpototal = removeRadical(aniquiladora(nltk.word_tokenize(linha),caracters,stopwords))
		dic_base[i]=(corpototal)
		palavrasestruturadas = estruturar(corpototal,ListaDep)
		#print(arquivo[i].strip('\n').strip('./base/'))
		NomedosArv.insert(i,arquivo[i].strip('\n').strip('./base/'))
	NumerodoArq.append(i)
	
	
	palavrasestruturadas=sorted(list(set(palavrasestruturadas)))
	#print(palavrasestruturadas)
	return palavrasestruturadas




dic_consulta = dict()
dic_base = dict()
dic_peso = dict()
dic_pesofinal = dict()


caracters = ['!','.','?',':','\n',';',',',' ','(',')',"''",'""','´´','``',"'",'$','#','@',"*",'+',"-",'_','...','<','=','>']
stopwords = nltk.corpus.stopwords.words('english')
indice={}

ListaDep =[]
NomedosArv=[]
NumerodoArq=[]

arquivo = sys.argv[1]
arquivo2 = sys.argv[2]
palavras=base(arquivo)
consulta(arquivo2)
peso(palavras)


fim = time.time()
print(fim - inicio)
