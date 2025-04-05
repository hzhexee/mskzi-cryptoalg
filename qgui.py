import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import random
from quantum import QuantumBB84

class QuantumBB84GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Квантовое распределение ключей BB84")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Создаем экземпляр симулятора
        self.simulator = QuantumBB84(length=10)
        
        # Инициализация интерфейса
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка элементов интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель с настройками и кнопками
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding=10)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Настройка длины последовательности
        length_frame = ttk.Frame(control_frame)
        length_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(length_frame, text="Длина последовательности:").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=10)
        self.length_spinbox = ttk.Spinbox(length_frame, from_=5, to=30, width=5, textvariable=self.length_var)
        self.length_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Переключатель режима (с подслушиванием или без)
        self.eavesdropping_var = tk.BooleanVar(value=False)
        self.eavesdropping_check = ttk.Checkbutton(
            control_frame, 
            text="С подслушиванием (Ева)", 
            variable=self.eavesdropping_var
        )
        self.eavesdropping_check.pack(side=tk.LEFT, padx=20)
        
        # Кнопка запуска симуляции
        self.run_button = ttk.Button(
            control_frame, 
            text="Запустить симуляцию", 
            command=self.run_simulation
        )
        self.run_button.pack(side=tk.RIGHT, padx=10)
        
        # Фрейм для визуализации
        viz_frame = ttk.LabelFrame(main_frame, text="Визуализация протокола", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas для анимации
        self.canvas = tk.Canvas(viz_frame, bg="white", height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Полоса прогресса для анимации
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress = ttk.Progressbar(
            viz_frame, 
            orient="horizontal", 
            length=100, 
            mode="determinate", 
            variable=self.progress_var
        )
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
        # Панель с логами и результатами
        log_frame = ttk.LabelFrame(main_frame, text="Результаты", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Текстовое поле для логов
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Нижняя панель статуса
        self.status_var = tk.StringVar(value="Готов к запуску симуляции")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        # Начальная инициализация визуализации
        self.setup_visualization()
    
    def setup_visualization(self):
        """Инициализация элементов визуализации на холсте"""
        self.canvas.delete("all")
        
        # Фиксированные позиции участников протокола
        self.alice_x, self.alice_y = 150, 150
        self.bob_x, self.bob_y = 750, 150
        self.eve_x, self.eve_y = 450, 300  # Ева будет посередине ниже
        
        # Рисуем участников
        self.draw_participant("Алиса", self.alice_x, self.alice_y, "skyblue")
        self.draw_participant("Боб", self.bob_x, self.bob_y, "lightgreen")
        
        # Рисуем линию для квантового канала
        self.quantum_channel = self.canvas.create_line(
            self.alice_x + 50, self.alice_y, 
            self.bob_x - 50, self.bob_y,
            width=3, dash=(5, 5), fill="black", tags="channel"
        )
        
        # Текст для отображения текущего шага
        self.step_text = self.canvas.create_text(
            450, 50, text="Готов к запуску", 
            font=("Arial", 12, "bold"), fill="black"
        )
    
    def draw_participant(self, name, x, y, color):
        """Рисует участника протокола на холсте"""
        # Рисуем иконку участника (круг)
        self.canvas.create_oval(x-40, y-40, x+40, y+40, fill=color, outline="black", width=2)
        # Добавляем имя
        self.canvas.create_text(x, y, text=name, font=("Arial", 12, "bold"))
        return (x, y)
    
    def log(self, message):
        """Добавляет сообщение в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def update_status(self, message):
        """Обновляет строку статуса"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run_simulation(self):
        """Запускает симуляцию в отдельном потоке"""
        # Блокируем кнопку на время симуляции
        self.run_button.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)  # Очищаем лог
        
        # Обновляем длину последовательности
        self.simulator.length = self.length_var.get()
        
        # Запускаем симуляцию в отдельном потоке
        threading.Thread(target=self._run_simulation_thread, daemon=True).start()
    
    def _run_simulation_thread(self):
        """Основной поток симуляции"""
        try:
            with_eavesdropping = self.eavesdropping_var.get()
            
            # Шаг 1: Инициализация визуализации
            self.root.after(0, self.setup_visualization)
            self.root.after(0, self.update_status, "Запуск симуляции...")
            self.root.after(0, lambda: self.progress_var.set(0))
            
            # Если выбран режим с подслушиванием, добавляем Еву
            if with_eavesdropping:
                self.root.after(500, lambda: self.draw_participant("Ева", self.eve_x, self.eve_y, "pink"))
                self.root.after(500, lambda: self.canvas.create_line(
                    self.alice_x + 40, self.alice_y + 20, 
                    self.eve_x - 20, self.eve_y - 20,
                    width=2, dash=(5, 5), fill="red", tags="eve_channel_in"
                ))
                self.root.after(500, lambda: self.canvas.create_line(
                    self.eve_x + 20, self.eve_y - 20, 
                    self.bob_x - 40, self.bob_y + 20,
                    width=2, dash=(5, 5), fill="red", tags="eve_channel_out"
                ))
            
            # Шаг 2: Алиса генерирует биты и базисы
            time.sleep(0.5)
            self.root.after(0, lambda: self.canvas.itemconfig(self.step_text, text="Алиса генерирует случайные биты и базисы"))
            self.root.after(0, self.update_status, "Алиса генерирует данные...")
            self.root.after(0, lambda: self.progress_var.set(10))
            
            alice_bits, alice_bases, quantum_states = self.simulator.prepare_alice_data()
            
            self.root.after(0, self.log, f"Биты Алисы: {alice_bits}")
            self.root.after(0, self.log, f"Базисы Алисы: {alice_bases}")
            self.root.after(0, self.log, f"Квантовые состояния: {quantum_states}")
            
            # Шаг 3: Визуализация отправки квантовых состояний от Алисы
            time.sleep(1)
            self.root.after(0, lambda: self.canvas.itemconfig(self.step_text, text="Алиса отправляет квантовые состояния"))
            self.root.after(0, self.update_status, "Отправка квантовых состояний...")
            self.root.after(0, lambda: self.progress_var.set(30))
            
            # Анимация отправки фотонов
            for i, state in enumerate(quantum_states):
                if i >= 5:  # Визуализируем только первые 5 фотонов
                    break
                    
                idx = i  # Для замыканий
                
                def animate_photon(idx, target_x, target_y, color="blue"):
                    photon = self.canvas.create_oval(
                        self.alice_x + 30, self.alice_y - 5, 
                        self.alice_x + 40, self.alice_y + 5, 
                        fill=color, outline=color
                    )
                    
                    # Анимируем движение
                    dx = (target_x - (self.alice_x + 35)) / 20
                    dy = (target_y - self.alice_y) / 20
                    
                    def move_photon(photon, step=0):
                        if step < 20:
                            self.canvas.move(photon, dx, dy)
                            self.root.after(50, lambda: move_photon(photon, step+1))
                        else:
                            self.canvas.delete(photon)
                    
                    move_photon(photon)
                
                # Определяем, куда отправлять фотон (к Еве или сразу к Бобу)
                target_x = self.eve_x if with_eavesdropping else self.bob_x - 35
                target_y = self.eve_y if with_eavesdropping else self.bob_y
                
                self.root.after(i*300, lambda i=idx, tx=target_x, ty=target_y: 
                               animate_photon(i, tx, ty, "blue"))
                
            time.sleep(1.5)
            
            # Шаг 4: Ева перехватывает фотоны (если включен режим с подслушиванием)
            if with_eavesdropping:
                self.root.after(0, lambda: self.canvas.itemconfig(self.step_text, text="Ева перехватывает и измеряет квантовые состояния"))
                self.root.after(0, self.update_status, "Ева перехватывает данные...")
                self.root.after(0, lambda: self.progress_var.set(50))
                
                eve_bases, eve_bits, modified_states = self.simulator.prepare_eve_data()
                
                self.root.after(0, self.log, f"Базисы Евы: {eve_bases}")
                self.root.after(0, self.log, f"Биты, полученные Евой: {eve_bits}")
                self.root.after(0, self.log, f"Модифицированные состояния: {modified_states}")
                
                # Анимация перенаправления фотонов от Евы к Бобу
                for i in range(min(5, len(modified_states))):
                    idx = i
                    self.root.after(i*300, lambda i=idx: 
                                   animate_photon(i, self.bob_x - 35, self.bob_y, "red"))
                
                time.sleep(1.5)
            
            # Шаг 5: Боб получает и измеряет фотоны
            self.root.after(0, lambda: self.canvas.itemconfig(self.step_text, text="Боб выбирает базисы и измеряет состояния"))
            self.root.after(0, self.update_status, "Боб измеряет квантовые состояния...")
            self.root.after(0, lambda: self.progress_var.set(70))
            
            bob_bases, bob_measured_bits = self.simulator.prepare_bob_data()
            
            self.root.after(0, self.log, f"Базисы Боба: {bob_bases}")
            self.root.after(0, self.log, f"Измеренные биты Боба: {bob_measured_bits}")
            
            time.sleep(1)
            
            # Шаг 6: Алиса и Боб сравнивают базисы
            self.root.after(0, lambda: self.canvas.itemconfig(self.step_text, text="Алиса и Боб сравнивают базисы"))
            self.root.after(0, self.update_status, "Сравнение базисов и просеивание ключа...")
            self.root.after(0, lambda: self.progress_var.set(90))
            
            sifted_key_alice, sifted_key_bob, error_rate = self.simulator.sift_keys()
            
            self.root.after(0, self.log, f"Совпавшие базисы на позициях: {self.simulator.matching_indices}")
            self.root.after(0, self.log, f"Просеянный ключ Алисы: {sifted_key_alice}")
            self.root.after(0, self.log, f"Просеянный ключ Боба: {sifted_key_bob}")
            self.root.after(0, self.log, f"Частота ошибок: {error_rate:.2%}")
            
            # Шаг 7: Финальный результат
            time.sleep(1)
            self.root.after(0, lambda: self.canvas.itemconfig(self.step_text, text=f"Симуляция завершена. Частота ошибок: {error_rate:.2%}"))
            self.root.after(0, lambda: self.progress_var.set(100))
            
            if with_eavesdropping:
                if error_rate > 0:
                    message = f"Подслушивание обнаружено! Частота ошибок {error_rate:.2%}"
                    self.root.after(0, self.log, message)
                    self.root.after(0, self.update_status, message)
                else:
                    message = "Странно! Ошибки не обнаружены, несмотря на подслушивание."
                    self.root.after(0, self.log, message)
                    self.root.after(0, self.update_status, message)
            else:
                if error_rate > 0:
                    message = "Предупреждение: Обнаружены ошибки, хотя подслушивания не было!"
                    self.root.after(0, self.log, message)
                    self.root.after(0, self.update_status, message)
                else:
                    message = "Успех! Ключ согласован без ошибок."
                    self.root.after(0, self.log, message)
                    self.root.after(0, self.update_status, message)
                    
            # Разблокируем кнопку
            self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}"))
            self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))

def main():
    root = tk.Tk()
    app = QuantumBB84GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
