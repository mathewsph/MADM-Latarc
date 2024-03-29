import ast
import sys
import math

#Bibliotecas "ast" (para leitura dos arquivos de texto) e math (para o uso de funcoes matematicas. Neste caso, sera necessaria usar raiz quadrada).

n = int(sys.argv[1])
ap_range = ast.literal_eval(sys.argv[2])

delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

l = [0] * n
score = []
#for a in range(1,(int(n)+1)):		
for a in ap_range:
 num = a
 ap = "ap" + str(a) + ".txt"
 k = "ap" + str(a)
 a = open("APs/"+ap,"r")
 a = a.read()
 a = ast.literal_eval(a)
# l.append(a)
 l[num-1]=a
 exec("%s = %s" % ("attr",[]))			
 for i in a:
  exec("%s = %s" % (i,[]))			
  exec("%s = %s" % (k,[]))
  exec("%s = %d" % (i + "_max",0))
  exec("%s = %d" % (i + "_min",0))
  exec("%s = %s" % (i + "_normalized",[]))
  exec("%s = %s" % (k + "_normalized",[]))

#for attributes in l[0]:
# attr.append(attributes)
attr=['delay','jitter','packet_loss','av_bandwidth']
attr.sort(key=len)

for z in range(1,(int(n)+1)):
 if z in ap_range:
  for xij in attr:
   exec("ap" + str(z) + ".append(float(l[z-1][xij]))")

print (l)

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

for j in attr:
 exec ('apc =' + j)
 for e in apc:
  exec(j+'_normalized.append(e**2)')

for ab in range(1,int(n)+1):
 if ab in ap_range: 
  exec('ap_list = ap'+str(ab))
  for attr_value in ap_list:
   if ap_list.index(attr_value) == 0:
     apc = (sum(delay_normalized))**0.5
     exec("ap" + str(ab) + "[(ap_list.index(attr_value))] = ((attr_value/apc)*delay_weight*(-1))")
   elif ap_list.index(attr_value) == 1:
     apc = (sum(jitter_normalized))**0.5
     exec("ap" + str(ab) + "[(ap_list.index(attr_value))] = (attr_value/apc*jitter_weight)*(-1)")
   elif ap_list.index(attr_value) == 2:
     apc = (sum(packet_loss_normalized))**0.5
     exec("ap" + str(ab) + "[(ap_list.index(attr_value))] = (attr_value/apc*packet_loss_weight*(-1))")
   elif ap_list.index(attr_value) == 3:
     apc = (sum(av_bandwidth_normalized))**0.5
     exec("ap" + str(ab) + "[(ap_list.index(attr_value))] = (attr_value/apc*av_bandwidth_weight*(1))")

for i in range(1,(int(n)+1)):   #criacao da lista com as pontuacoes de todas as redes.
 if i in ap_range:
  exec ("score.append(sum(ap"+str(i)+"))")
 else:
  score.append(-100)
print(score)
print("rede " + str(score.index(max(score)) + 1))
print("pontuacao da rede: " + str(max(score)))
