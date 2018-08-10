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
  exec("%s = %s" % (k + "_dist_pos",[]))
  exec("%s = %s" % (k + "_dist_neg",[]))
  exec("%s = %s" % (i + "_x",[]))

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

I_pos = [min(delay), min(jitter), min(packet_loss), max(av_bandwidth)]
I_neg = [max(delay), max(jitter), max(packet_loss), min(av_bandwidth)]

for i in range(1,len(l)+1):
 if i in ap_range:
  g = str(i)
  exec("w = ap" + g)
  for k in w:
   if w.index(k) == 0:
    m = (k - min(delay)) ** 2
    nn = (k - max(delay)) ** 2
    exec("ap" + g + "_dist_pos.append(m)")
    exec("ap" + g + "_dist_neg.append(nn)")
   if w.index(k) == 1:
    m = (k - min(jitter)) ** 2
    nn = (k - max(jitter)) ** 2
    exec("ap" + g + "_dist_pos.append(m)")
    exec("ap" + g + "_dist_neg.append(nn)")
   if w.index(k) == 2:
    m = (k - min(packet_loss)) ** 2
    nn = (k - max(packet_loss)) ** 2
    exec("ap" + g + "_dist_pos.append(m)")
    exec("ap" + g + "_dist_neg.append(nn)")
   if w.index(k) == 3:
    m = (k - max(av_bandwidth)) ** 2
    nn = (k - min(av_bandwidth)) ** 2
    exec("ap" + g + "_dist_pos.append(m)")
    exec("ap" + g + "_dist_neg.append(nn)")
  exec("ap"+g+"_dist_pos = math.sqrt(sum(ap" + g + "_dist_pos))")
  exec("ap"+g+"_dist_neg = math.sqrt(sum(ap" + g + "_dist_neg))")

all_pos = []
all_neg = []
score = []

for j in range(1,len(l)+1):
 if j in ap_range:
  exec ('j1 = ap'+str(j)+'_dist_pos')
  exec ('j2 = ap'+str(j)+'_dist_neg')
  all_pos.append(j1**2)
  all_neg.append(j2**2)

for ks in range(1,len(l)+1):
 if ks in ap_range:
  exec ("ap" + str(ks) + "_cp = ap"+str(ks)+"_dist_pos / math.sqrt(sum(all_pos))")
  exec ("ap" + str(ks) + "_cn = ap"+str(ks)+"_dist_neg / math.sqrt(sum(all_neg))")


for i2 in range(1,(int(n)+1)):	#criacao da lista com as pontuacoes de todas as redes.
 if i2 in ap_range:
  exec ('num = ap' + str(i2) + '_cn + ap' + str(i2) + '_cp')
  exec ('ng = ap' + str(i2) + '_cn')
  pts = ng/num
  score.append(pts)
 else:
  score.append(0)
print(score)
print("rede " + str(score.index(max(score)) + 1))
#print("pontuacao da rede: " + str(max(score)))
