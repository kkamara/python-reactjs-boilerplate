from django.views.generic import TemplateView
from django_ratelimit.decorators import ratelimit

catchall = ratelimit(
    key='ip', 
    rate='40/m', 
    method='GET'
)(TemplateView.as_view(template_name='index.html'))
