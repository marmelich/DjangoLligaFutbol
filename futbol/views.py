from django.shortcuts import render

# Create your views here.

from futbol.models import *

def classificacio(request):
    lliga = Lliga.objects.all()[1]
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        victories = 0
        derrotes = 0
        empats = 0
        gols_local_total = 0
        gols_visitant_total = 0
        gols_average = 0

        for partit in lliga.partits.filter(equip_local=equip):
            gols_local_total += partit.gols_local()
            if partit.gols_local() > partit.gols_visitant():
                #victoria
                punts += 3
                victories += 1
            elif partit.gols_local() == partit.gols_visitant():
                #empat
                punts += 1
                empats +=1
            else:
                derrotes +=1
            #else derrotes
        for partit in lliga.partits.filter(equip_visitant=equip):
            gols_visitant_total += partit.gols_visitant()
            if partit.gols_local() < partit.gols_visitant():
                #victoria
                punts += 3
                victories += 1
            elif partit.gols_local() == partit.gols_visitant():
                #empat
                punts += 1
                empats +=1
            else:
                derrotes +=1
            #else derrotes
        gols_average = round(gols_local_total/gols_visitant_total)
        classi.append( {"punts":punts, "equip":equip.nom, "victories":victories, "derrotes":derrotes, "empats":empats, "gols_local_total":gols_local_total, "gols_visitant_total":gols_visitant_total, "gols_average":gols_average,} )
    # ordenem llista
    classi.sort(reverse=True, key=lambda x: x["punts"])
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga
                })