import ast
import sys
import math

#Bibliotecas "ast" (para leitura dos arquivos de texto) e math (para o uso de funcoes matematicas. Neste caso, sera necessaria usar raiz quadrada).

def normalize_min(x,y):					#Funcao "quanto menos, melhor (Para criterios de custo)"
 if max(x) - min(x) != 0:
  m = (min(x))/(y)
 if max(x) - min(x) == 0:
  m = 1
 return m
	
def normalize_max(x,z):					#Funcao "quanto mais, melhor (Para criterios beneficos)"
 if max(x) - min(x) != 0:
  m = (z)/(max(x))
 if max(x) - min(x) == 0:
  m = 1
 return m

n = int(sys.argv[1])
ap_range = ast.literal_eval(sys.argv[2])

delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

l = [0] * n
score = [0] * n

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

for u in l:
 print (u)

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
  exec("w = ap" + g)
  print (z)
  for k in w:
   if w.index(k) == 0:
    m = (normalize_min(delay,k))
    exec("ap" + g + "_normalized.append(m)")
   if w.index(k) == 1:
    m = (normalize_min(jitter,k))
    exec("ap" + g + "_normalized.append(m)")
   if w.index(k) == 2:
    m = (normalize_min(packet_loss,k))
    exec("ap" + g + "_normalized.append(m)")
   if w.index(k) == 3:
    m = (normalize_max(av_bandwidth,k))
    exec("ap" + g + "_normalized.append(m)")

for ab in range(1,(int(n)+1)):		#Normalizacao com a equacao "rij" Multiplicacao dos pesos pelo resultado da equacao anterior
 if ab in ap_range:
  g = str(ab)
  exec("ap_list = ap"+g)
  exec("apc = math.sqrt(sum(ap" + g + "_normalized))")
  for attr_value in ap_list:
     exec("ap" + g + "[(ap_list.index(attr_value))] = attr_value/apc")
  for attr_valuen2 in ap_list:
     if ap_list.index(attr_valuen2) == 0:
       delay_normalized.append(attr_valuen2)
     elif ap_list.index(attr_valuen2) == 1:
       jitter_normalized.append(attr_valuen2)
     elif ap_list.index(attr_valuen2) == 2:
       packet_loss_normalized.append(attr_valuen2)
     elif ap_list.index(attr_valuen2) == 3:
       av_bandwidth_normalized.append(attr_valuen2)

for apt in l:			#Laco que fara a funcao das formulas de normalizacao A+ e A- (definicao das redes ideais positivas e negativas)
 if apt != 0:
  for attr in apt:
   if attr == "delay" or attr == "jitter" or attr == "packet_loss":
    exec(attr+"_max = min(" + attr + "_normalized)")
    exec(attr+"_min = max(" + attr + "_normalized)")
   elif attr == "throughput" or attr == "av_bandwidth":
    exec(attr+"_max = max(" + attr + "_normalized)")
    exec(attr+"_min = min(" + attr + "_normalized)")

def s_i (attribute,value,weight,max_attribute,min_attribute):
  i = weight*((max_attribute - value)/(max_attribute - min_attribute))  
  return i 
def r_i (attribute,value,weight,max_attribute,min_attribute):  
  i = max_attribute*(weight*((max_attribute - value)/(max_attribute - min_attribute)))
  return i

for ab in range(1,(int(n)+1)):
 if ab in ap_range:
  g = str(ab)
  exec ("z = ap" + g)
  exec("%s = %s" % ("ap"+g+"_dist_pos",[]))
  exec("%s = %s" % ("ap"+g+"_dist_neg",[]))
  for q in z:
   if z.index(q) == 0:
    w = s_i(delay, q, delay_weight, delay_max, delay_min)
    exec("ap"+g+"_dist_pos.append(w)")
    y = r_i(delay, q, delay_weight, delay_max, delay_min)
    exec("ap"+g+"_dist_neg.append(y)")
   elif z.index(q) == 1:
    w = s_i(jitter, q, jitter_weight, jitter_max, jitter_min)
    y = r_i(jitter, q, jitter_weight, jitter_max, jitter_min)
    exec("ap"+g+"_dist_neg.append(y)")
    exec("ap"+g+"_dist_pos.append(w)")
   elif z.index(q) == 2:
    w = s_i(packet_loss, q, packet_loss_weight, packet_loss_max, packet_loss_min)
    exec("ap"+g+"_dist_pos.append(w)")
    y = r_i(packet_loss, q, packet_loss_weight, packet_loss_max, packet_loss_min)
    exec("ap"+g+"_dist_neg.append(y)")
   elif z.index(q) == 3:
    w = s_i(av_bandwidth, q, av_bandwidth_weight, av_bandwidth_max, av_bandwidth_min)
    exec("ap"+g+"_dist_pos.append(w)")
    y = r_i(av_bandwidth, q, av_bandwidth_weight, av_bandwidth_max, av_bandwidth_min)
    exec("ap"+g+"_dist_neg.append(y)")

all_s = []
all_r = []

for ab in range(1,(int(n)+1)):
 if ab in ap_range:
  g = str(ab)
  exec ("z = ap" + g)
  exec("ap"+g+"_dist_pos = sum(ap" + g + "_dist_pos)")
  exec("ap"+g+"_dist_neg = sum(ap" + g + "_dist_neg)")
  exec("all_s.append(ap"+g+"_dist_pos)")
  exec("all_r.append(ap"+g+"_dist_neg)")

def q_i(si, ri):
  max_s = min(all_s)
  max_r = min(all_r)
  min_s = max(all_s)
  min_r = max(all_r)
  qi = ((0.5*((si - max_s)/(min_s - max_s))) + ((1-0.5)*((ri - max_r)/(min_r - max_r))))
  return qi

for zv in range(1,(int(n)+1)):
 if zv in ap_range:
  bt = str(zv)
  exec("si = ap"+bt+"_dist_pos")
  exec("ri = ap"+bt+"_dist_neg") 
  fc = q_i(si, ri)
  score[int(bt)-1] = fc
 else: 
  score[zv-1] = 1000000
print (all_s)
print (score) 
print("rede " + str(score.index(min(score)) + 1))

