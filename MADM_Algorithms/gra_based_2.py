import ast
import sys

#pesos
delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda disponivel (em Mb)

attrd = ['delay','jitter','packet_loss','av_bandwidth']

def normalize_min(x,y):					#Funcao "quanto menos, melhor (Para criterios de custo)"
 if max(x) - min(x) != 0:
  m = (max(x) - y)/(max(x)- min(x))
 if max(x) - min(x) == 0:
  m = 1
 return m
	
def normalize_max(x,z):					#Funcao "quanto mais, melhor (Para criterios beneficos)"
 if max(x) - min(x) != 0:
  m = (z - 0)/(max(x)- 0)
 if max(x) - min(x) == 0:
  m = 1
 return m

def cr(difference_attr,zeta,g):
 if max(difference_attr) != 0:
  h = (min(difference_attr) + (zeta*(max(difference_attr))))/(g + (zeta*(max(difference_attr))))
  return h
 elif max(difference_attr) == 0:
  h = 1
  return h

ap_range = ast.literal_eval(sys.argv[2])
n = int(sys.argv[1]) #Leitura do numero de APS que serao executados.

l= [0] * n
q = [0] * n

for a in range(1,(int(n)+1)):
 if a in ap_range:
  num = a
  ap = "ap" + str(a) + ".txt"
  k = "ap" + str(a)
  a = open("APs/"+ap,"r")
  a = a.read()
  a = ast.literal_eval(a)
  l[num-1] = a
  exec("%s = %s" % ("attr",[]))
  for i in a:	
   exec("%s = %s" % (i,[]))
   exec("%s = %s" % (k,[]))
   exec("%s = %s" % (k + "_normalized",[]))
   exec("%s = %s" % (k + "_normalized_cr",[]))
   exec("%s = %s" % (i + "_normalized",[]))
   exec("%s = %s" % (i + "_normalized_r",[0] * n))

attr = attrd
attr.sort(key=len)
for z in range(1,(int(n)+1)):
 if z in ap_range:
  for ij in attrd:
   exec("ap" + str(z) + ".append(float(l[z-1][ij]))")
	#adicionando nas listas de rede (ap + numero) os valores dos atributos "ij" de cada rede.


for x in l:    #adicionando elementos nas listas dos atributos, usadas futuramente para definir os valores maximo e minimo de cada um.							
 if x != 0: 
  for b in x:
   if b == 'delay':
    delay.append(x[b])
   if b == 'jitter':
    jitter.append(x[b])
   if b == 'packet_loss':
    packet_loss.append(x[b])
   if b == 'av_bandwidth':
    av_bandwidth.append(x[b])


for i in range(1,len(l)+1):	#trecho do codigo onde sera feita a normalizacao e a aplicacao dos pesos.
 if i in ap_range:
  g = str(i)	#numero da rede que esta sendo analisada (em string, para ser usado nos comandos "exec").
  exec("z = ap" + g)
  for k in z:
   if z.index(k) == 0:
    m = float((normalize_min(delay,k)))
    exec("ap" + g + "_normalized.append(m)")
    delay_normalized.append(m)
   if z.index(k) == 1:
    m = (normalize_min(jitter,k))
    m = float(m)
    exec("ap" + g + "_normalized.append(m)")
    jitter_normalized.append(m)
   if z.index(k) == 2:
    m = (normalize_min(packet_loss,k))
    m = float(m)
    exec("ap" + g + "_normalized.append(m)")
    packet_loss_normalized.append(m)
   if z.index(k) == 3:
    m = float((normalize_max(av_bandwidth,k)))
    exec("ap" + g + "_normalized.append(m)")
    av_bandwidth_normalized.append(m)

zeta = 0.5

#print len(l)

for attr in attrd:		#series padroes (default series = "ds"), para calculo dos coeficientes relacionais
# exec("ds_" + attr + "= max(" + attr + "_normalized)")
 exec("ds_" + attr + "=1")

 exec("p = "+attr+"_normalized")
 exec("%s = %s" % ("difference_"+attr,[]))
 for ij_normalized in p:
  exec("f = ds_" + attr + " - ij_normalized")
  exec("difference_"+attr+".append(f)")
# 	exec ("print max(difference_"+attr+")")
 exec("h = difference_"+attr)
#  t = cr(h,zeta)
 c = 1
 d = 0
 for n in range(1,len(l)+1):
  if n in ap_range:      
   exec("o = difference_"+attr+"[d]")
   t = cr(h,zeta,o)
   if c != len(l):
     d = d + 1
   exec("ap"+str(n)+"_normalized_cr.append(t)")
   c = c + 1
  else:
   c = c + 1

for n in range(1,len(l)+1):
 if n in ap_range:
  b = str(n)
  exec("%s = %s" % ("ap"+b+"_score",[0,0,0,0]))
  exec("z = ap"+b+"_normalized_cr")
  exec("ap"+b+"_score[0]=z[0]*delay_weight")
  exec("ap"+b+"_score[1]=z[1]*jitter_weight")
  exec("ap"+b+"_score[2]=z[2]*packet_loss_weight")
  exec("ap"+b+"_score[3]=z[3]*av_bandwidth_weight")

for ap_number in range(1,(int(n)+1)):		#sera executada a soma dos atributos normalizados e com os pesos, dando a pontuacao final da rede
 if ap_number in ap_range:
  index = str(ap_number-1)
  ap_number = str(ap_number)
  exec("q["+ index + "]=(sum(ap" + ap_number + "_score))")

print(q) #Pontuacao de todas as redes avaliadas (na ordem numerica de 1 ate n).

print("rede " + str(q.index(max(q)) + 1))	#Melhor rede entre as candidatas
print("pontuacao da rede: " + str(max(q)))	#Pontuacao dessa rede
