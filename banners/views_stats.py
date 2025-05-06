from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from .models import Banner, BannerClick, BannerView

def banner_stats(request):
    period = request.GET.get('period', 'day')
    
    # Define o truncamento baseado no período
    if period == 'week':
        trunc_function = TruncWeek
        days_ago = 7 * 4  # 4 semanas
    elif period == 'month':
        trunc_function = TruncMonth
        days_ago = 30 * 3  # 3 meses
    else:  # day
        trunc_function = TruncDay
        days_ago = 7  # 7 dias
    
    # Data inicial para filtro
    start_date = timezone.now() - timezone.timedelta(days=days_ago)
    
    # Agrupa clicks por período
    clicks = BannerClick.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        period=trunc_function('timestamp')
    ).values('period').annotate(
        total=Count('id')
    ).order_by('period')
    
    # Agrupa visualizações por período
    views = BannerView.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        period=trunc_function('timestamp')
    ).values('period').annotate(
        total=Count('id')
    ).order_by('period')
    
    # Prepara dados para o template
    stats_data = {
        'labels': [],
        'clicks': [],
        'views': [],
        'ctr': []
    }
    
    # Combina dados de clicks e views
    for date in clicks:
        stats_data['labels'].append(date['period'].strftime('%d/%m/%Y'))
        stats_data['clicks'].append(date['total'])
        
        # Encontra visualizações correspondentes
        view_count = next(
            (v['total'] for v in views if v['period'] == date['period']),
            0
        )
        stats_data['views'].append(view_count)
        
        # Calcula CTR
        ctr = (date['total'] / view_count * 100) if view_count > 0 else 0
        stats_data['ctr'].append(round(ctr, 2))
    
    return render(request, 'banners/stats.html', {
        'stats_data': stats_data,
        'period': period
    })
