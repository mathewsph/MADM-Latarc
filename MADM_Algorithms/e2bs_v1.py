import ast
import sys
import math

#pesos
delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

def normalize_min(x,y):					#Funcao "quanto menos, melhor (Para criterios de custo)"
 if max(x) - min(x) != 0:
  m = (max(x) - y)/(max(x)- min(x))
 if max(x) - min(x) == 0:
  m = 1
 return m
	
def normalize_max(x,z):					#Funcao "quanto mais, melhor (Para criterios beneficos)"
 if max(x) - min(x) != 0:
  m = (z - min(x))/(max(x)- min(x))
 if max(x) - min(x) == 0:
  m = 1
 return m

ap_range = ast.literal_eval(sys.argv[2])
n = int(sys.argv[1])
#n = input("Quantos APs? ") #Leitura do numero de APS que serao executados.

apr = {'delay': 0.0, 'jitter': 0.0, 'packet_loss': 0.0, 'av_bandwidth': 54.00}

p = [0] * n	#Armazenara as pontuacoes de cada rede
l = [0] * n

#print (l)
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

#for attributes in l[0]:
# attr.append(attributes)
attr=['delay','jitter','packet_loss','av_bandwidth']
attr.sort(key=len)

#print (l)

for z in range(1,(int(n)+1)):
 if z in ap_range:
#  print (l[(z-1)])
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


for attribute in attr:
  exec(attribute + "_average = float(sum("+attribute+ "))/len(" + attribute + ")" )

for attribute in attr:
  exec("z = "+ attribute)
  exec("%s = %s" % (attribute+"_square",[]))
  for value in z:
    exec(attribute+"_square.append((value - "+attribute+"_average)**2)")
    exec(attribute+"_variance=sum("+attribute+"_square)")
    exec(attribute+"_dp=math.sqrt("+attribute+"_variance)")

print (delay_dp)
print (jitter_dp)
print(packet_loss_dp)
print(av_bandwidth_dp)
#Normalization No.1
for attribute in attr:
  exec("a = "+ attribute)
  exec("%s = %s" % (attribute+"_normalized",[]))
#  print (a)
  for attr_value in a:
   exec(attribute+"_normalized.append("+attribute+"_weight*((attr_value-"+attribute+"_average)/"+attribute+"_dp))")

for attribute in attr:
 c = 1
 d = 0
 for n in range(1,len(l)+1):
  if n in ap_range:
   exec("o = "+attribute+"_normalized[d]")
   d = d + 1
   exec("ap"+str(n)+"_normalized.append(o)")
   c = c + 1
  else:
   c = c + 1

for number_of_aps in ap_range:
 exec("x = ap"+str(number_of_aps)+"_normalized")
 for m in x:
  if x.index(m) == 0:
   nv = (m - apr['delay']) ** 2
   exec("ap"+str(number_of_aps)+"_normalized[0] = nv")
  elif x.index(m) == 1:
   nv = (m - apr['jitter']) ** 2
   exec("ap"+str(number_of_aps)+"_normalized[1] = nv")
  elif x.index(m) == 2:
   nv = (m - apr['packet_loss']) ** 2
   exec("ap"+str(number_of_aps)+"_normalized[2] = nv")
  elif x.index(m) == 0:
   nv = (m - apr['av_bandwidth']) ** 2
   exec("ap"+str(number_of_aps)+"_normalized[3] = nv")

for n in range(1,len(l)+1):
 if n in ap_range:
  b = str(n)
  exec("%s = %s" % ("ap"+b+"_score",[0,0,0,0]))
  exec("z = ap"+b+"_normalized")
  exec("ap"+b+"_score[0]=z[0]*delay_weight")
  exec("ap"+b+"_score[1]=z[1]*jitter_weight")
  exec("ap"+b+"_score[2]=z[2]*packet_loss_weight")
  exec("ap"+b+"_score[3]=z[3]*av_bandwidth_weight")

for ap_number in range(1,(int(n)+1)):       #sera executada a soma dos atributos normalizados e com os pesos, dando a pontuacao final da rede
 if ap_number in ap_range:
  index = str(ap_number-1)
  ap_number = str(ap_number)
  exec("l["+ index + "]=(sum(ap" + ap_number + "_score))")

#print(l) #Pontuacao de todas as redes avaliadas (na ordem numerica de 1 ate n).

print("ap" + str(l.index(max(l)) + 1))   #Melhor rede entre as candidatas
#print("pontuacao da rede: " + str(max(l)))  #Pontuacao dessa rede
