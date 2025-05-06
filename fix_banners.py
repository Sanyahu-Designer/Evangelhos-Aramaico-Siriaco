import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bible_project.settings')
django.setup()

from banners.models import Banner

def fix_banner_urls():
    banners = Banner.objects.all()
    for banner in banners:
        if 'staging.sanyahudesigner.com.br' in banner.imagem.name:
            new_url = banner.imagem.name.split('/media/')[-1]
            banner.imagem.name = new_url
            banner.save()
            print(f"Updated banner {banner.id}: {banner.imagem.name}")

if __name__ == '__main__':
    fix_banner_urls()