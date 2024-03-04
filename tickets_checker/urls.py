from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main),
    path('main', views.main, name='main'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('ticket_info/<str:ticket_code>', views.ticket_info, name='ticket_info'),
    path('add_ticket', views.add_ticket, name='add_ticket'),
    path('success_url', views.show_success_page, name='success_url'),
    path('update_ticket_vouchers/<str:ticket_code>', views.update_ticket_vouchers, name='update_ticket_vouchers')

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
