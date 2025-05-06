from django.contrib import admin
from .models import Banner, BannerClick, BannerView

class BannerAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'data_inicio', 'data_fim', 'valor_pago', 'clicks', 'visualizacoes', 'ativo')
    list_filter = ('ativo', 'data_inicio', 'data_fim')
    search_fields = ('nome_cliente',)

class BannerClickAdmin(admin.ModelAdmin):
    list_display = ('banner_info', 'timestamp')
    list_filter = ('banner', 'timestamp')
    date_hierarchy = 'timestamp'
    search_fields = ('banner__nome_cliente',)
    
    def banner_info(self, obj):
        return f"{obj.banner.nome_cliente} - Banner {obj.banner.id}"
    banner_info.short_description = 'Banner'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class BannerViewAdmin(admin.ModelAdmin):
    list_display = ('banner_info', 'timestamp')
    list_filter = ('banner', 'timestamp')
    date_hierarchy = 'timestamp'
    search_fields = ('banner__nome_cliente',)
    
    def banner_info(self, obj):
        return f"{obj.banner.nome_cliente} - Banner {obj.banner.id}"
    banner_info.short_description = 'Banner'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_export_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerClick, BannerClickAdmin)
admin.site.register(BannerView, BannerViewAdmin)
