import ast
import sys
import math
import operator
import functools

#pesos
delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

def normalize_min(x,y):					#Funcao "quanto menos, melhor (Para criterios de custo)"
 if max(x) - min(x) != 0:
  m = (min(x)/y)
 if max(x) - min(x) == 0:
  m = 1
 return m
	
def normalize_max(x,z):					#Funcao "quanto mais, melhor (Para criterios beneficos)"
 if max(x) - min(x) != 0:
  m = (z/max(x))
 if max(x) - min(x) == 0:
  m = 1
 return m

ap_range = ast.literal_eval(sys.argv[2])
#ap_range = [1,2]
n = int(sys.argv[1])
#n = input("Quantos APs? ") #Leitura do numero de APS que serao executados.

p = [0] * n	#Armazenara as pontuacoes de cada rede
p2 = [0] * n
l = [0] * n

print (ap_range)

print (l)
#for a in range(1,(int(n)+1)):
for a in ap_range:			#Trecho de codigo para a leitura dos arquivos de texto (com dados dos APs).
 num = a
 ap = "ap" + str(a) + ".txt"
 k = "ap" + str(a)
 with open("APs/"+ap,"r") as a:
  a = a.read()
 a = ast.literal_eval(a)
# print (a)
# l.append(a)
 l[num-1]=a
 exec("%s = %s" % ("attr",[]))
 for i in a:	
  exec("%s = %s" % (i,[]))
  exec("%s = %s" % (k,[]))
  exec("%s = %s" % (k + "_normalized",[]))
  exec("%s = %s" % (k + "_normalized_2",[]))
  exec("%s = %s" % (k + "_normalized_m2ew",[]))

#for attributes in l[0]:
# attr.append(attributes)
attr=['delay','jitter','packet_loss','av_bandwidth']
attr.sort(key=len)

#print (l)

for z in range(1,(int(n)+1)):
 if z in ap_range:
  print (l[(z-1)])
  for q in attr:
   exec("ap" + str(z) + ".append(float(l[z-1][q]))")

#Criacao de listas de acordo com os atributos (delay, jitter, packet loss (perda de pacotes) e av_bandwidth (largura de banda disponivel).	
for x in l:
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

print (delay)

for i in range(1,len(l)+1):			#Normalizacao e multiplicacao pelos pesos
 if i in ap_range:
  g = str(i)
  exec("z = ap" + g)
  print (z)
  for k in z:
   if z.index(k) == 0:
    w = normalize_min(delay,k)
    exec("ap" + g + "_normalized.append(w)")
   if z.index(k) == 1:
    w = normalize_min(jitter,k)
    exec("ap" + g + "_normalized.append(w)")
   if z.index(k) == 2:
    w = normalize_min(packet_loss,k)
    exec("ap" + g + "_normalized.append(w)")
   if z.index(k) == 3:
    print (k)
    w = normalize_max(av_bandwidth, k)
    exec("ap" + g + "_normalized.append(w)")


for i in range(1,len(l)+1):			#Normalizacao e multiplicacao pelos pesos
 if i in ap_range:
  g = str(i)
  exec("z = ap" + g + "_normalized")
  print (z)
  for k in z:
   if z.index(k) == 0:
    m = k**delay_weight
    exec("ap" + g + "_normalized_2.append(m)")
   if z.index(k) == 1:
    m = k**jitter_weight
    exec("ap" + g + "_normalized_2.append(m)")
   if z.index(k) == 2:
    m = k**packet_loss_weight
    exec("ap" + g + "_normalized_2.append(m)")
   if z.index(k) == 3:
    m = k**av_bandwidth_weight
    exec("ap" + g + "_normalized_2.append(m)")

print (ap2_normalized_2)

for ap_number in range(1,(int(n)+1)):		#Soma das pontuacoes individuais de cada atributo, para dar a pontuacao final de cada rede.
 if ap_number in ap_range:
  str_index = str(ap_number-1)
  ap_number = str(ap_number)
#  exec("p.append(sum(ap" + ap_number + "_normalized))")
  exec("p["+ str_index +"]=functools.reduce(operator.mul, ap" + ap_number + "_normalized_2)")
for i in range(1,n+1):
  if i in ap_range:
    print (i)
#  else:
#    p[i-1] = 0
#    print (p[i-1])

for nn in range(1,(int(n)+1)):
 if nn in ap_range:
  str_in = str(nn - 1)
  nn1 = str(nn)
  for nn2 in ap_range:
   if nn2 != nn:
    exec("ap"+str(nn)+"_normalized_m2ew.append((p[nn-1] - p[nn2-1])**2)")
  exec("p2[nn-1] = p[nn-1] / (math.sqrt(sum(ap"+str(nn)+"_normalized_m2ew)))")
  

print(p2)

print("rede " + str(p2.index(max(p2)) + 1))
print("pontuacao da rede: " + str(max(p2)))
