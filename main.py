from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import os
import subprocess

class NotepadSuperCustom(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Area teks utama (Font 18 agar nyaman mengetik)
        self.text_input = TextInput(text='', multiline=True, font_size=18, padding=10)
        self.layout.add_widget(self.text_input)
        
        # Baris Tombol Atas (Fitur Utama)
        btn_layout_1 = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        btn_new = Button(text='Baru', background_color=(0.2, 0.6, 1, 1))
        btn_new.bind(on_press=self.new_file)
        
        btn_open = Button(text='Buka File', background_color=(0.8, 0.6, 0.2, 1))
        btn_open.bind(on_press=self.open_file_dialog)
        
        btn_save = Button(text='Simpan As...', background_color=(0.2, 0.8, 0.2, 1))
        btn_save.bind(on_press=self.save_file_dialog)
        
        btn_layout_1.add_widget(btn_new)
        btn_layout_1.add_widget(btn_open)
        btn_layout_1.add_widget(btn_save)
        self.layout.add_widget(btn_layout_1)

        # Baris Tombol Bawah (Fitur Jalankan Script)
        btn_layout_2 = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        btn_run = Button(text='👉 JALANKAN SCRIPT (.sh / Bash)', background_color=(0.9, 0.2, 0.2, 1))
        btn_run.bind(on_press=self.run_script)
        btn_layout_2.add_widget(btn_run)
        self.layout.add_widget(btn_layout_2)
        
        self.current_path = ""
        return self.layout

    def new_file(self, instance):
        self.text_input.text = ''
        self.current_path = ""

    # MENAMPILKAN PENJELAJAH FILE UNTUK MEMBUKA SEMUA JENIS FILE TEKS (.txt, .srt, .sh)
    def open_file_dialog(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path='/sdcard' if os.path.exists('/sdcard') else '.')
        content.add_widget(file_chooser)
        
        select_btn = Button(text='Buka File Ini', size_hint_y=0.15)
        content.add_widget(select_btn)
        
        popup = Popup(title='Pilih File Teks/Subtitle/Script', content=content, size_hint=(0.9, 0.9))
        
        def load_file(btn_instance):
            if file_chooser.selection:
                selected_file = file_chooser.selection[0]
                with open(selected_file, 'r', encoding='utf-8', errors='ignore') as f:
                    self.text_input.text = f.read()
                self.current_path = selected_file
                popup.dismiss()
                
        select_btn.bind(on_press=load_file)
        popup.open()

    # MENAMPILKAN KOTAK UNTUK MENGETIK NAMA DAN EKSTENSI FILE (Custom Extension)
    def save_file_dialog(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input tempat Anda mengetik nama file + ekstensi (misal: subtitle.srt)
        filename_input = TextInput(text='catatan_baru.txt', multiline=False, size_hint_y=0.2, font_size=16)
        content.add_widget(filename_input)
        
        file_chooser = FileChooserListView(path='/sdcard' if os.path.exists('/sdcard') else '.')
        content.add_widget(file_chooser)
        
        save_btn = Button(text='Simpan Sekarang', size_hint_y=0.15)
        content.add_widget(save_btn)
        
        popup = Popup(title='Ketik Nama File & Ekstensinya (.srt, .txt, .sh)', content=content, size_hint=(0.9, 0.9))
        
        def execute_save(btn_instance):
            folder_tujuan = file_chooser.path
            nama_file = filename_input.text
            full_path = os.path.join(folder_tujuan, nama_file)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(self.text_input.text)
                
            self.current_path = full_path
            popup.dismiss()
            
        save_btn.bind(on_press=execute_save)
        popup.open()

    # EKSEKUSI SCRIPT AUTOMATION
    def run_script(self, instance):
        script_content = self.text_input.text
        try:
            proses = subprocess.run(script_content, shell=True, capture_output=True, text=True, timeout=10)
            output = f"\n\n--- HASIL EKSEKUSI ---\n{proses.stdout}"
            if proses.stderr:
                output += f"\n--- ERROR ---\n{proses.stderr}"
            self.text_input.text += output
        except Exception as e:
            self.text_input.text += f"\n\n--- GAGAL MENJALANKAN ---\n{str(e)}"

if __name__ == '__main__':
    NotepadSuperCustom().run()
