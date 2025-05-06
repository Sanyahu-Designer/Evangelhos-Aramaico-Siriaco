#!/usr/bin/env python
"""
Script para adicionar categorias de conteúdo e associá-las a versículos.
Execute com: python add_categories.py
"""

import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bible_project.settings')
django.setup()

from bible_app.models import ContentCategory, VerseCategory, Verse, Book, Chapter

def create_categories():
    """Criar categorias de conteúdo."""
    categories = [
        {
            'name': 'Parábolas',
            'description': 'Histórias e parábolas contadas por Jesus',
            'color': '#e74c3c',
            'icon': 'bi-chat-quote'
        },
        {
            'name': 'Milagres',
            'description': 'Milagres realizados por Jesus',
            'color': '#3498db',
            'icon': 'bi-stars'
        },
        {
            'name': 'Discursos',
            'description': 'Principais discursos e sermões',
            'color': '#2ecc71',
            'icon': 'bi-megaphone'
        },
        {
            'name': 'Profecias',
            'description': 'Profecias sobre o Messias e eventos futuros',
            'color': '#9b59b6',
            'icon': 'bi-calendar-event'
        }
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = ContentCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'color': cat_data['color'],
                'icon': cat_data['icon']
            }
        )
        
        if created:
            print(f"Categoria criada: {category.name}")
        else:
            print(f"Categoria já existente: {category.name}")
            
        created_categories.append(category)
    
    return created_categories

def associate_verses_to_categories(categories):
    """Associar versículos às categorias."""
    # Mapear categorias por nome para fácil acesso
    category_map = {cat.name: cat for cat in categories}
    
    # Obter todos os livros disponíveis
    books = Book.objects.all()
    print(f"Livros disponíveis: {[book.name for book in books]}")
    
    # Vamos usar os primeiros capítulos e versículos disponíveis para cada categoria
    for book in books:
        print(f"\nProcessando livro: {book.name}")
        
        # Obter os primeiros capítulos do livro
        chapters = Chapter.objects.filter(book=book).order_by('number')[:3]
        
        if not chapters:
            print(f"Nenhum capítulo encontrado para o livro {book.name}")
            continue
            
        for i, chapter in enumerate(chapters):
            print(f"Processando capítulo: {chapter.number}")
            
            # Obter os primeiros versículos do capítulo
            verses = Verse.objects.filter(chapter=chapter).order_by('number')[:5]
            
            if not verses:
                print(f"Nenhum versículo encontrado para o capítulo {chapter.number}")
                continue
                
            # Distribuir versículos entre as categorias
            for j, verse in enumerate(verses):
                # Escolher uma categoria com base no índice
                category_index = (i + j) % len(categories)
                category = categories[category_index]
                
                # Criar a associação
                verse_category, created = VerseCategory.objects.get_or_create(
                    verse=verse,
                    category=category,
                    defaults={
                        'is_primary': True,
                        'notes': f'Exemplo de {category.name} em {book.name} {chapter.number}:{verse.number}'
                    }
                )
                
                if created:
                    print(f"Associação criada: {verse} - {category.name}")
                else:
                    print(f"Associação já existente: {verse} - {category.name}")
    
    # Não precisamos deste código, pois não estamos mais usando associations

if __name__ == '__main__':
    print("Criando categorias...")
    categories = create_categories()
    
    print("\nAssociando versículos às categorias...")
    associate_verses_to_categories(categories)
    
    print("\nProcesso concluído!")
