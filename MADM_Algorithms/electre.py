import ast
import sys

#pesos
delay_weight = 0.118	#atraso/delay
jitter_weight = 0.422	#jitter (variacao de atraso)
packet_loss_weight = 0.038	#perda de pacotes
av_bandwidth_weight = 0.422	#Largura de banda(em Mb - Megabits)

def normalize_min(x,y):					#Funcao "quanto menos, melhor (Para criterios de custo)"
 if max(x) - min(x) != 0:
  m = (max(x) - y)/(max(x)- min(x))
 if max(x) - min(x) == 0:
  m = 1
 return m
	
def normalize_max(x,z):					#Funcao "quanto mais, melhor (Para criterios beneficos)"
 if max(x) - min(x) != 0:
  m = (z - min(x))/(max(x)- min(x))
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
 with open("../"+ap,"r") as a:
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
    delay.append(x[b] - ap_reference['delay'])
   if b == 'jitter':
    jitter.append(x[b] - ap_reference['jitter'])
   if b == 'packet_loss':
    packet_loss.append(x[b] - ap_reference['packet_loss'])
   if b == 'av_bandwidth':
    avb = x[b] - ap_reference['av_bandwidth']
    if avb >= 0:
       av_bandwidth.append(avb)
    elif avb < 0:
       av_bandwidth.append(avb*(-1))

for i in range(1,len(l)+1):			#Normalizacao e multiplicacao pelos pesos
 if i in ap_range:
  g = str(i)
  exec("z = ap" + g)
#  print (z)
  for k in z:
   if z.index(k) == 0:
    m = (normalize_min(delay,(k - ap_reference['delay'])))*delay_weight
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 1:
    m = (normalize_min(jitter,k - ap_reference['jitter']))*jitter_weight
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 2:
    m = (normalize_min(packet_loss,(k - ap_reference['packet_loss'])))*packet_loss_weight
    exec("ap" + g + "_normalized.append(m)")
   if z.index(k) == 3:
    gv = k - ap_reference['av_bandwidth']
    if gv < 0:
     gv = -(gv)
    m = (normalize_min(av_bandwidth,gv))*av_bandwidth_weight
    exec("ap" + g + "_normalized.append(m)")


for ap_number in ap_range:
  for apn_number in ap_range:
   if ap_number > apn_number:
    exec("ap_a = ap"+str(ap_number)+"_normalized")
    exec("ap_b = ap"+str(apn_number)+"_normalized")
    if ap_a[0] > ap_b[0]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(delay_weight)")
    if ap_a[1] > ap_b[1]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(jitter_weight)")
    if ap_a[2] > ap_b[2]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(packet_loss_weight)")
    if ap_a[3] > ap_b[3]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(av_bandwidth_weight)")
   if ap_number < apn_number:
    exec("ap_a = ap"+str(ap_number)+"_normalized")
    exec("ap_b = ap"+str(apn_number)+"_normalized")
    if ap_a[0] > ap_b[0]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(delay_weight)")
    if ap_a[1] > ap_b[1]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(jitter_weight)")
    if ap_a[2] > ap_b[2]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(packet_loss_weight)")
    if ap_a[3] > ap_b[3]:
      exec("cset"+str(ap_number)+"_"+str(apn_number)+".append(av_bandwidth_weight)")

for ap_numberx in ap_range:
  for apn_numberx in ap_range:
   if ap_numberx > apn_numberx:
       exec("all_cset.append(sum(cset"+str(ap_numberx)+"_"+str(apn_numberx)+"))")
   if ap_numberx < apn_numberx:
       exec("all_cset.append(sum(cset"+str(ap_numberx)+"_"+str(apn_numberx)+"))")

