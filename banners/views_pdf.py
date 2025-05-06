from django.http import HttpResponse
from django.db.models import Count
from .models import Banner, BannerClick, BannerView
from datetime import datetime, timedelta
import locale
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import io

# Configurar locale para português
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def export_stats_pdf(request):
    # Pegar os filtros da URL
    banner_id = request.GET.get('banner')
    data_str = request.GET.get('data')
    
    # Inicializar queryset
    views_query = BannerView.objects.all()
    clicks_query = BannerClick.objects.all()
    
    # Aplicar filtros se fornecidos
    if banner_id:
        views_query = views_query.filter(banner_id=banner_id)
        clicks_query = clicks_query.filter(banner_id=banner_id)
        banner_nome = Banner.objects.get(id=banner_id).nome_cliente
    else:
        banner_nome = "Todos os Banners"
    
    if data_str:
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d')
            data_fim = data + timedelta(days=1)
            views_query = views_query.filter(timestamp__range=(data, data_fim))
            clicks_query = clicks_query.filter(timestamp__range=(data, data_fim))
            periodo = f"Data: {data.strftime('%d/%m/%Y')}"
        except ValueError:
            periodo = "Todas as datas"
    else:
        periodo = "Todas as datas"
    
    # Agrupar dados por banner
    if banner_id:
        banners = Banner.objects.filter(id=banner_id)
    else:
        banners = Banner.objects.all()
    
    # Preparar dados
    table_data = []
    total_views = 0
    total_clicks = 0
    
    # Cabeçalho da tabela
    table_data.append(['Banner', 'Visualizações', 'Clicks', 'CTR', 'Período de Atividade'])
    
    for banner in banners:
        views = views_query.filter(banner=banner).count()
        clicks = clicks_query.filter(banner=banner).count()
        ctr = f"{(clicks / views * 100) if views > 0 else 0:.2f}%"
        periodo_banner = f"{banner.data_inicio.strftime('%d/%m/%Y')} até {banner.data_fim.strftime('%d/%m/%Y')}"
        
        table_data.append([
            banner.nome_cliente or "Sem nome",
            str(views),
            str(clicks),
            ctr,
            periodo_banner
        ])
        
        total_views += views
        total_clicks += clicks
    
    # Linha de totais
    total_ctr = f"{(total_clicks / total_views * 100) if total_views > 0 else 0:.2f}%"
    table_data.append([
        'TOTAL',
        str(total_views),
        str(total_clicks),
        total_ctr,
        ''
    ])
    
    # Criar PDF com ReportLab
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Definir estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=30
    )
    
    # Elementos do PDF
    elements = []
    
    # Título
    title = Paragraph(f"Relatório de Estatísticas - {banner_nome}", title_style)
    elements.append(title)
    
    # Informações do período
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        spaceAfter=20
    )
    info = Paragraph(f"Período: {periodo}<br/>Gerado em: {datetime.now().strftime('%d de %B de %Y às %H:%M')}", info_style)
    elements.append(info)
    
    # Estatísticas principais
    stats_data = [[
        f"Total de Visualizações\n{total_views}",
        f"Total de Clicks\n{total_clicks}",
        f"CTR Médio\n{total_ctr}"
    ]]
    stats_table = Table(stats_data, colWidths=[doc.width/3.0]*3)
    stats_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 20))
    
    # Tabela principal
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ]))
    elements.append(table)
    
    # Rodapé
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1,
        spaceBefore=30
    )
    footer = Paragraph("Evangelhos Aramaico Siríaco - Todos os direitos reservados", footer_style)
    elements.append(footer)
    
    # Gerar PDF
    doc.build(elements)
    
    # Preparar resposta
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="estatisticas_{banner_nome}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response

def test_weasyprint(request):
    from weasyprint import HTML
    import tempfile
    import os
    
    # HTML simples sem estilos
    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Teste WeasyPrint</title>
    </head>
    <body>
        <h1>Teste do WeasyPrint</h1>
        <p>Este é um teste simples.</p>
    </body>
    </html>
    """
    
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        # Criar o PDF
        HTML(string=html_string).write_pdf(tmp.name)
        
        # Ler o arquivo PDF
        tmp.seek(0)
        pdf_content = tmp.read()
        
    # Excluir o arquivo temporário
    os.unlink(tmp.name)
    
    # Criar response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="teste_weasyprint.pdf"'
    
    return response