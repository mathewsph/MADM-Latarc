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

def cr(max_difference_attr,min_difference_attr,zeta,g):
  if max_difference_attr < 0:
     max_difference_attr = max_difference_attr * (-1)
  if min_difference_attr < 0:
     min_difference_attr = min_difference_attr * (-1)
  if g < 0:
     g = g*(-1)     
  h = ((min_difference_attr) + (zeta*(max_difference_attr))) / ( (g) + (zeta * (max_difference_attr)))
  return h


l = [0] * n
q = [0] * n

attrd = ['delay','jitter','packet_loss','av_bandwidth']

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
  exec("%s = %s" % (k + "_normalized_cr",[]))
  exec("%s = %s" % (k + "_normalized_cr_neg",[]))
  exec("%s = %s" % (k + "_normalized",[]))
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


for j in attr:
  exec ('apc =' + j)
  for e in apc:
   exec(j+'_x.append(e**2)')

for ab in range(1,(int(n)+1)):		#Normalizacao com a equacao "rij" Multiplicacao dos pesos pelo resultado da equacao anterior
 if ab in ap_range:
  g = str(ab)
  exec("ap_list = ap"+g)
#  exec("apc = math.sqrt(sum(ap" + g + "_normalized))")
  for attr_value in ap_list:
#     print (attr_value)
#     exec("ap" + g + "[(ap_list.index(attr_value))] = attr_value/apc")
#  for attr_valuen2 in ap_list:
     if ap_list.index(attr_value) == 0:
       apc = math.sqrt(sum(delay_x))
       exec("ff = attr_value/apc")
       exec("ap" + g + "[(ap_list.index(attr_value))] = (ff*delay_weight)")
       delay_normalized.append(ff)
     elif ap_list.index(attr_value) == 1:
       apc = math.sqrt(sum(jitter_x))
       exec("ff = attr_value/apc")
       exec("ap" + g + "[(ap_list.index(attr_value))] = (ff*jitter_weight)")
       jitter_normalized.append(ff)
     elif ap_list.index(attr_value) == 2:
       apc = math.sqrt(sum(packet_loss_x))
       exec("ff = attr_value/apc")
       exec("ap" + g + "[(ap_list.index(attr_value))] = (ff*packet_loss_weight)")
       packet_loss_normalized.append(ff)
     elif ap_list.index(attr_value) == 3:
       apc = math.sqrt(sum(av_bandwidth_x))
       exec("ff = attr_value/apc")
       exec("ap" + g + "[(ap_list.index(attr_value))] = (ff*av_bandwidth_weight)")
       av_bandwidth_normalized.append(ff)

###cod-gra
zeta = 0.5

for apt in l:			#Laco que fara a funcao das formulas de normalizacao A+ e A- (definicao das redes ideais positivas e negativas)
 if apt != 0:
  for attr in apt:
   if attr == "delay" or attr == "jitter" or attr == "packet_loss":
    exec(attr+"_max = min(" + attr + "_normalized)")
    exec(attr+"_min = max(" + attr + "_normalized)")
   elif attr == "throughput" or attr == "av_bandwidth":
    exec(attr+"_max = max(" + attr + "_normalized)")
    exec(attr+"_min = min(" + attr + "_normalized)")

#print len(l)

for attr in attrd:		#series padroes (default series = "ds"), para calculo dos coeficientes relacionais
 exec('ds_'+ attr +'_max_max =  (' + attr + '_max - '+ attr + '_max)')
 exec('ds_'+ attr +'_max_min =  (' + attr + '_max - '+ attr + '_min)')
 exec('ds_'+ attr +'_min_max =  (' + attr + '_min - '+ attr + '_max)')
 exec('ds_'+ attr +'_min_min =  (' + attr + '_min - '+ attr + '_min)')

for av in range(1,(int(n)+1)):		#Normalizacao com a equacao "rij" Multiplicacao dos pesos pelo resultado da equacao anterior
 if av in ap_range:
  gv = str(av)
  exec("list_ap = ap"+gv)
