from django import template
from home.models import DeliveryFeature

register = template.Library()

@register.inclusion_tag('partials/delivery_section.html', takes_context=False)
def delivery_section(page_key='all'):
    qs = DeliveryFeature.objects.filter(is_active=True).order_by('sort_order', 'id')
    if not page_key or page_key == 'all':
        return { 'features': list(qs) }
    filtered = []
    key = str(page_key).lower().strip()
    for f in qs:
        pages = (f.pages or '').lower()
        tokens = [t.strip() for t in pages.split(',') if t.strip()]
        if not tokens or 'all' in tokens or key in tokens:
            filtered.append(f)
    return { 'features': filtered }
