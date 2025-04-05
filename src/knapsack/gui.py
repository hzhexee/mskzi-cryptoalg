from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QTextEdit, QTableWidget, QTableWidgetItem,
                            QGroupBox, QTabWidget, QSplitter, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

import sys
import knapsack

class KnapsackGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Алгоритм шифрования рюкзака")
        self.setGeometry(100, 100, 1200, 800)
        
        # Данные для алгоритма
        self.private_key = None
        self.public_key = None
        self.n = None
        self.m = None
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
        
        # Группа для управления ключами
        keys_group = QGroupBox("Ключи шифрования")
        keys_layout = QVBoxLayout(keys_group)
        
        # Кнопка для генерации ключей
        generate_keys_btn = QPushButton("Сгенерировать ключи")
        generate_keys_btn.clicked.connect(self.generate_keys)
        keys_layout.addWidget(generate_keys_btn)
        
        # Отображение сгенерированных ключей
        key_details_layout = QHBoxLayout()
        
        # Закрытый ключ
        private_key_layout = QVBoxLayout()
        private_key_label = QLabel("Закрытый ключ:")
        private_key_layout.addWidget(private_key_label)
        self.private_key_display = QTextEdit()
        self.private_key_display.setReadOnly(True)
        private_key_layout.addWidget(self.private_key_display)
        key_details_layout.addLayout(private_key_layout)
        
        # Открытый ключ
        public_key_layout = QVBoxLayout()
        public_key_label = QLabel("Открытый ключ:")
        public_key_layout.addWidget(public_key_label)
        self.public_key_display = QTextEdit()
        self.public_key_display.setReadOnly(True)
        public_key_layout.addWidget(self.public_key_display)
        key_details_layout.addLayout(public_key_layout)
        
        # Параметры n и m
        params_layout = QVBoxLayout()
        params_label = QLabel("Параметры:")
        params_layout.addWidget(params_label)
        
        n_layout = QHBoxLayout()
        n_layout.addWidget(QLabel("n: "))
        self.n_display = QLineEdit()
        self.n_display.setReadOnly(True)
        n_layout.addWidget(self.n_display)
        params_layout.addLayout(n_layout)
        
        m_layout = QHBoxLayout()
        m_layout.addWidget(QLabel("m: "))
        self.m_display = QLineEdit()
        self.m_display.setReadOnly(True)
        m_layout.addWidget(self.m_display)
        params_layout.addLayout(m_layout)
        
        key_details_layout.addLayout(params_layout)
        
        keys_layout.addLayout(key_details_layout)
        layout.addWidget(keys_group)
        
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
        encrypted_label = QLabel("Зашифрованное сообщение:")
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
        
        # Создаем вкладки для визуализации шифрования и дешифрования
        vis_tabs = QTabWidget()
        layout.addWidget(vis_tabs)
        
        # Вкладка визуализации шифрования
        encrypt_vis_tab = QWidget()
        vis_tabs.addTab(encrypt_vis_tab, "Процесс шифрования")
        encrypt_vis_layout = QVBoxLayout(encrypt_vis_tab)
        
        # Заголовок и описание для визуализации шифрования
        encrypt_vis_label = QLabel("Визуализация процесса шифрования")
        encrypt_vis_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        encrypt_vis_layout.addWidget(encrypt_vis_label)
        
        encrypt_vis_desc = QLabel("Здесь показан пошаговый процесс шифрования каждого символа сообщения.")
        encrypt_vis_layout.addWidget(encrypt_vis_desc)
        
        # Таблица для отображения процесса шифрования
        self.encryption_table = QTableWidget(0, 6)
        self.encryption_table.setHorizontalHeaderLabels([
            "Символ", "ASCII", "Биты", "Использованные ключи", "Сумма", "Результат"
        ])
        encrypt_vis_layout.addWidget(self.encryption_table)
        
        # Вкладка визуализации дешифрования
        decrypt_vis_tab = QWidget()
        vis_tabs.addTab(decrypt_vis_tab, "Процесс дешифрования")
        decrypt_vis_layout = QVBoxLayout(decrypt_vis_tab)
        
        # Заголовок и описание для визуализации дешифрования
        decrypt_vis_label = QLabel("Визуализация процесса дешифрования")
        decrypt_vis_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        decrypt_vis_layout.addWidget(decrypt_vis_label)
        
        decrypt_vis_desc = QLabel("Здесь показан пошаговый процесс дешифрования каждого зашифрованного значения.")
        decrypt_vis_layout.addWidget(decrypt_vis_desc)
        
        # Таблица для отображения процесса дешифрования
        self.decryption_table = QTableWidget(0, 7)
        self.decryption_table.setHorizontalHeaderLabels([
            "Зашифр. значение", "n⁻¹", "m", "s'", "Биты", "Использованные ключи", "Символ"
        ])
        decrypt_vis_layout.addWidget(self.decryption_table)
    
    def setup_about_tab(self):
        layout = QVBoxLayout(self.about_tab)
        
        title_label = QLabel("Алгоритм шифрования рюкзака")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        description = QTextEdit()
        description.setReadOnly(True)
        description.setHtml("""
            <h2>Описание алгоритма</h2>
            <p>Алгоритм шифрования рюкзака - асимметричный криптографический алгоритм, основанный на задаче об укладке рюкзака (NP-полная задача).</p>
            <h3>Основные компоненты:</h3>
            <ol>
                <li><b>Закрытый ключ</b> - суперрастущая последовательность чисел, где каждое число больше суммы всех предыдущих.</li>
                <li><b>Открытый ключ</b> - трансформированная последовательность, полученная с помощью параметров n и m.</li>
                <li><b>Параметры n и m</b> - целые числа, где m больше суммы всех элементов закрытого ключа, а n взаимно просто с m.</li>
            </ol>
            <h3>Процесс шифрования:</h3>
            <p>1. Каждый символ сообщения преобразуется в 8-битное представление.</p>
            <p>2. Для каждого бита, если он равен 1, добавляется соответствующий элемент открытого ключа.</p>
            <p>3. Сумма этих значений является зашифрованным значением символа.</p>
            <h3>Процесс дешифрования:</h3>
            <p>1. Зашифрованное значение преобразуется в домен закрытого ключа с помощью обратного элемента n по модулю m.</p>
            <p>2. С использованием жадного алгоритма и суперрастущего свойства закрытого ключа восстанавливаются биты.</p>
            <p>3. Биты преобразуются обратно в символ.</p>
        """)
        layout.addWidget(description)
        
        credits_label = QLabel("© 2023 MSKZI Cryptography Project")
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(credits_label)
    
    def generate_keys(self):
        try:
            self.private_key, self.public_key, self.n, self.m = knapsack.generate_keys()
            
            # Отображаем ключи и параметры
            self.private_key_display.setText(str(self.private_key))
            self.public_key_display.setText(str(self.public_key))
            self.n_display.setText(str(self.n))
            self.m_display.setText(str(self.m))
            
            # Очищаем предыдущие результаты
            self.encrypted_display.clear()
            self.decrypted_display.clear()
            self.encryption_table.setRowCount(0)
            self.decryption_table.setRowCount(0)
        except Exception as e:
            self.show_error(f"Ошибка при генерации ключей: {str(e)}")
    
    def encrypt_message(self):
        if self.public_key is None:
            self.show_error("Сначала необходимо сгенерировать ключи!")
            return
        
        message = self.message_input.toPlainText()
        if not message:
            self.show_error("Введите сообщение для шифрования!")
            return
        
        try:
            self.encrypted_data, self.encryption_details = knapsack.encrypt_message(message, self.public_key)
            
            # Отображаем зашифрованное сообщение
            self.encrypted_display.setText(str(self.encrypted_data))
            
            # Очищаем поле с дешифрованным сообщением
            self.decrypted_display.clear()
            
            # Обновляем таблицу визуализации шифрования
            self.update_encryption_visualization()
            
            # Переключаемся на вкладку визуализации
            self.tabs.setCurrentIndex(1)
        except Exception as e:
            self.show_error(f"Ошибка при шифровании: {str(e)}")
    
    def decrypt_message(self):
        if self.encrypted_data is None:
            self.show_error("Сначала необходимо зашифровать сообщение!")
            return
        
        if self.private_key is None or self.n is None or self.m is None:
            self.show_error("Ключи шифрования отсутствуют!")
            return
        
        try:
            decrypted_message, self.decryption_details = knapsack.decrypt_message(
                self.encrypted_data, self.private_key, self.n, self.m
            )
            
            # Отображаем дешифрованное сообщение
            self.decrypted_display.setText(decrypted_message)
            
            # Обновляем таблицу визуализации дешифрования
            self.update_decryption_visualization()
            
            # Переключаемся на вкладку визуализации
            self.tabs.setCurrentIndex(1)
        except Exception as e:
            self.show_error(f"Ошибка при дешифровании: {str(e)}")
    
    def update_encryption_visualization(self):
        if not self.encryption_details:
            return
        
        # Очищаем таблицу
        self.encryption_table.setRowCount(0)
        
        # Заполняем таблицу данными о шифровании
        for idx, details in enumerate(self.encryption_details):
            row_position = self.encryption_table.rowCount()
            self.encryption_table.insertRow(row_position)
            
            # Символ
            self.encryption_table.setItem(row_position, 0, QTableWidgetItem(details['char']))
            
            # ASCII-код
            self.encryption_table.setItem(row_position, 1, QTableWidgetItem(str(details['ascii'])))
            
            # Биты
            bits_item = QTableWidgetItem(details['bits'])
            bits_item.setFont(QFont("Courier New", 10))
            self.encryption_table.setItem(row_position, 2, bits_item)
            
            # Использованные ключи
            used_keys_str = "\n".join([f"Бит {k}: {v}" for k, v in details['used_keys']])
            self.encryption_table.setItem(row_position, 3, QTableWidgetItem(used_keys_str))
            
            # Сумма
            self.encryption_table.setItem(row_position, 4, QTableWidgetItem(str(details['sum'])))
            
            # Результат
            result_item = QTableWidgetItem(str(details['result']))
            result_item.setBackground(QColor(200, 255, 200))  # Выделяем результат зеленым цветом
            self.encryption_table.setItem(row_position, 5, result_item)
        
        # Устанавливаем размер ячеек по содержимому
        self.encryption_table.resizeColumnsToContents()
        self.encryption_table.resizeRowsToContents()
    
    def update_decryption_visualization(self):
        if not self.decryption_details:
            return
        
        # Очищаем таблицу
        self.decryption_table.setRowCount(0)
        
        # Заполняем таблицу данными о дешифровании
        for idx, details in enumerate(self.decryption_details):
            row_position = self.decryption_table.rowCount()
            self.decryption_table.insertRow(row_position)
            
            # Зашифрованное значение
            self.decryption_table.setItem(row_position, 0, QTableWidgetItem(str(details['encrypted_value'])))
            
            # n⁻¹
            self.decryption_table.setItem(row_position, 1, QTableWidgetItem(str(details['n_inverse'])))
            
            # m
            self.decryption_table.setItem(row_position, 2, QTableWidgetItem(str(details['m'])))
            
            # s'
            self.decryption_table.setItem(row_position, 3, QTableWidgetItem(str(details['s_prime'])))
            
            # Биты
            bits_item = QTableWidgetItem(details['bits'])
            bits_item.setFont(QFont("Courier New", 10))
            self.decryption_table.setItem(row_position, 4, bits_item)
            
            # Использованные ключи
            used_keys_str = "\n".join([f"Бит {k}: {v}" for k, v in details['used_private_keys']])
            self.decryption_table.setItem(row_position, 5, QTableWidgetItem(used_keys_str))
            
            # Символ
            char_item = QTableWidgetItem(details['char'])
            char_item.setBackground(QColor(200, 255, 200))  # Выделяем результат зеленым цветом
            self.decryption_table.setItem(row_position, 6, char_item)
        
        # Устанавливаем размер ячеек по содержимому
        self.decryption_table.resizeColumnsToContents()
        self.decryption_table.resizeRowsToContents()
    
    def show_error(self, message):
        # В реальном приложении здесь можно использовать QMessageBox
        print(f"Ошибка: {message}")

def main():
    app = QApplication(sys.argv)
    window = KnapsackGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
