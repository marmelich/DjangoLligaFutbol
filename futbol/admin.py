from django.contrib import admin


from futbol.models import *

admin.site.register(Lliga)


class EquipAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Equip.objects.all()
        user = request.user
        equips = user.equips.all()
        equips_ids = [e.id for e in equips]
        qs = Equip.objects.filter(pk__in=equips_ids)
        return qs

admin.site.register(Equip, EquipAdmin)

admin.site.register(Jugador)

# class JugadorAdmin(admin.ModelAdmin):
#     search_fields = ("nom", "equip__nom")
# admin.site.register(Jugador.JugadorAdmin)

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

from django.contrib.auth.admin import UserAdmin

class UsuariAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Lliga", {"fields": ["equips", "telefon"]}),)
    filter_horizontal = UserAdmin.filter_horizontal + ("equips",)


admin.site.register(Usuari, UsuariAdmin)