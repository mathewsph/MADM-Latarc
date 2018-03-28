import ast
import sys
import math

#Bibliotecas "ast" (para leitura dos arquivos de texto) e math (para o uso de funcoes matematicas. Neste caso, sera necessaria usar raiz quadrada).

def dj(attr,avl):
 a = avl - attr
 if a >= 0:
  return a
 else:
  a = a * (-1)
  return a

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

#for attributes in l[0]:
# attr.append(attributes)
attr=['delay','jitter','packet_loss','av_bandwidth']
attr.sort(key=len)

for z in range(1,(int(n)+1)):
 if z in ap_range:
  for xij in attr:
   exec("ap" + str(z) + ".append(float(l[z-1][xij]))")

#for u in l:
# print (u)

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

for apt in l:			#Laco que fara a funcao das formulas de normalizacao A+ e A- (definicao das redes ideais positivas e negativas)
 if apt != 0:
  for attr in apt:
   if attr == "delay" or attr == "jitter" or attr == "packet_loss":
    exec(attr+"_max = min(" + attr+")")
    exec(attr+"_min = max(" + attr+")")
   elif attr == "throughput" or attr == "av_bandwidth":
    exec(attr+"_max = max(" + attr+")")
    exec(attr+"_min = min(" + attr+")")

all_djpos = []
all_djneg = []

for num in range(1,len(l)+1):
 if num in ap_range:
  djpos = []
  djneg = []
  exec("v = ap"+str(num))
  for avl in v:
   if v.index(avl) == 0:
    vlx = dj(delay_max,avl)
    vly = dj(delay_min,avl)
    djpos.append(vlx)
    djneg.append(vly)
   if v.index(avl) == 1:
    vlx = dj(jitter_max,avl)
    vly = dj(jitter_min,avl)
    djpos.append(vlx)
    djneg.append(vly)
   if v.index(avl) == 2:
    vlx = dj(packet_loss_max,avl)
    vly = dj(packet_loss_min,avl)
    djpos.append(vlx)
    djneg.append(vly)
   if v.index(avl) == 3:
    vlx = dj(av_bandwidth_max,avl)
    vly = dj(av_bandwidth_min,avl)
    djpos.append(vlx)
    djneg.append(vly)
   exec("%s = %s" % ("ap"+str(num)+"_djpos",sum(djpos)))
   exec("%s = %s" % ("ap"+str(num)+"_djneg",sum(djneg)))
for nn in range(1,len(l)+1):
 if nn in ap_range:
   exec("all_djpos.append(ap" + str(nn) +"_djpos)")
   exec("all_djneg.append(ap" + str(nn) +"_djneg)")

def result(p,ng,all_djpos,all_djneg):
 x = math.sqrt(((p - min(all_djpos))**2)+ ((ng - max(all_djneg))**2))
 return x
for num2 in range(1,len(l)+1):
 if num2 in ap_range:
  exec("p = ap"+str(num2)+"_djpos")
  exec("ng = ap"+str(num2)+"_djneg")
  rt = result(p,ng,all_djpos,all_djneg)
  score.append(rt)
 else:
  score.append(1000000)
#print(score)
print("ap" + str(score.index(min(score)) + 1))