#  exec("apc = math.sqrt(sum(ap" + g + "_normalized))")
  for value_attr in list_ap:
#     print (list_ap)
     if list_ap.index(value_attr) == 0:
          dv = cr(ds_delay_max_min,ds_delay_max_max,0.5,(delay_max - value_attr))
          dv_neg = cr(ds_delay_min_max,ds_delay_min_min,0.5,(delay_min - value_attr))
          print (dv)
          exec("ap"+str(av)+"_normalized_cr.append(dv)")
          exec("ap"+str(av)+"_normalized_cr_neg.append(dv_neg)")
     elif list_ap.index(value_attr) == 1:
          dv = cr(ds_jitter_max_min,ds_jitter_max_max,0.5,(jitter_max - value_attr))
          dv_neg = cr(ds_jitter_min_max,ds_jitter_min_min,0.5,(jitter_min - value_attr))
          print (dv)
          exec("ap"+str(av)+"_normalized_cr.append(dv)")
          exec("ap"+str(av)+"_normalized_cr_neg.append(dv_neg)")
     elif list_ap.index(value_attr) == 2:
          dv = cr(ds_packet_loss_max_min,ds_packet_loss_max_max,0.5,(packet_loss_max - value_attr))
          dv_neg = cr(ds_packet_loss_min_max,ds_packet_loss_min_min,0.5,(packet_loss_min - value_attr))
          print (dv)
          exec("ap"+str(av)+"_normalized_cr.append(dv)")
          exec("ap"+str(av)+"_normalized_cr_neg.append(dv_neg)")
     elif list_ap.index(value_attr) == 3:
          dv = cr(ds_av_bandwidth_max_min,ds_av_bandwidth_max_max,0.5,(av_bandwidth_max - value_attr))
          dv_neg = cr(ds_av_bandwidth_min_max,ds_av_bandwidth_min_min,0.5,(av_bandwidth_min - value_attr))
          print (dv)
          exec("ap"+str(av)+"_normalized_cr.append(dv)")
          exec("ap"+str(av)+"_normalized_cr_neg.append(dv_neg)")

for n in range(1,len(l)+1):
 if n in ap_range:
  b = str(n)
  exec("%s = %s" % ("ap"+b+"_score_pos",[0,0,0,0]))
  exec("z = ap"+b+"_normalized_cr")
  exec("ap"+b+"_score_pos[0]=z[0]*delay_weight")
  exec("ap"+b+"_score_pos[1]=z[1]*jitter_weight")
  exec("ap"+b+"_score_pos[2]=z[2]*packet_loss_weight")
  exec("ap"+b+"_score_pos[3]=z[3]*av_bandwidth_weight")

for n_n in range(1,len(l)+1):
 if n_n in ap_range:
  b_n = str(n_n)
  exec("%s = %s" % ("ap"+b_n+"_score_neg",[0,0,0,0]))
  exec("z_n = ap"+b_n+"_normalized_cr_neg")
  exec("ap"+b_n+"_score_neg[0]=z_n[0]*delay_weight")
  exec("ap"+b_n+"_score_neg[1]=z_n[1]*jitter_weight")
  exec("ap"+b_n+"_score_neg[2]=z_n[2]*packet_loss_weight")
  exec("ap"+b_n+"_score_neg[3]=z_n[3]*av_bandwidth_weight")

for ap_number in range(1,(int(n)+1)):		#sera executada a soma dos atributos normalizados e com os pesos, dando a pontuacao final da rede
 if ap_number in ap_range:
  index = str(ap_number-1)
  ap_number = str(ap_number)
  exec("q["+ index + "]=( sum(ap" + ap_number + "_score_pos) / sum(ap" + ap_number + "_score_neg) )")

print(q) #Pontuacao de todas as redes avaliadas (na ordem numerica de 1 ate n).

print("rede " + str(q.index(max(q)) + 1))	#Melhor rede entre as candidatas
print("pontuacao da rede: " + str(max(q)))	#Pontuacao dessa rede