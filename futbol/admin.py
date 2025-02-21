from django.contrib import admin


from futbol.models import *

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

# class JugadorAdmin(admin.ModelAdmin):
#     search_fields = ("nom",)
#     admin.site.register(Jugador.JugadorAdmin)

class EventInline(admin.TabularInline): #esto hace que dentro de 1 partido puedas añadir los eventos
    model = Event
    extra = 2


class PartitAdmin(admin.ModelAdmin):
    list_display = ("equip_local", "equip_visitant", "data", "gols_local", "gols_visitant") #esto hace que se muestren estos datos en la tabla partidos
    fields = ("lliga","equip_local", "equip_visitant","data","gols_local", "gols_visitant") #camps que hem decidit que volem que surtin
    readonly_fields = ("lliga","gols_local", "gols_visitant") #nomes de lectura, si no surten en el anterior, no funcionará
    search_fields = ("equip_local__nom", "equip_visitant__nom")
    inlines = [EventInline,]


admin.site.register(Partit, PartitAdmin)