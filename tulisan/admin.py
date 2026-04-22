from django.contrib import admin
from .models import Karya, Profile, Berita, Komentar

# Mempercantik tampilan daftar di Admin
class KaryaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'kategori', 'tanggal_terbit')
    list_filter = ('kategori', 'tanggal_terbit')
    search_fields = ('judul', 'penulis')

class KomentarAdmin(admin.ModelAdmin):
    # 'is_approved' dimunculin biar kelihatan mana yang udah tayang, mana yang belum
    list_display = ('nama', 'karya', 'is_approved', 'tanggal_tambah') 
    
    # Baris sakti: biar lo bisa centang/uncentang langsung di daftar tanpa klik detail
    list_editable = ('is_approved',) 
    
    list_filter = ('is_approved', 'tanggal_tambah')
    search_fields = ('nama', 'isi')

# Daftarkan semua model ke Admin
admin.site.register(Profile)
admin.site.register(Karya, KaryaAdmin)
admin.site.register(Berita)
admin.site.register(Komentar, KomentarAdmin)