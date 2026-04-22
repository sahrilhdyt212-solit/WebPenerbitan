from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.http import HttpResponseForbidden # Tambahan untuk keamanan
from django.contrib.auth.models import User # Tambahan untuk profil
from .models import Karya, Berita, Komentar
from .forms import KaryaForm
from django.shortcuts import render
from .models import Berita

#---- BERITA-------
def daftar_karya_view(request):
    # Ambil semua data berita dari database
    berita_list = Berita.objects.all().order_by('-id') 
    
    # Render ke file yang lagi kamu edit di screenshot tadi
    return render(request, 'tulisan/daftar_karya.html', {
        'berita_list': berita_list
    })

# --- 1. HALAMAN DEPAN (Fokus Artikel/Opini) ---
def daftar_karya(request):
    query = request.GET.get('q')
    kategori_filter = request.GET.get('kategori') 
    
    # MODIFIKASI: Hanya ambil yang BUKAN jurnal ilmiah untuk beranda
    karya_list = Karya.objects.filter(is_published=True, is_jurnal_ilmiah=False)

    if query:
        karya_list = karya_list.filter(
            Q(judul__icontains=query) | Q(isi__icontains=query)
        )
    
    if kategori_filter:
        karya_list = karya_list.filter(kategori=kategori_filter)

    karya_list = karya_list.order_by('-id')
    berita_list = Berita.objects.all().order_by('-tanggal_post')[:5] 
    
    return render(request, 'tulisan/daftar_karya.html', {
        'karya_list': karya_list,
        'berita_list': berita_list,
        'query': query,
        'kategori_aktif': kategori_filter 
    })

# --- BARU: HALAMAN KHUSUS ARSIP JURNAL PDF ---
def daftar_jurnal(request):
    query = request.GET.get('q')
    
    # Hanya ambil yang ditandai sebagai Jurnal Ilmiah
    jurnal_list = Karya.objects.filter(is_published=True, is_jurnal_ilmiah=True)

    if query:
        jurnal_list = jurnal_list.filter(
            Q(judul__icontains=query) | Q(penulis__icontains=query)
        )

    jurnal_list = jurnal_list.order_by('-id')
    terpopuler = Karya.objects.filter(is_published=True).order_by('-id')[:5]
    
    return render(request, 'tulisan/daftar_jurnal.html', {
        'jurnal_list': jurnal_list,
        'terpopuler': terpopuler,
        'query': query
    })

# --- 2. DETAIL NASKAH ---
def detail_karya(request, id):
    karya = get_object_or_404(Karya, id=id)
    
    if request.method == "POST":
        nama_in = request.POST.get('nama')
        isi_in = request.POST.get('isi')
        if nama_in and isi_in:
            Komentar.objects.create(karya=karya, nama=nama_in, isi=isi_in)
            messages.success(request, "Komentar kamu berhasil dikirim!")
            return redirect('detail_karya', id=id)

    komentar_list = karya.komentars.all().order_by('-tanggal_tambah')
    
    baca_juga = Karya.objects.filter(
        kategori=karya.kategori, 
        is_published=True
    ).exclude(id=karya.id).order_by('-id')[:3]
    
    terpopuler = Karya.objects.filter(is_published=True).order_by('-id')[:5]
    
    context = {
        'karya': karya,
        'baca_juga': baca_juga,
        'terpopuler': terpopuler,
        'komentar_list': komentar_list,
    }
    return render(request, 'tulisan/detail_karya.html', context)

# --- 3. TAMBAH & EDIT NASKAH (SESUAI MULTI-PENULIS) ---
@login_required(login_url='login')
def tambah_karya(request, id=None):
    if id:
        karya = get_object_or_404(Karya, id=id)
        # KEAMANAN: Cek apakah user yang login adalah pemilik naskah atau staff/admin
        if karya.penulis_user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("Anda tidak memiliki izin untuk mengedit naskah ini.")
        edit_mode = True
    else:
        karya = None
        edit_mode = False

    if request.method == "POST":
        form = KaryaForm(request.POST, request.FILES, instance=karya) 
        if form.is_valid():
            naskah = form.save(commit=False)
            
            # OTOMATIS: Hubungkan ke akun penulis jika baru buat
            if not edit_mode:
                naskah.penulis_user = request.user
            
            action = request.POST.get('action')
            if action == 'publish':
                naskah.is_published = True
                naskah.save()
                messages.success(request, f"Naskah '{naskah.judul}' resmi diterbitkan!")
                return redirect('home')
            else:
                naskah.is_published = False
                naskah.save()
                messages.info(request, "Perubahan draf berhasil disimpan!")
                return redirect('daftar_draft')
        else:
            messages.error(request, "Gagal menyimpan. Pastikan semua kolom terisi dengan benar.")
    else:
        form = KaryaForm(instance=karya)
    
    return render(request, 'tulisan/tambah_karya.html', {
        'form': form, 
        'edit_mode': edit_mode,
        'karya': karya 
    })

# --- 4. HALAMAN DRAF (FILTERED BY USER) ---
@login_required(login_url='login')
def daftar_draft(request):
    # Hanya tampilkan draf milik user yang login
    draft_list = Karya.objects.filter(penulis_user=request.user, is_published=False).order_by('-id')
    terpopuler = Karya.objects.filter(is_published=True).order_by('-id')[:5]
    
    return render(request, 'tulisan/daftar_draft.html', {
        'karya_list': draft_list,
        'terpopuler': terpopuler
    })

# --- 5. HAPUS NASKAH (PROTECTED) ---
@login_required(login_url='login')
def hapus_karya(request, id):
    karya = get_object_or_404(Karya, id=id)
    
    # KEAMANAN: Pastikan hanya pemilik yang bisa hapus
    if karya.penulis_user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk menghapus naskah ini.")
        
    if request.method == "POST":
        judul_naskah = karya.judul
        karya.delete()
        messages.warning(request, f"Naskah '{judul_naskah}' telah dihapus.")
        return redirect('daftar_draft')
    return render(request, 'tulisan/konfirmasi_hapus.html', {'karya': karya})

# --- 6. HALAMAN PROFIL PENULIS ---
def profil_penulis(request, username):
    # Cari user berdasarkan username
    user_penulis = get_object_or_404(User, username=username)
    
    # Ambil karya yang sudah dipublish oleh user tersebut
    karya_list = Karya.objects.filter(penulis_user=user_penulis, is_published=True).order_by('-id')
    
    return render(request, 'tulisan/profil_penulis.html', {
        'penulis': user_penulis,
        'karya_list': karya_list
    })

# --- 7. AUTENTIKASI ---
def login_view(request):
    if request.method == "POST":
        user_in = request.POST.get('username')
        pass_in = request.POST.get('password')
        user = authenticate(request, username=user_in, password=pass_in)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang kembali, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Username atau Password salah!")
    return render(request, 'tulisan/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah keluar dari sistem.")
    return redirect('home')