import ast
import sys
import math
import operator
import functools
import itertools
import operator

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

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
  exec("%s = %s" % (k + "_st1",[0]*4))
  exec("%s = %s" % (k + "_st2",[]))
  exec("%s = %s" % (k + "_st3",[]))


#for attributes in l[0]:
# attr.append(attributes)
attr=['delay','jitter','packet_loss','av_bandwidth']
attr.sort(key=len)

for z in range(1,(int(n)+1)):
 if z in ap_range:
  for xij in attr:
   exec("ap" + str(z) + ".append(float(l[z-1][xij]))")



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
     exec("ap" + str(ab) + "_st1[(ap_list.index(attr_value))] = ((attr_value/apc)*delay_weight*(-1))")
   elif ap_list.index(attr_value) == 1:
     apc = (sum(jitter_normalized))**0.5
     exec("ap" + str(ab) + "_st1[(ap_list.index(attr_value))] = (attr_value/apc*jitter_weight)*(-1)")
   elif ap_list.index(attr_value) == 2:
     apc = (sum(packet_loss_normalized))**0.5
     exec("ap" + str(ab) + "_st1[(ap_list.index(attr_value))] = (attr_value/apc*packet_loss_weight*(-1))")
   elif ap_list.index(attr_value) == 3:
     apc = (sum(av_bandwidth_normalized))**0.5
     exec("ap" + str(ab) + "_st1[(ap_list.index(attr_value))] = (attr_value/apc*av_bandwidth_weight*(1))")

rj_delay = (min(delay_normalized)**0.5)*delay_weight/((sum(delay_normalized))**0.5)
rj_jitter = (min(jitter_normalized)**0.5)*jitter_weight/((sum(jitter_normalized))**0.5)
rj_packet_loss = (min(packet_loss_normalized)**0.5)*packet_loss_weight/((sum(packet_loss_normalized))**0.5)
rj_av_bandwidth = (max(av_bandwidth_normalized)**0.5)*av_bandwidth_weight/((sum(av_bandwidth_normalized))**0.5)

for ab1 in range(1,int(n)+1):
 if ab1 in ap_range: 
  exec('ap_list = ap'+str(ab1)+"_st1")
  for attr_v in ap_list:
   if ap_list.index(attr_v) == 0:
    attr_v = attr_v*(-1)
    xf = rj_delay - attr_v
    xf = float("%.4f" % xf)
    if xf < 0:
     xf = (-1)*xf
    exec("ap"+str(ab1)+"_st2.append(xf)")
   elif ap_list.index(attr_v) == 1:
    attr_v = attr_v*-1 
    xf = rj_jitter - attr_v
    xf = float("%.4f" % xf)
    if xf < 0:
     xf = xf*(-1)
    exec("ap"+str(ab1)+"_st2.append(xf)")
   elif ap_list.index(attr_v) == 2:
    attr_v = attr_v*(-1)
    xf = rj_packet_loss - attr_v
    xf = float("%.4f" % xf)
    if xf < 0:
     xf = (-1)*xf
    exec("ap"+str(ab1)+"_st2.append(xf)")
   elif ap_list.index(attr_v) == 3:
    xf = rj_av_bandwidth - attr_v
    xf = float("%.4f" % xf)
    if xf < 0:
     xf = -1*xf
    exec("ap"+str(ab1)+"_st2.append(xf)")

score_st2 = [0]*n

for ab2 in range(1,int(n)+1):
 if ab2 in ap_range: 
  exec("ex = max(ap"+str(ab2)+"_st2)")
  score_st2[ab2-1] = ex
 else:
  score_st2[ab2-1] = -100

#---------st3
for ab3 in range(1,int(n)+1):
 if ab3 in ap_range:
  exec("arr = ap"+str(ab3))
  for attr_v3 in arr:
   if arr.index(attr_v3) == 0:
    exec("ap"+str(ab3)+"_st3.append(attr_v3**delay_weight)")
   if arr.index(attr_v3) == 1:
    exec("ap"+str(ab3)+"_st3.append(attr_v3**jitter_weight)")
   if arr.index(attr_v3) == 2:
    exec("ap"+str(ab3)+"_st3.append(attr_v3**packet_loss_weight)")
   if arr.index(attr_v3) == 3:
    exec("ap"+str(ab3)+"_st3_a = attr_v3**av_bandwidth_weight")

score_st3 = [0] * n  
 
for ab3v in range(1,int(n)+1):
 if ab3v in ap_range:
  exec("score_st3[ab3v-1]=(ap"+str(ab3v)+"_st3_a)/(functools.reduce(operator.mul, ap" + str(ab3v) + "_st3))")

for i in range(1,(int(n)+1)):   #criacao da lista com as pontuacoes de todas as redes.
 if i in ap_range:
  exec ("score.append(sum(ap"+str(i)+"_st1))")
 else:
  score.append(-100)

final_score = []

final_score.append(score.index(max(score)) + 1)
final_score.append(score_st2.index(max(score_st2)) + 1)
final_score.append(score_st3.index(max(score_st3)) + 1)

m = most_common(final_score)
print ("ap"+str(m))
#print("pontuacao da rede: " + str(max(score)))


