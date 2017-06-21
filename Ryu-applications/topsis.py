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

#for a in range(1,(int(n)+1)):		
for a in ap_range:
 num = a
 ap = "ap" + str(a) + ".txt"
 k = "ap" + str(a)
 a = open("../"+ap,"r")
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

#print (l)

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

for i in range(1,len(l)+1):
 if i in ap_range:
  g = str(i)
  exec("w = ap" + g)
  for k in w:
   if w.index(k) == 0:
    m  = k ** 2
    exec("ap" + g + "_normalized.append(m)")
   if w.index(k) == 1:
    m  = k ** 2
    exec("ap" + g + "_normalized.append(m)")
   if w.index(k) == 2:
    m = k ** 2
    exec("ap" + g + "_normalized.append(m)")
   if w.index(k) == 3:
    m = k ** 2
    exec("ap" + g + "_normalized.append(m)")

for ab in range(1,(int(n)+1)):		#Normalizacao com a equacao "rij" Multiplicacao dos pesos pelo resultado da equacao anterior
 if ab in ap_range:
  g = str(ab)
  exec("ap_list = ap"+g)
  exec("apc = math.sqrt(sum(ap" + g + "_normalized))")
  for attr_value in ap_list:
#    print (attr_value/apc)
     exec("ap" + g + "[(ap_list.index(attr_value))] = attr_value/apc")
  for attr_valuen2 in ap_list:
     if ap_list.index(attr_valuen2) == 0:
       exec("ap" + g + "[(ap_list.index(attr_valuen2))] = (attr_valuen2*delay_weight)")
       delay_normalized.append(attr_valuen2*delay_weight)
     elif ap_list.index(attr_valuen2) == 1:
       exec("ap" + g + "[(ap_list.index(attr_valuen2))] = (attr_valuen2*jitter_weight)")
       jitter_normalized.append(attr_valuen2*jitter_weight)
     elif ap_list.index(attr_valuen2) == 2:
       exec("ap" + g + "[(ap_list.index(attr_valuen2))] = (attr_valuen2*packet_loss_weight)")
       packet_loss_normalized.append(attr_valuen2*packet_loss_weight)
     elif ap_list.index(attr_valuen2) == 3:
       exec("ap" + g + "[(ap_list.index(attr_valuen2))] = (attr_valuen2*av_bandwidth_weight)")
       av_bandwidth_normalized.append(attr_valuen2*av_bandwidth_weight)


for apt in l:			#Laco que fara a funcao das formulas de normalizacao A+ e A- (definicao das redes ideais positivas e negativas)
 if apt != 0:
  for attr in apt:
   if attr == "delay" or attr == "jitter" or attr == "packet_loss":
    exec(attr+"_max = min(" + attr + "_normalized)")
    exec(attr+"_min = max(" + attr + "_normalized)")
   elif attr == "throughput" or attr == "av_bandwidth":
    exec(attr+"_max = max(" + attr + "_normalized)")
    exec(attr+"_min = min(" + attr + "_normalized)")

for ab in range(1,(int(n)+1)):
 if ab in ap_range:
  g = str(ab)
  exec ("z = ap" + g)
  exec("%s = %s" % ("ap"+g+"_dist_pos",[]))
  exec("%s = %s" % ("ap"+g+"_dist_neg",[]))
  for q in z:
   if z.index(q) == 0:
    w = ((z[0] - delay_max) ** 2)
    exec("ap"+g+"_dist_pos"+".append(w)")
   elif z.index(q) == 3:
    exec("ap"+g+"_dist_pos"+".append((z[3] - av_bandwidth_max) ** 2)")
   elif z.index(q) == 1:
    exec("ap"+g+"_dist_pos"+".append((z[1] - jitter_max) ** 2)")
   elif z.index(q) == 2:
    exec("ap"+g+"_dist_pos"+".append((z[2] - packet_loss_max) ** 2)")
  for q in z:
   if z.index(q) == 0:
    exec("ap"+g+"_dist_neg"+".append((z[0] - delay_min) ** 2)")
   elif z.index(q) == 3:
    exec("ap"+g+"_dist_neg"+".append((z[3] - av_bandwidth_min) ** 2)")
   elif z.index(q) == 1:
    exec("ap"+g+"_dist_neg"+".append((z[1] - jitter_min) ** 2)")
   elif z.index(q) == 2:
    exec("ap"+g+"_dist_neg"+".append((z[2] - packet_loss_min) ** 2)")

score = []


#for i in range(1,(int(n)+1)):
# if i in ap_range:
#  exec ("print (math.sqrt(sum(ap" + str(i) + "_dist_pos)))")
#  exec ("print (math.sqrt(sum(ap" + str(i) + "_dist_neg)))")

for i in range(1,(int(n)+1)):	#criacao da lista com as pontuacoes de todas as redes.
 if i in ap_range:
  exec ("score.append(math.sqrt(sum(ap" + str(i) + "_dist_neg))/(math.sqrt(sum(ap" + str(i)+"_dist_pos)) + math.sqrt(sum(ap" + str(i) + "_dist_neg))))")
 else:
  score.append(0)
#print(score)
print("ap" + str(score.index(max(score)) + 1))
#print("pontuacao da rede: " + str(max(score)))
