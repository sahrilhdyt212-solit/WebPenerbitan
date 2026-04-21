from django.contrib import admin
from django.urls import path
from tulisan import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.daftar_karya, name='home'),
    path('drafts/', views.daftar_draft, name='daftar_draft'),
    path('tambah/', views.tambah_karya, name='tambah_karya'),
    path('edit/<int:id>/', views.tambah_karya, name='edit_karya'), 
    path('karya/<int:id>/', views.detail_karya, name='detail_karya'),
    path('karya/hapus/<int:id>/', views.hapus_karya, name='hapus_karya'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('jurnal/', views.daftar_jurnal, name='daftar_jurnal'),
    path('profil/<str:username>/', views.profil_penulis, name='profil_penulis'),
]

# Pastikan ini berada di luar list urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Tambahkan ini juga agar file static (CSS/JS) lebih aman terbaca
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)