#dset
for ap_number2 in ap_range:
  for apn_number2 in ap_range:
   if ap_number2 > apn_number2:
    exec("ap_a = ap"+str(ap_number2)+"_normalized")
    exec("ap_b = ap"+str(apn_number2)+"_normalized")
    if ap_a[0] < ap_b[0]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('delay')")
    if ap_a[1] < ap_b[1]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('jitter')")
    if ap_a[2] < ap_b[2]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('packet_loss')")
    if ap_a[3] < ap_b[3]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('av_bandwidth')")
   if ap_number2 < apn_number2:
    exec("ap_a = ap"+str(ap_number2)+"_normalized")
    exec("ap_b = ap"+str(apn_number2)+"_normalized")
    if ap_a[0] < ap_b[0]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('delay')")
    if ap_a[1] < ap_b[1]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('jitter')")
    if ap_a[2] < ap_b[2]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('packet_loss')")
    if ap_a[3] < ap_b[3]:
     exec("dset"+str(ap_number2)+"_"+str(apn_number2)+".append('av_bandwidth')")


def dset(dset,k,lf,n1,n2):
 discordant_attr = []
 dk = k[0] - lf[0]
 if dk < 0:
  dk = dk * (-1)
 jk = k[1] - lf[1]
 if jk < 0:
  jk = -(jk)
 plk = k[2] - lf[2]
 if plk < 0:
  plk = -(plk)
 abk = k[3] - lf[3]
 if abk < 0:
  abk = -(abk)
 for attr in dset:
  if attr == 'delay':
   discordant_attr.append(dk)
  if attr == 'jitter':
   discordant_attr.append(jk)
  if attr == 'packet_loss':
   discordant_attr.append(plk)
  if attr == 'av_bandwidth':
   discordant_attr.append(abk)
 var = (sum(discordant_attr))/(dk+jk+plk+abk)
 return var

for ap_number3 in ap_range:
  for apn_number3 in ap_range:
   if ap_number3 > apn_number3:
    exec("x = dset"+str(ap_number3)+"_"+str(apn_number3))
    exec("ap_a = ap"+str(ap_number3)+"_normalized")
    exec("ap_b = ap"+str(apn_number3)+"_normalized")
    dn = dset(x,ap_a,ap_b,ap_number3,apn_number3)
    exec("dset"+str(ap_number3)+"_"+str(apn_number3)+"= dn")
    all_dset.append(dn)
   if ap_number3 < apn_number3:
    exec("x = dset"+str(ap_number3)+"_"+str(apn_number3))
    exec("ap_a = ap"+str(ap_number3)+"_normalized")
    exec("ap_b = ap"+str(apn_number3)+"_normalized")
    dn = dset(x,ap_a,ap_b,ap_number3,apn_number3)
    exec("dset"+str(ap_number3)+"_"+str(apn_number3)+"= dn")
    all_dset.append(dn)

fmatrix = []
gmatrix = []
ematrix = []
for x in range(1,len(l)+1):
 fmatrix.append([0]*len(l))
 gmatrix.append([0]*len(l))
 ematrix.append([0]*len(l))
def cdom_ddom (c,cset):
 if cset >= c:
  return 1
 elif cset < c:
  v = 0
  return v

c = (sum(all_cset))/(nnu * (nnu-1))
d = (sum(all_dset))/(nnu * (nnu-1))
for nn in range(1,len(l)+1):
 for nc in range(1,len(l)+1):
  if nn != nc:
   if nn not in ap_range:
    fmatrix[nn-1][nc-1] = 0
    gmatrix[nn-1][nc-1] = 1
   else:
    if nc not in ap_range:
     fmatrix[nn-1][nc-1] = 1
     gmatrix[nn-1][nc-1] = 0
    else:
     exec("vf = cset"+str(nn)+"_"+str(nc))
     exec("vg = dset"+str(nn)+"_"+str(nc))
     vf = cdom_ddom(c,sum(vf))
     vg = cdom_ddom(d,vg)
     fmatrix[nn-1][nc-1] = vf
     gmatrix[nn-1][nc-1] = vg
  else:
    fmatrix[nn-1][nc-1] = 1
    gmatrix[nn-1][nc-1] = 0

for im in range(len(fmatrix)):
 for jm in range(len(gmatrix[0])):
  for ss in range(len(gmatrix)):
   ematrix[im][jm] += fmatrix[im][ss] * gmatrix[jm][ss]

score = []

for indexscore in ematrix:
 score.append(sum(indexscore)) 

print("ap" + str(score.index(max(score)) + 1))
#print (score)
