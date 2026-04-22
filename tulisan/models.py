from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from cloudinary.models import CloudinaryField # <--- IMPORT WAJIB

# --- MODEL PROFIL PENULIS (UNTUK FOTO & BIO) ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Pakai CloudinaryField, default langsung ke nama file di Cloudinary Home
    foto = CloudinaryField('image', folder='profile_pics/', default='default.png', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Profil {self.user.username}"

# --- SIGNALS UNTUK OTOMATISASI PROFIL ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Karya(models.Model):
    penulis_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daftar_karya', null=True, blank=True)
    
    KATEGORI_CHOICES = [
        ('pidana', 'Hukum Pidana'),
        ('perdata', 'Hukum Perdata'),
        ('htn', 'Hukum Tata Negara'),
        ('han', 'Hukum Administrasi Negara'),
    ]

    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    
    isi = RichTextField() 
    # Ganti ke CloudinaryField
    gambar = CloudinaryField('image', folder='naskah/', blank=True, null=True)
    
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='pidana')
    is_published = models.BooleanField(default=False)
    tanggal_terbit = models.DateTimeField(auto_now_add=True)

    # Untuk PDF tetep pakai FileField (Cloudinary free tier fokus ke gambar/video)
    file_pdf = models.FileField(upload_to='jurnal_pdf/', blank=True, null=True)
    is_jurnal_ilmiah = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.judul

# 4. Model untuk Berita SOLIT
class Berita(models.Model):
    judul = models.CharField(max_length=200)
    isi = RichTextField() 
    # Ganti ke CloudinaryField
    gambar = CloudinaryField('image', folder='berita/', blank=True, null=True)
    tanggal_post = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

# --- TAMBAHAN MODEL KOMENTAR ---
class Komentar(models.Model):
    karya = models.ForeignKey(Karya, on_delete=models.CASCADE, related_name='komentars')
    nama = models.CharField(max_length=100)
    isi = models.TextField() 
    tanggal_tambah = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentar oleh {self.nama} di {self.karya.judul}"