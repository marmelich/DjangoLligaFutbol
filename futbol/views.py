from django.shortcuts import render, redirect
from django import forms
from futbol.models import *


class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    dades = forms.CharField(required=False)

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = "__all__"


def taula_partits(request):
    resultats = []
    form = MenuForm()
    context = {"form": form, "resultats": resultats}

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            equips = list(lliga.equips.all())
            
            # Primera fila con nombres de equipos
            header = [""] + [equip.nom for equip in equips]
            resultats.append(header)
            
            # Generar matriz de resultados
            for equip_local in equips:
                fila = [equip_local.nom]
                for equip_visitant in equips:
                    if equip_local == equip_visitant:
                        fila.append("X")
                    else:
                        gols = 0
                        try:
                            partit = lliga.partits.get(equip_local=equip_local, equip_visitant=equip_visitant)
                            gols = partit.gols_local()
                        except Partit.DoesNotExist:
                            pass
                        fila.append(gols)
                resultats.append(fila)
            
            context = {
                "form": form,
                "resultats": resultats,
                "lliga_seleccionada": lliga.nom
            }
    
    return render(request, "taula_partits.html", context)


def pichichis(request):
    jugadors = []
    form = MenuForm()
    lliga = None

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data["lliga"]
            qs = Jugador.objects.filter(equip__lliga=lliga)

            for jugador in qs:
                gols = Event.objects.filter(jugador=jugador, tipus_esdeveniment="gol").count()
                jugadors.append({
                    "gols": gols,
                    "equip": jugador.equip.nom,
                    "nom": jugador.nom
                })

            jugadors.sort(reverse=True, key=lambda x: x["gols"])

    return render(request, "pichichis.html", {
        "jugadors": jugadors,
        "form": form,
        "lliga": lliga
    })


def nou_jugador(request):
    form = JugadorForm()
    if request.method == "POST":
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nou_jugador')
    return render(request, "menu.html", {"form":form})
 
 
def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })


def classificacio(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
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