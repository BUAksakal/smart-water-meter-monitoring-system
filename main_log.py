import logging
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from PIL import Image, ImageTk
import json
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue, Empty

class DataDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Display")

        # Canvas oluştur ve arka plan resmi ekle
        self.canvas = tk.Canvas(root, width=800, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Arka plan resmini yükle
        self.bg_image = Image.open(r"C:\Baylan\Lora_Payload\Payload_Json\images.png")
        self.bg_image = self.bg_image.resize((800, 500), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor=tk.NW)

        # Header ekle
        self.header_label = tk.Label(root, text="Baylan Payload System", font=("Arial", 18, "bold"), bg="lightblue")
        self.header_label_window = self.canvas.create_window(400, 10, window=self.header_label, anchor=tk.N)

        # Metin alanı oluştur
        self.text_area = scrolledtext.ScrolledText(root, width=50, height=10, bg="white", fg="black", font=("Arial", 12))
        self.text_area_window = self.canvas.create_window(200, 100, window=self.text_area, anchor=tk.NW)

        # Decoded Data TextBox
        self.decoded_data_textbox = tk.Text(root, height=2, width=50, bg="lightgrey", font=("Arial", 12))
        self.decoded_data_window = self.canvas.create_window(200, 50, window=self.decoded_data_textbox, anchor=tk.NW)

        # Search Butonu
        self.search_button = tk.Button(root, text="Search", command=self.start_listener, bg="blue", fg="white")
        self.search_button_window = self.canvas.create_window(100, 100, window=self.search_button, anchor=tk.NW)

        # Live Data Butonu
        self.live_data_button = tk.Button(root, text="Live Data", command=self.start_web_ui, bg="green", fg="white")
        self.live_data_button_window = self.canvas.create_window(100, 150, window=self.live_data_button, anchor=tk.NW)

        # Manuel Data Butonu
        self.manual_data_button = tk.Button(root, text="Manuel Data", command=self.enter_manual_data, bg="orange", fg="white")
        self.manual_data_button_window = self.canvas.create_window(100, 200, window=self.manual_data_button, anchor=tk.NW)

        # Veriyi İşle Butonu
        self.process_data_button = tk.Button(root, text="Veriyi İşle", command=self.process_data, bg="purple", fg="white")
        self.process_data_button_window = self.canvas.create_window(100, 250, window=self.process_data_button, anchor=tk.NW)

        # İşlem Bitir Butonu
        self.stop_button = tk.Button(root, text="İşlem Bitir", command=self.stop_all_processes, bg="red", fg="white")
        self.stop_button_window = self.canvas.create_window(100, 300, window=self.stop_button, anchor=tk.NW)

        self.file_path = r"C:\Users\berke\OneDrive\Masaüstü\Uİ_LİVE\data_store.json"
        self.is_reading = False
        self.read_thread = None
        self.queue = Queue()
        self.manual_data = None
        self.listener_process = None
        self.web_ui_process = None

        # Watchdog için event handler ve observer
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_modified = self.on_file_modified
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=os.path.dirname(self.file_path), recursive=False)
        self.observer.start()

        # GUI güncellemeleri için arka plan thread'inden veri alacak
        self.check_queue()

        # Loglama başlatılmamış
        self.logging_started = False

    def start_logging(self):
        if not self.logging_started:
            logging.basicConfig(
                filename='app.log',
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
            )
            logging.info("Uygulama başlatıldı ve loglama başlatıldı.")
            self.logging_started = True

    def start_listener(self):
        self.start_logging()
        if not self.listener_process:
            self.listener_process = subprocess.Popen(['python', r'C:\Users\berke\OneDrive\Masaüstü\Uİ_LİVE\listener.py'])
            logging.info("Listener başlatıldı.")
            messagebox.showinfo("Başarı", "Listener başlatıldı.")
        else:
            messagebox.showinfo("Bilgi", "Listener zaten çalışıyor.")

    def start_web_ui(self):
        self.start_logging()
        if not self.web_ui_process:
            self.web_ui_process = subprocess.Popen(['python', r'C:\Users\berke\OneDrive\Masaüstü\Uİ_LİVE\web_ui.py'])
            logging.info("Web UI başlatıldı.")
            messagebox.showinfo("Başarı", "Web UI başlatıldı.")
        else:
            messagebox.showinfo("Bilgi", "Web UI zaten çalışıyor.")

    def enter_manual_data(self):
        decoded_data = simpledialog.askstring("Manuel Data", "Lütfen manuel veriyi girin:", parent=self.root)
        if decoded_data:
            self.manual_data = decoded_data
            logging.info(f"Manuel veri girildi: {decoded_data}")
            messagebox.showinfo("Başarı", "Manuel veri girildi.")
        else:
            self.manual_data = None
            logging.info("Manuel veri girilmedi.")

    def process_data(self):
        self.start_logging()
        try:
            if self.manual_data:
                self._process_data(self.manual_data)
            elif os.path.isfile(self.file_path):
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, list) and len(data) > 0:
                        decoded_data = data[0].get("decoded_data", "Veri bulunamadı")
                        self._process_data(decoded_data)
                    else:
                        logging.error("JSON dosyasında veri bulunamadı.")
                        messagebox.showerror("Hata", "JSON dosyasında veri bulunamadı.")
            else:
                logging.error("İşlenecek veri bulunamadı.")
                messagebox.showerror("Hata", "İşlenecek veri bulunamadı.")
        except Exception as e:
            logging.error(f"Hata: {e}")
            self.queue.put((f"Hata: {e}", "Kredi bulunamadı", "Pil bulunamadı", "Decoded Data: Veri bulunamadı", "Connection Type: Veri bulunamadı", "Meter Type: Veri bulunamadı", "Penalty: Veri bulunamadı", "Warning: Veri bulunamadı", "Versiyon: Bilinmiyor"))

    def stop_all_processes(self):
        self.start_logging()
        self.is_reading = False
        if self.read_thread is not None:
            self.read_thread.join()
        if self.listener_process:
            self.listener_process.terminate()
            self.listener_process = None
            logging.info("Listener işlemi durduruldu.")
        if self.web_ui_process:
            self.web_ui_process.terminate()
            self.web_ui_process = None
            logging.info("Web UI işlemi durduruldu.")
        self.manual_data = None
        self._update_text_area("Tüm işlemler durduruldu.", "Kredi bulunamadı", "Pil bulunamadı", "Decoded Data: Veri bulunamadı", "Connection Type: Veri bulunamadı", "Meter Type: Veri bulunamadı", "Penalty: Veri bulunamadı", "Warning: Veri bulunamadı", "Versiyon: Bilinmiyor")
        messagebox.showinfo("Başarı", "Tüm işlemler durduruldu.")

    def on_file_modified(self, event):
        if event.src_path == self.file_path:
            self.process_data()

    def _process_data(self, decoded_data):
        try:
            # Voltaj hesabı
            byte_value = int(decoded_data[2:4], 16)
            voltage = byte_value / 1000
            voltage_str = f"Voltage: {voltage:.3f} V"

            # Kredi hesabı
            credit_hex = decoded_data[10:14]
            reversed_hex = credit_hex[2:] + credit_hex[:2]
            credit_value = int(reversed_hex, 16)
            scaled_credit = credit_value / 1000
            credit_str = f"Credit: {scaled_credit:.3f}"

            # Pil hesabı
            battery_hex = decoded_data[28:30]
            battery_value = int(battery_hex, 16)
            battery_status = battery_value / 10
            battery_str = f"Battery Status: {battery_status:.1f} V"

            # Connection Type 
            connection_type_value = int(decoded_data[26], 16)
            connection_types = {
                0: "first boot",
                1: "periodic",
                2: "reconnection",
                3: "manual connection",
                4: "valve couldn't open connection",
                5: "valve couldn't close",
                6: "hygienic valve couldn't close",
                7: "magnetic penalty",
                8: "cover penalty",
                9: "fitting penalty"
            }
            connection_type_str = f"Connection Type: {connection_types.get(connection_type_value, 'Unknown')}"

            # Meter Type 
            meter_type_value = int(decoded_data[27], 16)
            meter_types = {
                0: "AK-311 LoRa",
                1: "TK LoRa",
                2: "AMR LoRa",
                3: "AK411 LoRa",
                4: "ScanIF LoRa",
                5: "AMR Coil LoRa",
                6: "AK411 Heat LoRa",
                7: "AK411 LoRa No Valve",
                8: "AK411 Heat LoRa No Valve",
                9: "LoRa Valve"
            }
            meter_type_str = f"Meter Type: {meter_types.get(meter_type_value, 'Unknown')}"

            # Penalty 
            penalty_value = decoded_data[20]
            penalties = {
                '0': "Meter Cover opened",
                '1': "Fitting removed",
                '2': "Magnetic affected",
                '3': "Battery cover opened",
                '4': "Leakage penalty",
                '5': "Fire mode activated",
                '6': "Valve closed by consumer card",
                '7': "Meter disabled"
            }
            penalty_str = f"Penalty: {penalties.get(penalty_value, 'Unknown')}"

            # Warning bit 
            warning_bits_value = int(decoded_data[22:24], 16)
            warnings = {
                0: "Critical credit",
                1: "Valve malfunction",
                2: "Pulse malfunction",
                3: "Leakage warning",
                4: "Reverse flow",
                5: "Battery dead",
                6: "Overall consumption",
                7: "Maximum flow rate"
            }
            warning_str = f"Warning: {warnings.get(warning_bits_value, 'Unknown')}"

            # Versiyon 
            version_value = decoded_data[-2:]
            version_mapping = {
                '00': '0.0',
                '01': '0.1',
                '02': '0.2',
                '03': '0.3',
                '04': '0.4',
                '05': '0.5',
                '06': '0.6',
                '07': '0.7',
                '08': '0.8',
                '09': '0.9',
                '10': '1.0',
                '11': '1.1'
            }
            version_str = f"Version: {version_mapping.get(version_value, 'Bilinmiyor')}"

            # GUI güncellemeleri
            self._update_text_area(voltage_str, credit_str, battery_str, decoded_data, connection_type_str, meter_type_str, penalty_str, warning_str, version_str)
        except Exception as e:
            logging.error(f"Hata: {e}")
            self.queue.put((f"Hata: {e}", "Kredi bulunamadı", "Pil bulunamadı", "Decoded Data: Veri bulunamadı", "Connection Type: Veri bulunamadı", "Meter Type: Veri bulunamadı", "Penalty: Veri bulunamadı", "Warning: Veri bulunamadı", "Versiyon: Bilinmiyor"))

    def _update_text_area(self, voltage, credit, battery, decoded_data, connection_type, meter_type, penalty, warning, version):
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, f"{voltage}\n{credit}\n{battery}\n\n{connection_type}\n{meter_type}\n{penalty}\n{warning}\n{version}\n")
        self.decoded_data_textbox.delete('1.0', tk.END)
        self.decoded_data_textbox.insert(tk.END, f"Decoded Data: {decoded_data}\n")

    def check_queue(self):
        try:
            while True:
                item = self.queue.get_nowait()
                self._update_text_area(*item)
        except Empty:
            pass
        self.root.after(100, self.check_queue)

    def on_closing(self):
        self.stop_all_processes()
        self.observer.stop()
        self.observer.join()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = DataDisplayApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()