import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QSpinBox, QCheckBox, QGroupBox, 
                            QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush
import random
from quantum import QuantumBB84

class QuantumStateWidget(QWidget):
    """Виджет для отображения квантового состояния"""
    def __init__(self, state=None, size=40, parent=None):
        super().__init__(parent)
        self.state = state
        self.size = size
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
    
    def setState(self, state):
        """Устанавливает квантовое состояние для отображения"""
        self.state = state
        self.update()
    
    def paintEvent(self, event):
        if not self.state:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Настройка кистей и перьев
        painter.setPen(QPen(QColor("#333333"), 2))
        
        # Определяем цвет заполнения в зависимости от состояния
        if self.state == "|0⟩":
            painter.setBrush(QBrush(QColor("#88c0d0")))  # Синий для |0⟩
            self.drawVerticalArrow(painter)
        elif self.state == "|1⟩":
            painter.setBrush(QBrush(QColor("#b48ead")))  # Фиолетовый для |1⟩
            self.drawHorizontalArrow(painter)
        elif self.state == "|+⟩":
            painter.setBrush(QBrush(QColor("#a3be8c")))  # Зеленый для |+⟩
            self.drawDiagonalArrowRight(painter)
        elif self.state == "|-⟩":
            painter.setBrush(QBrush(QColor("#ebcb8b")))  # Желтый для |-⟩
            self.drawDiagonalArrowLeft(painter)
    
    def drawVerticalArrow(self, painter):
        """Рисует вертикальную стрелку для состояния |0⟩"""
        width = self.size
        height = self.size
        
        # Рисуем стрелку, указывающую вверх
        painter.drawLine(width // 2, height - 5, width // 2, 5)
        painter.drawLine(width // 2, 5, width // 2 - 5, 15)
        painter.drawLine(width // 2, 5, width // 2 + 5, 15)
    
    def drawHorizontalArrow(self, painter):
        """Рисует горизонтальную стрелку для состояния |1⟩"""
        width = self.size
        height = self.size
        
        # Рисуем стрелку, указывающую вправо
        painter.drawLine(5, height // 2, width - 5, height // 2)
        painter.drawLine(width - 5, height // 2, width - 15, height // 2 - 5)
        painter.drawLine(width - 5, height // 2, width - 15, height // 2 + 5)
    
    def drawDiagonalArrowRight(self, painter):
        """Рисует диагональную стрелку (↗) для состояния |+⟩"""
        width = self.size
        height = self.size
        
        # Рисуем диагональную стрелку из левого нижнего в правый верхний угол
        painter.drawLine(5, height - 5, width - 5, 5)
        painter.drawLine(width - 5, 5, width - 15, 5 + 5)
        painter.drawLine(width - 5, 5, width - 5 - 5, 15)
    
    def drawDiagonalArrowLeft(self, painter):
        """Рисует диагональную стрелку (↘) для состояния |-⟩"""
        width = self.size
        height = self.size
        
        # Рисуем диагональную стрелку из левого верхнего в правый нижний угол
        painter.drawLine(5, 5, width - 5, height - 5)
        painter.drawLine(width - 5, height - 5, width - 15, height - 10)
        painter.drawLine(width - 5, height - 5, width - 10, height - 15)


class BasisWidget(QWidget):
    """Виджет для отображения базиса измерения"""
    def __init__(self, basis=None, size=40, parent=None):
        super().__init__(parent)
        self.basis = basis
        self.size = size
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
    
    def setBasis(self, basis):
        """Устанавливает базис для отображения"""
        self.basis = basis
        self.update()
    
    def paintEvent(self, event):
        if not self.basis:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Настройка кисти и пера
        painter.setPen(QPen(QColor("#333333"), 2))
        
        width = self.size
        height = self.size
        
        if self.basis == '+':
            # Рисуем прямоугольный базис (горизонтальная и вертикальная линии)
            painter.drawLine(5, height // 2, width - 5, height // 2)
            painter.drawLine(width // 2, 5, width // 2, height - 5)
        elif self.basis == '×':
            # Рисуем диагональный базис (диагональные линии)
            painter.drawLine(5, 5, width - 5, height - 5)
            painter.drawLine(5, height - 5, width - 5, 5)


class BitDisplay(QWidget):
    """Виджет для отображения бита (0 или 1)"""
    def __init__(self, bit=None, size=40, parent=None):
        super().__init__(parent)
        self.bit = bit
        self.size = size
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
    
    def setBit(self, bit):
        """Устанавливает бит для отображения"""
        self.bit = bit
        self.update()
    
    def paintEvent(self, event):
        if self.bit is None:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Настройка кисти и пера
        painter.setPen(QPen(QColor("#333333"), 2))
        
        if self.bit == 0:
            painter.setBrush(QBrush(QColor("#88c0d0")))  # Синий для 0
        else:
            painter.setBrush(QBrush(QColor("#bf616a")))  # Красный для 1
            
        # Рисуем круг
        width = self.size
        height = self.size
        painter.drawEllipse(5, 5, width - 10, height - 10)
        
        # Рисуем текст
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        painter.drawText(0, 0, width, height, Qt.AlignmentFlag.AlignCenter, str(self.bit))


class QuantumBB84GUI(QMainWindow):
    """Главное окно приложения с GUI для протокола BB84"""
    def __init__(self):
        super().__init__()
        self.simulator = QuantumBB84(length=10)
        self.initUI()
        
    def initUI(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Квантовое распределение ключей - Протокол BB84")
        self.setGeometry(100, 100, 1200, 800)
        
        # Создаем центральный виджет и основной макет
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем группы для различных этапов протокола
        control_group = self.createControlGroup()
        alice_group = self.createAliceGroup()
        quantum_channel_group = self.createQuantumChannelGroup()
        bob_group = self.createBobGroup()
        result_group = self.createResultGroup()
        
        # Добавляем группы в основной макет
        main_layout.addWidget(control_group)
        main_layout.addWidget(alice_group)
        main_layout.addWidget(quantum_channel_group)
        main_layout.addWidget(bob_group)
        main_layout.addWidget(result_group)
        
        # Устанавливаем центральный виджет
        self.setCentralWidget(central_widget)
        
    def createControlGroup(self):
        """Создает группу элементов управления"""
        group_box = QGroupBox("Управление симуляцией")
        layout = QHBoxLayout()
        
        # Элементы управления
        self.length_spin = QSpinBox()
        self.length_spin.setRange(5, 50)
        self.length_spin.setValue(10)
        self.length_spin.valueChanged.connect(self.updateLength)
        
        self.eve_checkbox = QCheckBox("Включить подслушивание (Ева)")
        
        self.start_button = QPushButton("Запустить симуляцию")
        self.start_button.clicked.connect(self.runSimulation)
        
        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.resetSimulation)
        
        # Добавляем элементы в макет
        layout.addWidget(QLabel("Длина последовательности:"))
        layout.addWidget(self.length_spin)
        layout.addWidget(self.eve_checkbox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)
        layout.addStretch()
        
        group_box.setLayout(layout)
        return group_box
        
    def createAliceGroup(self):
        """Создает группу для отображения данных Алисы"""
        group_box = QGroupBox("Алиса")
        layout = QVBoxLayout()
        
        # Заголовок таблицы
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Биты:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Биты Алисы
        self.alice_bits_layout = QHBoxLayout()
        self.alice_bits_widgets = []
        for i in range(10):
            bit_widget = BitDisplay(size=30)
            self.alice_bits_widgets.append(bit_widget)
            self.alice_bits_layout.addWidget(bit_widget)
        layout.addLayout(self.alice_bits_layout)
        
        # Базисы Алисы
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Базисы:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        self.alice_bases_layout = QHBoxLayout()
        self.alice_bases_widgets = []
        for i in range(10):
            basis_widget = BasisWidget(size=30)
            self.alice_bases_widgets.append(basis_widget)
            self.alice_bases_layout.addWidget(basis_widget)
        layout.addLayout(self.alice_bases_layout)
        
        group_box.setLayout(layout)
        return group_box
        
    def createQuantumChannelGroup(self):
        """Создает группу для отображения квантового канала"""
        group_box = QGroupBox("Квантовый канал")
        layout = QVBoxLayout()
        
        # Заголовок для квантовых состояний
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Квантовые состояния:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Квантовые состояния
        self.quantum_states_layout = QHBoxLayout()
        self.quantum_states_widgets = []
        for i in range(10):
            state_widget = QuantumStateWidget(size=30)
            self.quantum_states_widgets.append(state_widget)
            self.quantum_states_layout.addWidget(state_widget)
        layout.addLayout(self.quantum_states_layout)
        
        # Информация о Еве (если присутствует)
        self.eve_info_label = QLabel("Ева не активна")
        layout.addWidget(self.eve_info_label)
        
        # Измененные состояния после Евы
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Состояния после измерения Евой:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        self.eve_states_layout = QHBoxLayout()
        self.eve_states_widgets = []
        for i in range(10):
            state_widget = QuantumStateWidget(size=30)
            self.eve_states_widgets.append(state_widget)
            self.eve_states_layout.addWidget(state_widget)
        layout.addLayout(self.eve_states_layout)
        
        group_box.setLayout(layout)
        return group_box
        
    def createBobGroup(self):
        """Создает группу для отображения данных Боба"""
        group_box = QGroupBox("Боб")
        layout = QVBoxLayout()
        
        # Базисы Боба
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Базисы:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        self.bob_bases_layout = QHBoxLayout()
        self.bob_bases_widgets = []
        for i in range(10):
            basis_widget = BasisWidget(size=30)
            self.bob_bases_widgets.append(basis_widget)
            self.bob_bases_layout.addWidget(basis_widget)
        layout.addLayout(self.bob_bases_layout)
        
        # Измеренные биты Боба
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Измеренные биты:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        self.bob_bits_layout = QHBoxLayout()
        self.bob_bits_widgets = []
        for i in range(10):
            bit_widget = BitDisplay(size=30)
            self.bob_bits_widgets.append(bit_widget)
            self.bob_bits_layout.addWidget(bit_widget)
        layout.addLayout(self.bob_bits_layout)
        
        group_box.setLayout(layout)
        return group_box
    
    def createResultGroup(self):
        """Создает группу для отображения результатов"""
        group_box = QGroupBox("Результаты")
        layout = QVBoxLayout()
        
        # Сравнение базисов
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Совпадающие базисы:"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        self.matching_bases_layout = QHBoxLayout()
        self.matching_bases_widgets = []
        for i in range(10):
            label = QLabel("?")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(30, 30)
            label.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
            self.matching_bases_widgets.append(label)
            self.matching_bases_layout.addWidget(label)
        layout.addLayout(self.matching_bases_layout)
        
        # Итоговый ключ
        self.final_key_label = QLabel("Просеянный ключ: ")
        layout.addWidget(self.final_key_label)
        
        # Частота ошибок
        self.error_rate_label = QLabel("Частота ошибок: -")
        layout.addWidget(self.error_rate_label)
        
        # Вывод о подслушивании
        self.eavesdropping_label = QLabel("")
        self.eavesdropping_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.eavesdropping_label)
        
        group_box.setLayout(layout)
        return group_box
    
    def updateLength(self, value):
        """Обновляет длину последовательности"""
        self.simulator.length = value
        
        # Обновляем виджеты в зависимости от новой длины
        for i in range(max(len(self.alice_bits_widgets), value)):
            visible = i < value
            
            if i < len(self.alice_bits_widgets):
                self.alice_bits_widgets[i].setVisible(visible)
            else:
                bit_widget = BitDisplay(size=30)
                self.alice_bits_widgets.append(bit_widget)
                self.alice_bits_layout.addWidget(bit_widget)
            
            if i < len(self.alice_bases_widgets):
                self.alice_bases_widgets[i].setVisible(visible)
            else:
                basis_widget = BasisWidget(size=30)
                self.alice_bases_widgets.append(basis_widget)
                self.alice_bases_layout.addWidget(basis_widget)
            
            if i < len(self.quantum_states_widgets):
                self.quantum_states_widgets[i].setVisible(visible)
            else:
                state_widget = QuantumStateWidget(size=30)
                self.quantum_states_widgets.append(state_widget)
                self.quantum_states_layout.addWidget(state_widget)
            
            if i < len(self.eve_states_widgets):
                self.eve_states_widgets[i].setVisible(visible)
            else:
                state_widget = QuantumStateWidget(size=30)
                self.eve_states_widgets.append(state_widget)
                self.eve_states_layout.addWidget(state_widget)
            
            if i < len(self.bob_bases_widgets):
                self.bob_bases_widgets[i].setVisible(visible)
            else:
                basis_widget = BasisWidget(size=30)
                self.bob_bases_widgets.append(basis_widget)
                self.bob_bases_layout.addWidget(basis_widget)
            
            if i < len(self.bob_bits_widgets):
                self.bob_bits_widgets[i].setVisible(visible)
            else:
                bit_widget = BitDisplay(size=30)
                self.bob_bits_widgets.append(bit_widget)
                self.bob_bits_layout.addWidget(bit_widget)
            
            if i < len(self.matching_bases_widgets):
                self.matching_bases_widgets[i].setVisible(visible)
            else:
                label = QLabel("?")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFixedSize(30, 30)
                label.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
                self.matching_bases_widgets.append(label)
                self.matching_bases_layout.addWidget(label)
    
    def runSimulation(self):
        """Запускает симуляцию протокола BB84"""
        # Получаем параметры симуляции
        self.simulator.length = self.length_spin.value()
        with_eavesdropping = self.eve_checkbox.isChecked()
        
        # Запускаем симуляцию
        results = self.simulator.run_simulation(with_eavesdropping=with_eavesdropping)
        
        # Обновляем интерфейс с результатами
        self.updateInterface(results)
    
    def resetSimulation(self):
        """Сбрасывает симуляцию и интерфейс"""
        self.simulator.reset()
        
        # Очищаем все виджеты
        for widget in self.alice_bits_widgets:
            widget.setBit(None)
        
        for widget in self.alice_bases_widgets:
            widget.setBasis(None)
        
        for widget in self.quantum_states_widgets:
            widget.setState(None)
            
        for widget in self.eve_states_widgets:
            widget.setState(None)
        
        for widget in self.bob_bases_widgets:
            widget.setBasis(None)
        
        for widget in self.bob_bits_widgets:
            widget.setBit(None)
        
        for widget in self.matching_bases_widgets:
            widget.setText("?")
            widget.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
        
        # Сбрасываем метки
        self.final_key_label.setText("Просеянный ключ: ")
        self.error_rate_label.setText("Частота ошибок: -")
        self.eavesdropping_label.setText("")
        self.eve_info_label.setText("Ева не активна")
    
    def updateInterface(self, results):
        """Обновляет интерфейс с результатами симуляции"""
        # Обновляем данные Алисы
        for i, bit in enumerate(results['alice_bits']):
            if i < len(self.alice_bits_widgets):
                self.alice_bits_widgets[i].setBit(bit)
        
        for i, basis in enumerate(results['alice_bases']):
            if i < len(self.alice_bases_widgets):
                self.alice_bases_widgets[i].setBasis(basis)
        
        # Обновляем квантовые состояния
        for i, state in enumerate(results['quantum_states']):
            if i < len(self.quantum_states_widgets):
                self.quantum_states_widgets[i].setState(state)
        
        # Если Ева активна, обновляем информацию о ней
        if results['eve_present']:
            self.eve_info_label.setText("Ева активна - перехватывает и измеряет кубиты")
            for i, state in enumerate(self.simulator.modified_states):
                if i < len(self.eve_states_widgets):
                    self.eve_states_widgets[i].setState(state)
        else:
            self.eve_info_label.setText("Ева не активна")
            for widget in self.eve_states_widgets:
                widget.setState(None)
        
        # Обновляем данные Боба
        for i, basis in enumerate(results['bob_bases']):
            if i < len(self.bob_bases_widgets):
                self.bob_bases_widgets[i].setBasis(basis)
        
        for i, bit in enumerate(results['bob_measured_bits']):
            if i < len(self.bob_bits_widgets):
                self.bob_bits_widgets[i].setBit(bit)
        
        # Обновляем информацию о совпадающих базисах
        for i in range(len(results['alice_bases'])):
            if i < len(self.matching_bases_widgets):
                if i in results['matching_indices']:
                    self.matching_bases_widgets[i].setText("✓")
                    self.matching_bases_widgets[i].setStyleSheet("background-color: lightgreen; border: 1px solid green;")
                else:
                    self.matching_bases_widgets[i].setText("✗")
                    self.matching_bases_widgets[i].setStyleSheet("background-color: pink; border: 1px solid red;")
        
        # Обновляем итоговую информацию
        alice_key = ''.join(str(b) for b in results['sifted_key_alice'])
        bob_key = ''.join(str(b) for b in results['sifted_key_bob'])
        self.final_key_label.setText(f"Просеянный ключ Алисы: {alice_key}\nПросеянный ключ Боба: {bob_key}")
        
        self.error_rate_label.setText(f"Частота ошибок: {results['error_rate']:.2%}")
        
        if results['error_rate'] > 0:
            self.eavesdropping_label.setText("ВНИМАНИЕ: Обнаружено подслушивание! Канал небезопасен.")
            self.eavesdropping_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.eavesdropping_label.setText("Канал безопасен, подслушивание не обнаружено.")
            self.eavesdropping_label.setStyleSheet("color: green; font-weight: bold;")


def main():
    """Запуск приложения с графическим интерфейсом"""
    app = QApplication(sys.argv)
    window = QuantumBB84GUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
