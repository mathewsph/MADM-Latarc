import ast
import sys

#pesos
delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

delay_threshold = 150
jitter_threshold = 100
packet_loss_threshold = 10
av_bandwidth_threshold = 0.2
min_delay = 0
min_jitter = 50
min_packet_loss = 0
max_av_bandwidth = 54

def normalize_min(y,min_attr,threshold):					#Funcao "quanto menos, melhor (Para criterios de custo)"
  m = (y - threshold) / (min_attr - threshold)
  return m
	
def normalize_max(z,max_attr,threshold):					#Funcao "quanto mais, melhor (Para criterios de beneficio)"
  m = (z - threshold) / (max_attr - threshold)
  return m

ap_range = ast.literal_eval(sys.argv[2])
n = int(sys.argv[1])
#n = input("Quantos APs? ") #Leitura do numero de APS que serao executados.

p = [0] * n	#Armazenara as pontuacoes de cada rede
l = [0] * n

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

for i in range(1,len(l)+1):			#Normalizacao e multiplicacao pelos pesos
 if i in ap_range:
  g = str(i)
  exec("z = ap" + g)
  print (z)
  for k in z:
   if z.index(k) == 0:
    m = (normalize_min(k,min_delay,delay_threshold))*delay_weight
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 1:
    m = (normalize_min(k,min_jitter,jitter_threshold))*jitter_weight
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 2:
    m = (normalize_min(k, min_packet_loss,packet_loss_threshold))*packet_loss_weight
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 3:
    m = (normalize_max(k,max_av_bandwidth,av_bandwidth_threshold))*av_bandwidth_weight
    exec("ap" + g + "_normalized.append(m)")


for ap_number in range(1,(int(n)+1)):		#Soma das pontuacoes individuais de cada atributo, para dar a pontuacao final de cada rede.
 if ap_number in ap_range:
  str_index = str(ap_number-1)
  ap_number = str(ap_number)
#  exec("p.append(sum(ap" + ap_number + "_normalized))")
  exec("p["+ str_index +"]=sum(ap" + ap_number + "_normalized)")
for i in range(1,n+1):
  if i in ap_range:
    print (i)
  else:
    p[i-1] = 0
    print (p[i-1])

print(p)

print("rede " + str(p.index(max(p)) + 1))
print("pontuacao da rede: " + str(max(p)))