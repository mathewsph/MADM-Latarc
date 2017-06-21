import ast
import math

#Bibliotecas "ast" (para leitura dos arquivos de texto) e math (para o uso de funcoes matematicas. Neste caso, sera necessaria usar raiz quadrada).

n = input("Quantos APs? ")

delay_weight = 0.36	#em milisegundos(ms)
jitter_weight = 0.32	#em milisegundos(ms)
packet_loss_weight = 0.18	#em porcentagem de perda de pacotes
av_bandwidth_weight =0.14	#Em Mb/s (Megabit por segundo)

l = []

for a in range(1,(int(n)+1)):		
 ap = "ap" + str(a) + ".txt"
 k = "ap" + str(a)
 a = open("APs/"+ap,"r")
 a = a.read()
 a = ast.literal_eval(a)
 l.append(a)
 exec("%s = %s" % ("attr",[]))			
 for i in a:
  exec("%s = %s" % (i,[]))			
  exec("%s = %s" % (k,[]))
  exec("%s = %d" % (i + "_max",0))
  exec("%s = %d" % (i + "_min",0))
  exec("%s = %s" % (k + "_normalized",[]))

for attributes in l[0]:
 attr.append(attributes)
attr.sort(key=len)

for z in range(0,(int(n))):
 for xij in attr:
  exec("ap" + str(z+1) + ".append(float(l[z][xij]))")

for x in l:					
#	print x						
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
 g = str(ab)
 exec("x = math.sqrt(sum(ap" + g + "_normalized))")
#	print x
 for i in delay:
  if delay.index(i) == ab - 1:
   delay[ab-1] = (i/x)*delay_weight
   exec("ap" + g + "[0]"+"= (i/x)*delay_weight")
 for i in jitter:
  if jitter.index(i) == ab - 1:
   jitter[ab-1] = (i/x)*jitter_weight
   exec("ap" + g + "[1]"+"= (i/x)*jitter_weight")
 for i in packet_loss:
  if packet_loss.index(i) == ab - 1:
   packet_loss[ab-1] = (i/x)*packet_loss_weight
   exec("ap" + g + "[2]"+"= (i/x)*packet_loss_weight")
 for i in av_bandwidth:
  if av_bandwidth.index(i) == ab - 1:
   av_bandwidth[ab-1] = (i/x)*av_bandwidth_weight
   exec("ap" + g + "[3]"+"= (i/x)*av_bandwidth_weight")


for apt in l:			#Laco que fara a funcao das formulas de normalizacao A+ e A- (definicao das redes ideais positivas e negativas)
 for attr in apt:
  if attr == "delay" or attr == "jitter" or attr == "packet_loss":
   exec(attr+"_max = min(" + attr + ")")
   exec(attr+"_min = max(" + attr + ")")
  elif attr == "throughput" or attr == "av_bandwidth":
   exec(attr+"_max = max(" + attr + ")")
   exec(attr+"_min = min(" + attr + ")")

#for v in range(1,(len(l)+1)):
#	exec("print ap" + str(v))

#for attr in l[0]:
#	exec ("print " +attr+"_max")
#	exec ("print " +attr+"_min")

for ab in range(1,(int(n)+1)):
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
#	exec ("print math.sqrt(sum(ap" + str(i) + "_dist_pos))")
#	exec ("print math.sqrt(sum(ap" + str(i) + "_dist_neg))")

for i in range(1,(int(n)+1)):	#criacao da lista com as pontuacoes de todas as redes.
 exec ("score.append(math.sqrt(sum(ap" + str(i) + "_dist_neg))/(math.sqrt(sum(ap" + str(i)+"_dist_pos)) + math.sqrt(sum(ap" + str(i) + "_dist_neg))))")

print(score)
print("rede " + str(score.index(max(score)) + 1))
print("pontuacao da rede: " + str(max(score)))
