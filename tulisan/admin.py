from django.contrib import admin
from .models import Karya, Profile, Berita, Komentar

# Mempercantik tampilan daftar di Admin
class KaryaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'kategori', 'tanggal_terbit')
    list_filter = ('kategori', 'tanggal_terbit')
    search_fields = ('judul', 'penulis')

class KomentarAdmin(admin.ModelAdmin):
    list_display = ('nama', 'karya', 'tanggal_tambah')
    list_filter = ('tanggal_tambah',)
    search_fields = ('nama', 'isi')

# Daftarkan semua model ke Admin
admin.site.register(Profile)
admin.site.register(Karya, KaryaAdmin)
admin.site.register(Berita)
admin.site.register(Komentar, KomentarAdmin)