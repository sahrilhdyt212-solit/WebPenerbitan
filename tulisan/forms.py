from django import forms
from .models import Karya

class KaryaForm(forms.ModelForm):
    class Meta:
        model = Karya
        # Tambahkan 'file_pdf' dan 'is_jurnal_ilmiah' ke dalam list fields
        fields = ['judul', 'penulis', 'kategori', 'isi', 'gambar', 'file_pdf', 'is_jurnal_ilmiah']
        
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan Judul Jurnal...'
            }),
            'penulis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Penulis...'
            }),
            'kategori': forms.Select(attrs={
                'class': 'form-select'
            }),
            'isi': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tuliskan abstrak atau isi naskah hukum progresif di sini...',
                'rows': 10
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            # Widget tambahan untuk PDF
            'file_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf' # Membatasi agar hanya bisa pilih PDF
            }),
            'is_jurnal_ilmiah': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    # --- VALIDASI TETAP DIPERTAHANKAN ---
    def clean_judul(self):
        judul = self.cleaned_data.get('judul')
        if len(judul) < 10:
            raise forms.ValidationError("Judul terlalu pendek. Minimal 10 karakter ya.")
        return judul

    def clean_isi(self):
        isi = self.cleaned_data.get('isi')
        # Menghitung kata (logika tetap sama)
        kata = isi.split()
        if len(kata) < 50: 
            raise forms.ValidationError(f"Naskah terlalu singkat (baru {len(kata)} kata). Minimal 50 kata untuk standar penerbitan.")
        return isi