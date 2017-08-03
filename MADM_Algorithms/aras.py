import ast
import sys
import math

#Bibliotecas "ast" (para leitura dos arquivos de texto) e math (para o uso de funcoes matematicas. Neste caso, sera necessaria usar raiz quadrada).

def normalize_min(xij,soma):
 z = (1/xij)/soma
 return z

def normalize_max(xij,soma):
 z = xij/soma
 return z

n = int(sys.argv[1])
ap_range = ast.literal_eval(sys.argv[2])

delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

l = [0] * n
score = [0]*n
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
  exec("%s = %s" % ('s0',[]))
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
    delay.append(1.0/x[b])
   if b == 'jitter':
    jitter.append(1.0/x[b])
   if b == 'packet_loss':
    packet_loss.append(1./x[b])
   if b == 'av_bandwidth':
    av_bandwidth.append(x[b])

for j in attr:
 exec("%s = %s" % (j+"_normalized",[]))			
 exec('apc = ' + j)
 exec('wa = ' + j + '_weight')
 for u in apc:
  x = (u)/sum(apc)
  exec(j+"_normalized.append(x*wa)")

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

#definir s0
for attribute in attr:
 exec('sv=' + attribute+'_normalized')
 s0.append(max(sv))

for z in range(1,(int(n)+1)):
 if z in ap_range:
  exec("k = sum(ap"+str(z)+"_normalized)/(sum(s0))")
  score[z-1] = k
print("ap" + str(score.index(max(score)) + 1))
print (score)