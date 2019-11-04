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

ap_range = ast.literal_eval(sys.argv[2])
n = int(sys.argv[1])
#n = input("Quantos APs? ") #Leitura do numero de APS que serao executados.

p = [0] * n	#Armazenara as pontuacoes de cada rede
l = [0] * n
all_cset = []
all_dset = []

ap_reference = {'delay': 0, 'jitter': 0, 'packet_loss': 0, 'av_bandwidth': 54}

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
  exec("%s = %s" % (k+"_pos",[]))
  exec("%s = %s" % (k+"_neg",[]))
  exec("%s = %s" % (k + "_normalized",[]))

for value_ap in ap_range:
 for value_apn in ap_range:
  if value_ap > value_apn:
   exec("%s = %s" % ("cset"+str(value_ap)+'_'+str(value_apn),[]))
   exec("%s = %s" % ("dset"+str(value_ap)+'_'+str(value_apn),[]))
  if value_ap < value_apn:
   exec("%s = %s" % ("cset"+str(value_ap)+'_'+str(value_apn),[]))
   exec("%s = %s" % ("dset"+str(value_ap)+'_'+str(value_apn),[]))

nnu = 0

for u in l:
 if u != 0:
  nnu = nnu +1

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

for i in range(1,len(l)+1):			#Normalizacao e multiplicacao pelos pesos
 if i in ap_range:
  g = str(i)
  exec("z = ap" + g)
#  print (z)
  for k in z:
   if z.index(k) == 0:
    m = (normalize_min(delay,(k)))
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 1:
    m = (normalize_min(jitter,k))
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 2:
    m = (normalize_min(packet_loss,(k)))
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 3:
#    gv = k - ap_reference['av_bandwidth']
#    if gv < 0:
#     gv = -(gv)
    m = (normalize_max(av_bandwidth,k))
    exec("ap" + g + "_normalized.append(m)")

for ap_number in ap_range:
  for apn_number in ap_range:
   if ap_number > apn_number:
    exec("ap_a = ap"+str(ap_number)+"_normalized")
    exec("ap_b = ap"+str(apn_number)+"_normalized")
    if ap_a[0] > ap_b[0]:
      xs = ap_a[0] - ap_b[0]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*delay_weight)")
    if ap_a[1] > ap_b[1]:
      xs = ap_a[1] - ap_b[1]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*jitter_weight)")
    if ap_a[2] > ap_b[2]:
      xs = ap_a[2] - ap_b[2]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*packet_loss_weight)")
    if ap_a[3] > ap_b[3]:
      xs = ap_a[3] - ap_b[3]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*av_bandwidth_weight)")
   if ap_number < apn_number:
    exec("ap_a = ap"+str(ap_number)+"_normalized")
    exec("ap_b = ap"+str(apn_number)+"_normalized")
    if ap_a[0] > ap_b[0]:
      xs = ap_a[0] - ap_b[0]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*delay_weight)")
    if ap_a[1] > ap_b[1]:
      xs = ap_a[1] - ap_b[1]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*jitter_weight)")
    if ap_a[2] > ap_b[2]:
      xs = ap_a[2] - ap_b[2]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*packet_loss_weight)")
    if ap_a[3] > ap_b[3]:
      xs = ap_a[3] - ap_b[3]
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(xs*av_bandwidth_weight)")

all_pos = []

for apl_number in ap_range:
 vn = len(ap_range)
 for apln_number in ap_range:
   if apl_number != apln_number:
    exec("posm=sum(cset"+str(apl_number)+"_"+str(apln_number)+")")
    all_pos.append(posm)

cset_max = max(all_pos)
cset_min = min(all_pos)

for apz_number in ap_range:
 for apzn_number in ap_range:
   if apz_number > apzn_number:
    exec("pm=sum(cset"+str(apz_number)+"_"+str(apzn_number)+")")
    exec("dm=sum(cset"+str(apzn_number)+"_"+str(apz_number)+")")
    exec("ap"+str(apz_number)+"_pos.append((pm - cset_max) ** 2)")
    exec("ap"+str(apz_number)+"_neg.append((pm - cset_min) ** 2)")    
   if apz_number < apzn_number:
    exec("pm=sum(cset"+str(apz_number)+"_"+str(apzn_number)+")")
    exec("dm=sum(cset"+str(apzn_number)+"_"+str(apz_number)+")")
    exec("ap"+str(apz_number)+"_pos.append((pm - cset_max) ** 2)")
    exec("ap"+str(apz_number)+"_neg.append((pm - cset_min) ** 2)")  

for pon in ap_range:
 exec("xyz = math.sqrt(sum(ap"+str(pon)+"_neg)) / (math.sqrt(sum(ap"+str(pon)+"_pos)) + math.sqrt(sum(ap"+str(pon)+"_neg)))")
 p[pon-1]=(xyz)

for xc in range(1,n+1):
 if xc not in ap_range:
  p[xc-1] = -15000

print("rede " + str(p.index(max(p)) + 1))
print (p)