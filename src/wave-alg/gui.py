from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QTextEdit, QTableWidget, QTableWidgetItem,
                            QGroupBox, QTabWidget, QSplitter, QLineEdit, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
import sys
import wave

class WaveGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Алгоритм волнового шифрования")
        self.setGeometry(100, 100, 1200, 800)
        
        # Данные для алгоритма
        self.z = 0.5
        self.dx = 0.5
        self.encrypted_data = None
        self.encryption_details = None
        self.decryption_details = None
        
        # Создаем центральный виджет и основной макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем вкладки для различных функций
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Вкладка шифрования
        self.encryption_tab = QWidget()
        self.tabs.addTab(self.encryption_tab, "Шифрование")
        self.setup_encryption_tab()
        
        # Вкладка визуализации
        self.visualization_tab = QWidget()
        self.tabs.addTab(self.visualization_tab, "Визуализация")
        self.setup_visualization_tab()
        
        # Вкладка о программе
        self.about_tab = QWidget()
        self.tabs.addTab(self.about_tab, "О программе")
        self.setup_about_tab()
    
    def setup_encryption_tab(self):
        layout = QVBoxLayout(self.encryption_tab)
        
        # Группа для ввода исходного сообщения
        input_group = QGroupBox("Исходное сообщение")
        input_layout = QVBoxLayout(input_group)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Введите сообщение для шифрования...")
        input_layout.addWidget(self.message_input)
        
        layout.addWidget(input_group)
        
        # Группа для параметров алгоритма
        params_group = QGroupBox("Параметры алгоритма")
        params_layout = QVBoxLayout(params_group)
        
        # Ввод параметра z
        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Начальная фаза волны (z):"))
        self.z_input = QDoubleSpinBox()
        self.z_input.setRange(-500, 500)
        self.z_input.setValue(0.5)
        self.z_input.setSingleStep(0.1)
        self.z_input.valueChanged.connect(self.update_params)
        z_layout.addWidget(self.z_input)
        params_layout.addLayout(z_layout)
        
        # Ввод параметра dx
        dx_layout = QHBoxLayout()
        dx_layout.addWidget(QLabel("Шаг изменения фазы (dx):"))
        self.dx_input = QDoubleSpinBox()
        self.dx_input.setRange(-500, 500)
        self.dx_input.setValue(0.5)
        self.dx_input.setSingleStep(0.1)
        self.dx_input.valueChanged.connect(self.update_params)
        dx_layout.addWidget(self.dx_input)
        params_layout.addLayout(dx_layout)
        
        params_layout.addStretch(1)
        
        # Кнопка для генерации случайных параметров
        generate_params_btn = QPushButton("Сгенерировать случайные параметры")
        generate_params_btn.clicked.connect(self.generate_random_params)
        params_layout.addWidget(generate_params_btn)
        
        layout.addWidget(params_group)
        
        # Группа для результатов шифрования и дешифрования
        results_group = QGroupBox("Результаты")
        results_layout = QVBoxLayout(results_group)
        
        buttons_layout = QHBoxLayout()
        
        # Кнопка для шифрования
        encrypt_btn = QPushButton("Зашифровать")
        encrypt_btn.clicked.connect(self.encrypt_message)
        buttons_layout.addWidget(encrypt_btn)
        
        # Кнопка для дешифрования
        decrypt_btn = QPushButton("Дешифровать")
        decrypt_btn.clicked.connect(self.decrypt_message)
        buttons_layout.addWidget(decrypt_btn)
        
        results_layout.addLayout(buttons_layout)
        
        # Поле для вывода зашифрованного сообщения
        encrypted_layout = QVBoxLayout()
        encrypted_label = QLabel("Зашифрованное сообщение (hex):")
        encrypted_layout.addWidget(encrypted_label)
        self.encrypted_display = QTextEdit()
        self.encrypted_display.setReadOnly(True)
        encrypted_layout.addWidget(self.encrypted_display)
        results_layout.addLayout(encrypted_layout)
        
        # Поле для вывода дешифрованного сообщения
        decrypted_layout = QVBoxLayout()
        decrypted_label = QLabel("Дешифрованное сообщение:")
        decrypted_layout.addWidget(decrypted_label)
        self.decrypted_display = QTextEdit()
        self.decrypted_display.setReadOnly(True)
        decrypted_layout.addWidget(self.decrypted_display)
        results_layout.addLayout(decrypted_layout)
        
        layout.addWidget(results_group)
    
    def setup_visualization_tab(self):
        layout = QVBoxLayout(self.visualization_tab)
        
        # Создаем вкладки для различных визуализаций
        vis_tabs = QTabWidget()
        layout.addWidget(vis_tabs)
        
        # Вкладка для графика волновой функции
        wave_plot_tab = QWidget()
        vis_tabs.addTab(wave_plot_tab, "График волновой функции")
        wave_plot_layout = QVBoxLayout(wave_plot_tab)
        
        # Создаем холст для графика
        self.wave_figure = plt.figure(figsize=(10, 6))
        self.wave_canvas = FigureCanvas(self.wave_figure)
        wave_plot_layout.addWidget(self.wave_canvas)
        
        # Кнопка обновления графика
        update_wave_btn = QPushButton("Обновить график")
        update_wave_btn.clicked.connect(self.update_wave_plot)
        wave_plot_layout.addWidget(update_wave_btn)
        
        # Вкладка визуализации процесса шифрования
        encrypt_vis_tab = QWidget()
        vis_tabs.addTab(encrypt_vis_tab, "Процесс шифрования")
        encrypt_vis_layout = QVBoxLayout(encrypt_vis_tab)
        
        # Заголовок для визуализации шифрования
        encrypt_vis_label = QLabel("Визуализация процесса шифрования")
        encrypt_vis_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        encrypt_vis_layout.addWidget(encrypt_vis_label)
        
        encrypt_vis_desc = QLabel("Здесь показан пошаговый процесс шифрования каждого символа сообщения.")
        encrypt_vis_layout.addWidget(encrypt_vis_desc)
        
        # Таблица для отображения процесса шифрования
        self.encryption_table = QTableWidget(0, 6)
        self.encryption_table.setHorizontalHeaderLabels([
            "Символ", "ASCII", "Значение волны", "Вычисление", "Результат", "Hex"
        ])
        encrypt_vis_layout.addWidget(self.encryption_table)
        
        # Вкладка визуализации процесса дешифрования
        decrypt_vis_tab = QWidget()
        vis_tabs.addTab(decrypt_vis_tab, "Процесс дешифрования")
        decrypt_vis_layout = QVBoxLayout(decrypt_vis_tab)
        
        # Заголовок для визуализации дешифрования
        decrypt_vis_label = QLabel("Визуализация процесса дешифрования")
        decrypt_vis_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        decrypt_vis_layout.addWidget(decrypt_vis_label)
        
        decrypt_vis_desc = QLabel("Здесь показан пошаговый процесс дешифрования каждого зашифрованного значения.")
        decrypt_vis_layout.addWidget(decrypt_vis_desc)
        
        # Таблица для отображения процесса дешифрования
        self.decryption_table = QTableWidget(0, 6)
        self.decryption_table.setHorizontalHeaderLabels([
            "Hex", "ASCII", "Значение волны", "Вычисление", "Результат", "Символ"
        ])
        decrypt_vis_layout.addWidget(self.decryption_table)
        
        # Инициализация графика волны
        self.update_wave_plot()
    
    def setup_about_tab(self):
        layout = QVBoxLayout(self.about_tab)
        
        title_label = QLabel("Алгоритм волнового шифрования")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        description = QTextEdit()
        description.setReadOnly(True)
        description.setHtml("""
        <h2>Описание алгоритма</h2>
        <p>Волновой алгоритм шифрования (Wave Cipher) использует тригонометрические функции для создания "волны", 
        которая накладывается на ASCII-коды символов исходного сообщения.</p>
        
        <h3>Принцип работы:</h3>
        <ol>
            <li>Для каждого символа вычисляется модификация его ASCII-кода с использованием функции косинуса</li>
            <li>Параметры шифрования:
                <ul>
                    <li><b>z</b> - начальная фаза волны</li>
                    <li><b>dx</b> - шаг изменения фазы от символа к символу</li>
                </ul>
            </li>
            <li>Формула шифрования: <code>результат = ASCII-код + 255 * cos(z + n * dx)</code></li>
            <li>Результат нормализуется и преобразуется в шестнадцатеричный формат</li>
        </ol>
        
        <h3>Особенности:</h3>
        <ul>
            <li>Простая реализация и быстродействие</li>
            <li>Возможность настройки параметров для изменения силы шифрования</li>
            <li>Визуальная наглядность процесса с помощью графика волновой функции</li>
        </ul>
        """)
        layout.addWidget(description)
    
    def update_params(self):
        """Обновляет параметры алгоритма при изменении значений в полях ввода"""
        self.z = self.z_input.value()
        self.dx = self.dx_input.value()
        self.update_wave_plot()
    
    def generate_random_params(self):
        """Генерирует случайные параметры для алгоритма"""
        import random
        z = random.uniform(-10, 10)
        dx = random.uniform(-10, 10)
        
        self.z_input.setValue(z)
        self.dx_input.setValue(dx)
        self.update_params()
    
    def update_wave_plot(self):
        """Обновляет график волновой функции"""
        # Очищаем текущий график
        self.wave_figure.clear()
        ax = self.wave_figure.add_subplot(111)
        
        # Создаем данные для графика
        x = np.linspace(0, 10, 1000)
        wave_values = [255 * math.cos(self.z + i * self.dx) for i in range(len(x))]
        
        # Строим график волновой функции
        ax.plot(x, wave_values, 'b-', linewidth=2)
        ax.set_title('Волновая функция с параметрами z={:.2f}, dx={:.2f}'.format(self.z, self.dx))
        ax.set_xlabel('Позиция символа')
        ax.set_ylabel('Значение волновой функции')
        ax.grid(True)
        
        # Добавляем горизонтальные линии для визуального ориентира
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axhline(y=255, color='r', linestyle='--', alpha=0.5)
        ax.axhline(y=-255, color='r', linestyle='--', alpha=0.5)
        
        # Обновляем холст
        self.wave_canvas.draw()
    
    def encrypt_message(self):
        """Шифрует введенное сообщение и отображает результат"""
        message = self.message_input.toPlainText()
        if not message:
            return
        
        # Сохраняем детали шифрования для визуализации
        self.encryption_details = []
        
        # Шифруем сообщение
        encrypted = wave.encrypt(message, self.z, self.dx)
        self.encrypted_data = encrypted
        self.encrypted_display.setText(encrypted)
        
        # Заполняем таблицу визуализации процесса шифрования
        self.encryption_table.setRowCount(len(message))
        
        for idx, char in enumerate(message):
            ascii_val = ord(char)
            wave_val = 255 * math.cos(self.z + idx * self.dx)
            new_val = ascii_val + wave_val
            
            # Нормализуем результат
            if new_val < 0:
                new_val += 255
            elif new_val > 255:
                new_val -= 255
            
            new_val = math.ceil(new_val)
            hex_val = format(new_val, '02x')
            
            # Записываем данные для визуализации
            self.encryption_details.append({
                'char': char,
                'ascii': ascii_val,
                'wave_val': wave_val,
                'new_val': new_val,
                'hex': hex_val
            })
            
            # Заполняем строку в таблице
            self.encryption_table.setItem(idx, 0, QTableWidgetItem(char))
            self.encryption_table.setItem(idx, 1, QTableWidgetItem(str(ascii_val)))
            self.encryption_table.setItem(idx, 2, QTableWidgetItem(f"{wave_val:.2f}"))
            self.encryption_table.setItem(idx, 3, QTableWidgetItem(f"{ascii_val} + {wave_val:.2f}"))
            self.encryption_table.setItem(idx, 4, QTableWidgetItem(str(new_val)))
            self.encryption_table.setItem(idx, 5, QTableWidgetItem(hex_val))
        
        # Переключаемся на вкладку визуализации
        self.tabs.setCurrentIndex(1)
    
    def decrypt_message(self):
        """Дешифрует сообщение и отображает результат"""
        encrypted = self.encrypted_display.toPlainText()
        if not encrypted:
            return
        
        # Дешифруем сообщение
        decrypted = wave.decrypt(encrypted, self.z, self.dx)
        self.decrypted_display.setText(decrypted)
        
        # Сохраняем детали дешифрования для визуализации
        self.decryption_details = []
        
        # Заполняем таблицу визуализации процесса дешифрования
        temp = wave.hex_to_vec(encrypted)
        self.decryption_table.setRowCount(len(temp))
        
        for idx, num in enumerate(temp):
            hex_val = format(num, '02x')
            wave_val = 255 * math.cos(self.z + idx * self.dx)
            new_val = num - wave_val
            
            # Нормализуем результат
            if new_val < 0:
                new_val += 255
            elif new_val > 255:
                new_val -= 255
                
            new_val = math.floor(new_val)
            char = chr(new_val)
            
            # Записываем данные для визуализации
            self.decryption_details.append({
                'hex': hex_val,
                'ascii': num,
                'wave_val': wave_val,
                'new_val': new_val,
                'char': char
            })
            
            # Заполняем строку в таблице
            self.decryption_table.setItem(idx, 0, QTableWidgetItem(hex_val))
            self.decryption_table.setItem(idx, 1, QTableWidgetItem(str(num)))
            self.decryption_table.setItem(idx, 2, QTableWidgetItem(f"{wave_val:.2f}"))
            self.decryption_table.setItem(idx, 3, QTableWidgetItem(f"{num} - {wave_val:.2f}"))
            self.decryption_table.setItem(idx, 4, QTableWidgetItem(str(new_val)))
            self.decryption_table.setItem(idx, 5, QTableWidgetItem(char))
        
        # Переключаемся на вкладку визуализации
        self.tabs.setCurrentIndex(1)

def main():
    app = QApplication(sys.argv)
    window = WaveGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
