import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QMessageBox, QStackedWidget, QCalendarWidget, QDialog, QFormLayout,
                             QDateEdit, QSpinBox, QComboBox, QFrame, QDialogButtonBox, QListWidget,
                             QTextEdit, QFileDialog)
from PyQt6.QtGui import QIcon, QFont, QPixmap, QTextCharFormat, QTextDocument
from PyQt6.QtCore import QTimer, QDate, Qt, QDateTime
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import sqlite3
import random
from datetime import datetime, timedelta
from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QValueAxis, QBarCategoryAxis

class StyleSheet:
    @staticmethod
    def get_style(is_dark_mode=False):
        if is_dark_mode:
            return """
            QMainWindow, QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #34495e;
                border-radius: 5px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QLabel {
                font-size: 16px;
                color: #ecf0f1;
            }
            QTableWidget {
                background-color: #34495e;
                alternate-background-color: #2c3e50;
                color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: none;
            }
            QCalendarWidget {
                background-color: #34495e;
                color: #ecf0f1;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #ecf0f1;
                background-color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: #ecf0f1;
            }
            #date_time_label {
                color: #ecf0f1;
                font-size: 18px;
                font-weight: bold;
            }
            """
        else:
            return """
            QMainWindow, QWidget {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QLabel {
                font-size: 16px;
                color: #2c3e50;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: none;
            }
            #date_time_label {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
            }
            """
        
class LoginWindow(QWidget):
    def __init__(self, switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main
        self.admin_username = "admin"
        self.admin_password = "123"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add semi-transparent overlay
        overlay = QWidget(self)
        overlay.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 20px;")
        overlay_layout = QVBoxLayout(overlay)
        
        logo_label = QLabel()
        pixmap = QPixmap("church_logo.png")
        logo_label.setPixmap(pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(logo_label)
        
        title_label = QLabel('نظام إدارة المخدومين')
        title_label.setStyleSheet("""
            font-size: 28px;
            color: #2c3e50;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(title_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #2980b9;
            }
        """)
        overlay_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #2980b9;
            }
        """)
        overlay_layout.addWidget(self.password_input)
        
        login_button = QPushButton('تسجيل الدخول')
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        overlay_layout.addWidget(login_button)

        login_button.clicked.connect(self.login)

        layout.addWidget(overlay)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_message('خطأ', 'اسم المستخدم وكلمة المرور لا يمكن أن تكون فارغة', QMessageBox.Icon.Warning)
            return
        
        if username == self.admin_username and password == self.admin_password:
            self.show_message('نجاح', 'تم تسجيل الدخول بنجاح!', QMessageBox.Icon.Information)
            self.switch_to_main()
        else:
            self.show_message('خطأ', 'اسم المستخدم أو كلمة المرور غير صحيحة', QMessageBox.Icon.Warning)

    def show_message(self, title, message, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 16px;
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 14px;
                border-radius: 3px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        msg_box.exec()
                    
class ServantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة مخدوم جديد")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setDisplayFormat("dd/MM/yyyy")
        self.phone_input = QLineEdit()
        self.service_input = QComboBox()
        self.service_input.addItems(["مدارس الأحد", "الشباب", "الخدمة الاجتماعية", "الكورال", "المسرح", "إعداد خدام", "الكشافة"])
        self.confession_father_input = QLineEdit()
        self.address_input = QLineEdit()
        
        layout.addRow("الاسم", self.name_input)
        layout.addRow("تاريخ الميلاد", self.birthdate_input)
        layout.addRow("رقم الهاتف", self.phone_input)
        layout.addRow("الخدمة", self.service_input)
        layout.addRow("أب الاعتراف", self.confession_father_input)
        layout.addRow("العنوان", self.address_input)
        
        buttons = QHBoxLayout()
        save_button = QPushButton("حفظ")
        cancel_button = QPushButton("إلغاء")
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, church_system):
        super().__init__()
        self.church_system = church_system
        self.setWindowTitle('نظام إدارة المخدومين')
        self.setGeometry(100, 100, 1000, 700)
        self.is_dark_mode = False
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # إنشاء تخطيط أفقي للتاريخ والوقت
        date_time_layout = QHBoxLayout()

        # إضافة التاريخ والوقت
        self.date_time_label = QLabel()
        self.date_time_label.setObjectName("date_time_label")
        self.date_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_time_layout.addWidget(self.date_time_label)

        # إضافة تخطيط التاريخ والوقت إلى التخطيط الرئيسي
        left_layout.addLayout(date_time_layout)
        
        self.verse_frame = QFrame()
        self.verse_frame.setFrameShape(QFrame.Shape.Box)
        self.verse_frame.setStyleSheet("QFrame { border: 2px solid #3498db; border-radius: 5px; background-color: #ecf0f1; }")
        verse_layout = QVBoxLayout(self.verse_frame)
        self.daily_verse_label = QLabel()
        self.daily_verse_label.setWordWrap(True)
        self.daily_verse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        verse_layout.addWidget(self.daily_verse_label)
        left_layout.addWidget(self.verse_frame)

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.show_daily_records)
        left_layout.addWidget(self.calendar)

        self.stats_label = QLabel('إحصائيات:\nعدد المخدومين: 0\nنسبة الحضور: 0%')
        left_layout.addWidget(self.stats_label)

        main_layout.addWidget(left_panel, 1)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # إضافة حقل البحث وزر البحث
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("البحث عن مخدوم...")
        self.search_button = QPushButton("بحث")
        self.search_button.clicked.connect(self.search_servants)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        right_layout.addLayout(self.search_layout)

        # إضافة القائمة المنسدلة لاختيار معيار البحث
        self.search_criteria = QComboBox()
        self.search_criteria.addItems(["الكل", "الاسم", "الهاتف", "الخدمة", "أب الاعتراف", "العنوان"])
        right_layout.addWidget(self.search_criteria)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(['الاسم', 'تاريخ الميلاد', 'الهاتف', 'الخدمة', 'أب الاعتراف', 'العنوان', 'الحضور', 'الغياب'])
        self.table.setStyleSheet("""
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item QLabel {
                margin: 0;
                padding: 0;
            }
        """)
        right_layout.addWidget(self.table)

        control_layout = QHBoxLayout()
         # إضافة زر للتذكيرات
        reminders_button = QPushButton('التذكيرات')
        reminders_button.clicked.connect(self.show_reminders)
        control_layout.addWidget(reminders_button)
        
        add_edit_button = QPushButton('إضافة/تعديل مخدوم')
        delete_button = QPushButton('حذف مخدوم')
        attendance_button = QPushButton('تسجيل الحضور/الغياب')
        report_button = QPushButton('تقرير الخدمة')
        control_layout.addWidget(add_edit_button)
        control_layout.addWidget(delete_button)
        control_layout.addWidget(attendance_button)
        control_layout.addWidget(report_button)
        right_layout.addLayout(control_layout)

        main_layout.addWidget(right_panel, 3)

        add_edit_button.clicked.connect(self.add_or_edit_servant)
        delete_button.clicked.connect(self.delete_servant)
        attendance_button.clicked.connect(self.mark_attendance)
        report_button.clicked.connect(self.generate_report)

        self.night_mode_button = QPushButton('الوضع الليلي')
        self.night_mode_button.clicked.connect(self.toggle_night_mode)
        left_layout.addWidget(self.night_mode_button)
        
        self.init_database()
        self.load_data()

        # تحديث التاريخ والوقت والـ highlight عند بدء التطبيق
        self.update_date_time()

        # إعداد مؤقت لتحديث التاريخ والوقت كل دقيقة
        self.date_time_timer = QTimer(self)
        self.date_time_timer.timeout.connect(self.update_date_time)
        self.date_time_timer.start(60000)  # تحديث كل دقيقة (60000 ميلي ثانية)


        self.update_daily_verse()

        # زر إحصائية الغياب والحضور
        attendance_stats_button = QPushButton('إحصائية الغياب والحضور')
        attendance_stats_button.clicked.connect(self.show_attendance_statistics)
        control_layout.addWidget(attendance_stats_button)

        # إضافة ور تسجيل الخروج
        logout_button = QPushButton('تسجيل الخروج')
        logout_button.clicked.connect(self.logout)
        left_layout.addWidget(logout_button)

    def logout(self):
        try:
            reply = QMessageBox.question(self, 'تأكيد تسجيل الخروج', 
                                 'هل أنت متأكد من أنك تريد تسجيل الخروج؟',
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                 QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                QMessageBox.information(self, 'تسجيل الخروج', 'تم تسجيل الخروج بنجاح')
                self.church_system.switch_to_login()
        except Exception as e:
            QMessageBox.warning(self, 'خطأ', f'حدث خطأ أثناء تسجيل الخروج: {str(e)}')
            
        
    def init_database(self):
        db_path = 'church_database.db'
        
        # إذا كانت قاعدة البيانات غير موجودة، قم بإنشائها
        if not os.path.exists(db_path):
            QMessageBox.warning(self, 'تحذير', 'لا تحذف قاعدة البيانات')
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # إنشاء جدول servants إذا لم يكن موجوداً
        c.execute('''CREATE TABLE IF NOT EXISTS servants
                     (id INTEGER PRIMARY KEY, name TEXT, birthdate TEXT, phone TEXT, 
                      service TEXT, confession_father TEXT, address TEXT, attendance INTEGER, absence INTEGER)''')
        
        # التحقق من وجود عمود 'absence' وإضافته إذا لم يكن موجوداً
        c.execute("PRAGMA table_info(servants)")
        columns = [column[1] for column in c.fetchall()]
        if 'absence' not in columns:
            c.execute("ALTER TABLE servants ADD COLUMN absence INTEGER DEFAULT 0")
        
        # إنشاء جدول daily_records إذا لم يكن موجوداً
        c.execute('''CREATE TABLE IF NOT EXISTS daily_records
                     (date TEXT PRIMARY KEY, records TEXT)''')
        
        conn.commit()
        conn.close()

    def check_birthday_and_visitation(self, name, birthdate):
        today = QDate.currentDate()
        birthday = QDate.fromString(birthdate, "yyyy-MM-dd")
    
        # فحص عيد الميلاد
        days_until_birthday = today.daysTo(birthday.addYears(today.year() - birthday.year()))
        if 0 <= days_until_birthday <= 7:
            return f"تذكير: عيد ميلاد {name} بعد {days_until_birthday} يوم"
        # تذكير بالافتقاد
        return f"تذكير: افتقاد {name} هذا الأسبوع"

    def search_servants(self):
        search_text = self.search_input.text()
        search_criterion = self.search_criteria.currentText()

        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()

        all_columns = ["name", "birthdate", "phone", "service", "confession_father", "address", "attendance", "absence"]
        display_columns = all_columns

        if search_criterion == "الكل" or not search_text:
            query = f"SELECT {', '.join(all_columns)} FROM servants"
            c.execute(query)
        else:
            column_mapping = {
            "الاسم": "name",
            "الهاتف": "phone",
            "الخدمة": "service",
            "أب الاعتراف": "confession_father",
            "العنوان": "address"
            }
            search_column = column_mapping[search_criterion]
            query = f"SELECT {', '.join(all_columns)} FROM servants WHERE {search_column} LIKE ?"
            c.execute(query, (f'%{search_text}%',))

        servants = c.fetchall()
        conn.close()

        if not servants:
            QMessageBox.information(self, 'نتيجة البحث', 'لا يوجد مخدومين مطابقين لمعايير البحث')
            return

        # تحديث عناوين الأعمدة وعدد الأعمدة في الجدول
        column_headers = {
        "name": "الاسم",
        "birthdate": "تاريخ الميلاد",
        "phone": "الهاتف",
        "service": "الخدمة",
        "confession_father": "أب الاعتراف",
        "address": "العنوان",
        "attendance": "الحضور",
        "absence": "الغياب"
        }
        self.table.setColumnCount(len(display_columns))
        self.table.setHorizontalHeaderLabels([column_headers[col] for col in display_columns])

        # ملء الجدول بالبيانات
        self.table.setRowCount(len(servants))
        for row, servant in enumerate(servants):
            for col, column_name in enumerate(display_columns):
                value = servant[all_columns.index(column_name)]
                if column_name in ['attendance', 'absence']:
                    item = QTableWidgetItem()
                    label = QLabel()
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if value > 0:
                        pixmap = QPixmap('check.png' if column_name == 'attendance' else 'cross.png')
                        label.setPixmap(pixmap)
                        self.table.setCellWidget(row, col, label)
                else:
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()
        self.update_stats()

    def get_column_header(self, column_name):
        headers = {
        "name": "الاسم",
        "birthdate": "تاريخ الميلاد",
        "phone": "الهاتف",
        "service": "الخدمة",
        "confession_father": "أب الاعتراف",
        "address": "العنوان",
        "attendance": "الحضور",
        "absence": "الغياب"
        }
        return headers.get(column_name, column_name)

    def show_reminders(self):
        try:
            dialog = RemindersDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.warning(self, 'خطأ', f'حدث خطأ أثناء استرجاع التذكيرات من قاعدة البيانات: {str(e)}')
        
        
    def load_data(self):
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
        c.execute("SELECT name, birthdate, phone, service, confession_father, address, attendance, absence FROM servants")
        servants = c.fetchall()
        self.table.setRowCount(len(servants))
        for row, servant in enumerate(servants):
            for col, value in enumerate(servant):
                if col in [6, 7]:  # Attendance and Absence columns
                    item = QTableWidgetItem()
                    label = QLabel()
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if value > 0:
                        pixmap = QPixmap('check.png' if col == 6 else 'cross.png')
                        label.setPixmap(pixmap)
                    self.table.setCellWidget(row, col, label)
                else:
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
        
        # تحميل السجلات اليومية وتحديث التقويم
        c.execute("SELECT date FROM daily_records")
        dates_with_records = [QDate.fromString(date[0], "yyyy-MM-dd") for date in c.fetchall()]
        self.update_calendar_format(dates_with_records)
        
        conn.close()
        self.update_stats()
        self.update_search_visibility()

    def update_search_visibility(self):
        is_table_empty = self.table.rowCount() == 0
        self.search_input.setVisible(not is_table_empty)
        self.search_button.setVisible(not is_table_empty)
        self.search_criteria.setVisible(not is_table_empty)

    def update_calendar_format(self, dates_with_records):
        format = QTextCharFormat()
        format.setFontWeight(QFont.Weight.Bold)
        format.setBackground(Qt.GlobalColor.lightGray)
        
        for date in dates_with_records:
            self.calendar.setDateTextFormat(date, format)

    def generate_report(self):
        try:
            conn = sqlite3.connect('church_database.db')
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM servants")
            servant_count = c.fetchone()[0]
            if servant_count == 0:
                QMessageBox.warning(self, 'لا توجد بيانات', 'لا توجد بيانات المخدومين')
                conn.close()
                return
            
            # استخراج البيانات من قاعدة البيانات
            c.execute("""SELECT name, service, 
                 (SELECT COUNT(*) FROM daily_records WHERE records LIKE '%' || servants.name || '%حاضر%') as attendance,
                 (SELECT COUNT(*) FROM daily_records WHERE records LIKE '%' || servants.name || '%غائب%') as absence
                 FROM servants""")
            servants_data = c.fetchall()

            # حساب الإحصائيات العامة
            total_servants = len(servants_data)
            total_attendance = sum(servant[2] for servant in servants_data)
            total_absence = sum(servant[3] for servant in servants_data)

            # إنشاء محتوى التقرير
            report_content = "تقرير الخدمة\n\n"
            report_content += f" :إجمالي عدد المخدومين {total_servants}\n"
            report_content += f" :إجمالي الحضور {total_attendance}\n"
            report_content += f" :إجمالي الغياب {total_absence}\n\n"

            # جدول تفصيلي للمخدومين
            report_content += "الاسم                    الخدمة        الحضور  الغياب\n"
            report_content += "-" * 52 + "\n"
            for servant in servants_data:
                report_content += f"{servant[0]:<25} {servant[1]:<12} {servant[2]:<7} {servant[3]:<7}\n"
                
            # إحصائيات حسب الخدمة
            services = {}
            for servant in servants_data:
                if servant[1] not in services:
                    services[servant[1]] = {'count': 0, 'attendance': 0, 'absence': 0}
                    services[servant[1]]['count'] += 1
                    services[servant[1]]['attendance'] += servant[2]
                    services[servant[1]]['absence'] += servant[3]

            report_content += "\nإحصائيات حسب الخدمة\n"
            report_content += "-" * 52 + "\n"
            report_content += "الخدمة        عدد المخدومين  إجمالي الحضور  إجمالي الغياب\n"
            report_content += "-" * 52 + "\n"
            for service, data in services.items():
                report_content += f"{service:<12} {data['count']:<15} {data['attendance']:<15} {data['absence']:<15}\n"
            conn.close()

            # إنشاء مستند HTML
            html_content = f"<pre dir='rtl' style='font-family: Arial; font-size: 150px;'>{report_content}</pre>"
            document = QTextDocument()
            document.setHtml(html_content)

            # طباعة التقرير
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                document.print(printer)
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'خطأ', f'حدث خطأ أثناء إنشاء التقرير: {str(e)}')
        
    # إنشاء إحصائية الحضور والغياب
    def show_attendance_statistics(self):
        dialog = AttendanceStatisticsDialog(self)
        dialog.exec()

    def show_daily_records(self):
        try:
            selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")

            conn = sqlite3.connect('church_database.db')
            c = conn.cursor()

            # التحقق من وجود الجدول
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_records'")
            if not c.fetchone():
                conn.close()
                self.init_database()
                conn = sqlite3.connect('church_database.db')
                c = conn.cursor()
            # الحصول على السجلات لليوم المحدد
            c.execute("SELECT records FROM daily_records WHERE date = ?", (selected_date,))
            result = c.fetchone()

            # الحصول على جميع المخدومين
            c.execute("SELECT name FROM servants")
            all_servants = [row[0] for row in c.fetchall()]

            dialog = QDialog(self)
            dialog.setWindowTitle(f'سجلات {selected_date}')
            layout = QVBoxLayout()

            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(['الاسم', 'الحالة'])
            table.setRowCount(len(all_servants))

            # تكبير الجدول
            table.setMinimumWidth(400)
            table.setMinimumHeight(300)
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setDefaultSectionSize(30)

            if result:
                records = dict(record.rsplit(' ', 1) for record in result[0].split('\n'))
            else:
                records = {}
            for row, name in enumerate(all_servants):
                table.setItem(row, 0, QTableWidgetItem(name))
                status = records.get(name, 'غير مسجل')
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # توسيط النص
                table.setItem(row, 1, status_item)

            table.resizeColumnsToContents()
            layout.addWidget(table)

            close_button = QPushButton('إغلاق')
            close_button.clicked.connect(dialog.accept)
            layout.addWidget(close_button)

            dialog.setLayout(layout)
            dialog.exec()

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'خطأ', f'حدث خطأ أثناء عرض السجلات: {str(e)}')
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'خطأ', f'حدث خطأ أثناء إنشاء التقرير: {str(e)}')
        finally:
            if conn:
                conn.close()
            
        
    def add_or_edit_servant(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            # Edit existing servant
            row = selected_items[0].row()
            servant_data = self.get_servant_data(row)
            dialog = ServantDialog(self, servant_data)
        else:
            # Add new servant
            dialog = ServantDialog(self)
        while True:
            if dialog.exec():
                name = dialog.name_input.text()
                birthdate = dialog.birthdate_input.date().toString("yyyy-MM-dd")
                phone = dialog.phone_input.text()
                service = dialog.service_input.currentText()
                confession_father = dialog.confession_father_input.text()
                address = dialog.address_input.text()

                if not all([name, birthdate, phone, service, confession_father, address]):
                    QMessageBox.warning(self, 'الحقل فارغ', 'جميع الحقول مطلوبة. يرجى ملء جميع الحقول.')
                    continue  # This will keep the dialog open

                try:
                    conn = sqlite3.connect('church_database.db')
                    c = conn.cursor()
                    if selected_items:
                        # Update existing servant data
                        c.execute("""UPDATE servants SET name=?, birthdate=?, phone=?, service=?, 
                                 confession_father=?, address=? WHERE name=?""",
                              (name, birthdate, phone, service, confession_father, address, servant_data['name']))
                        QMessageBox.information(self, 'نجاح', 'تم تحديث بيانات المخدوم بنجاح!')
                    else:
                        # Add new servant
                        c.execute("""INSERT INTO servants (name, birthdate, phone, service, 
                                 confession_father, address, attendance, absence) 
                                 VALUES (?, ?, ?, ?, ?, ?, 0, 0)""",
                              (name, birthdate, phone, service, confession_father, address))
                        QMessageBox.information(self, 'نجاح', 'تمت إضافة المخدوم بنجاح!')
                    conn.commit()
                
                    # إضافة التذكير بعيد الميلاد والافتقاد
                    reminder = self.check_birthday_and_visitation(name, birthdate)
                    QMessageBox.information(self, 'تذكير', reminder)
                    
                
                except sqlite3.Error as e:
                    QMessageBox.critical(self, 'خطأ', f'حدث خطأ أثناء حفظ بيانات المخدوم: {str(e)}')
                finally:
                    if conn:
                        conn.close()
                self.load_data()
                break  # Exit the loop if successful
            else:
                # User clicked Cancel
                break

        
    def delete_servant(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, ' تنبيه', 'رجاءً تحديد المخدوم المناسب')
            return
        
        row = selected_items[0].row()
        name = self.table.item(row, 0).text()
        
        reply = QMessageBox.question(self, 'تأكيد الحذف',
                                     f'هل أنت متأكد من حذف المخدوم {name}؟',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('church_database.db')
            c = conn.cursor()
            c.execute("DELETE FROM servants WHERE name=?", (name,))
            conn.commit()
            conn.close()
            self.load_data()
            
    def get_servant_data(self, row):
        return {
            'name': self.table.item(row, 0).text(),
            'birthdate': self.table.item(row, 1).text(),
            'phone': self.table.item(row, 2).text(),
            'service': self.table.item(row, 3).text(),
            'confession_father': self.table.item(row, 4).text(),
            'address': self.table.item(row, 5).text()
        }
    
    def mark_attendance(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'تنبيه', 'رجاءً تحديد المخدوم المناسب')
            return
    
        row = selected_items[0].row()
        name = self.table.item(row, 0).text()

        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
        c.execute("SELECT attendance, absence FROM servants WHERE name = ?", (name,))
        current_attendance, current_absence = c.fetchone()
        conn.close()

        dialog = QDialog(self)
        dialog.setWindowTitle('تسجيل الحضور/الغياب')
        layout = QVBoxLayout()

        label = QLabel(f'ما هو وضع الحضور للمخدوم {name}؟')
        layout.addWidget(label)

        present_button = QPushButton('حاضر')
        absent_button = QPushButton('غائب')
        correct_button = QPushButton('تصحيح خطأ سابق')

        layout.addWidget(present_button)
        layout.addWidget(absent_button)
        layout.addWidget(correct_button)

        dialog.setLayout(layout)

        def mark_present():
            if current_attendance > 0 or current_absence > 0:
                QMessageBox.warning(dialog, 'تنبيه', 'لا يمكن التسجيل مرة أخرى')
            else:
                self.update_attendance(name, row, True)
            dialog.accept()

        def mark_absent():
            if current_attendance > 0 or current_absence > 0:
                QMessageBox.warning(dialog, 'تنبيه', 'لا يمكن التسجيل مرة أخرى')
            else:
                self.update_attendance(name, row, False)
            dialog.accept()

        def correct_previous():
            dialog.accept()
            self.correct_attendance(name, row)

        present_button.clicked.connect(mark_present)
        absent_button.clicked.connect(mark_absent)
        correct_button.clicked.connect(correct_previous)

        dialog.exec()


    def update_attendance(self, name, row, is_present):
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
    
        today = QDate.currentDate().toString("yyyy-MM-dd")
    
        if is_present:
            c.execute("UPDATE servants SET attendance = attendance + 1 WHERE name = ?", (name,))
            status = 'حاضر'
        else:
            c.execute("UPDATE servants SET absence = absence + 1 WHERE name = ?", (name,))
            status = 'غائب'

        # تحديث أو إضافة السجل اليومي
        c.execute("SELECT records FROM daily_records WHERE date = ?", (today,))
        result = c.fetchone()
        if result:
            current_records = result[0].split('\n')
            updated_records = [record for record in current_records if not record.startswith(name)]
            updated_records.append(f"{name} {status}")
            new_records = '\n'.join(updated_records)
        else:
            new_records = f"{name} {status}"
    
        c.execute("INSERT OR REPLACE INTO daily_records (date, records) VALUES (?, ?)", (today, new_records))
    
        conn.commit()
        conn.close()
    
        self.update_attendance_icon(row, 6 if is_present else 7, 'check.png' if is_present else 'cross.png')
        self.load_data()
        
        # عرض رسالة بعد تحديث الحضور
        QMessageBox.information(self, 'تحديث الحضور', f'المخدوم {name} {status} الآن')
        
        
    def update_attendance_icon(self, row, column, icon):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(icon)
        if not pixmap.isNull():
            label.setPixmap(pixmap)
        else:
            label.setText("!")  # fallback if image not found
        self.table.setCellWidget(row, column, label)

    def correct_attendance(self, name, row):
        try:
            conn = sqlite3.connect('church_database.db')
            c = conn.cursor()
    
            c.execute("SELECT attendance, absence FROM servants WHERE name = ?", (name,))
            result = c.fetchone()
    
            if result is None:
                QMessageBox.warning(self, 'خطأ', f'لم يتم العثور على بيانات للمخدوم {name}')
                return
    
            attendance, absence = result
    
            dialog = QDialog(self)
            dialog.setWindowTitle('تصحيح الحضور/الغياب')
            layout = QVBoxLayout()
    
            info_label = QLabel(f'تصحيح سجل الحضور والغياب للمخدوم: {name}')
            current_label = QLabel(f'الحضور الحالي: {attendance}, الغياب الحالي: {absence}')
            layout.addWidget(info_label)
            layout.addWidget(current_label)
    
            attendance_spinbox = QSpinBox()
            attendance_spinbox.setRange(0, 1000)
            attendance_spinbox.setValue(attendance)
            layout.addWidget(QLabel('الحضور الصحيح:'))
            layout.addWidget(attendance_spinbox)
    
            absence_spinbox = QSpinBox()
            absence_spinbox.setRange(0, 1000)
            absence_spinbox.setValue(absence)
            layout.addWidget(QLabel('الغياب الصحيح:'))
            layout.addWidget(absence_spinbox)
    
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            layout.addWidget(button_box)
    
            dialog.setLayout(layout)
    
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
    
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_attendance = attendance_spinbox.value()
                new_absence = absence_spinbox.value()
        
            if new_attendance < 0 or new_absence < 0:
                QMessageBox.warning(self, 'خطأ', 'لا يمكن أن تكون قيم الحضور أو الغياب سالبة.')
                return
            
            if new_attendance == new_absence:
                QMessageBox.warning(self, 'خطأ', 'لا يمكن تصحيح السجل: تساوى الحضور والغياب')
                return
        
            c.execute("UPDATE servants SET attendance = ?, absence = ? WHERE name = ?", (new_attendance, new_absence, name))
        
            # تحديث السجل اليومي مع الحالة الجديدة
            today = QDate.currentDate().toString("yyyy-MM-dd")
            c.execute("SELECT records FROM daily_records WHERE date = ?", (today,))
            result = c.fetchone()
            if result:
                current_records = result[0].split('\n')
                updated_records = [record for record in current_records if not record.startswith(name)]
            
            # تحديد الحالة الجديدة بناءً على التغييرات
            if new_absence > 0 and new_attendance == 0:
                status = 'غائب'
            elif new_attendance > 0 and new_absence == 0:
                status = 'حاضر'
            else:
                status = 'تم تصحيح السجل'
            
            updated_records.append(f"{name} {status}")
            new_records = '\n'.join(updated_records)
            c.execute("UPDATE daily_records SET records = ? WHERE date = ?", (new_records, today))
        
            conn.commit()
        
            self.update_attendance_icon(row, 6, 'check.png' if new_attendance > 0 else 'blank.png')
            self.update_attendance_icon(row, 7, 'cross.png' if new_absence > 0 else 'blank.png')
        
            QMessageBox.information(self, 'تم التصحيح', 
                                f'تم تحديث سجل الحضور والغياب للمخدوم {name}\n'
                                f'الحضور الجديد: {new_attendance}\n'
                                f'الغياب الجديد: {new_absence}\n'
                                f'الحالة: {status}')
        
            self.load_data()

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'خطأ في قاعدة البيانات', f'حدث خطأ أثناء تحديث البيانات: {str(e)}')
        except Exception as e:
            QMessageBox.critical(self, 'خطأ', f'حدث خطأ غير متوقع: {str(e)}')
        finally:
            if conn:
                conn.close()
                
    def update_daily_verse(self):
        verses = [
            "لأَنَّهُ هكَذَا أَحَبَّ اللهُ الْعَالَمَ حَتَّى بَذَلَ ابْنَهُ الْوَحِيدَ، لِكَيْ لاَ يَهْلِكَ كُلُّ مَنْ يُؤْمِنُ بِهِ، بَلْ تَكُونُ لَهُ الْحَيَاةُ الأَبَدِيَّةُ.   (يوحنا 3:16)",
            "أَنَا هُوَ الطَّرِيقُ وَالْحَقُّ وَالْحَيَاةُ. لَيْسَ أَحَدٌ يَأْتِي إِلَى الآبِ إِلاَّ بِي.   (يوحنا 14:6)",
            "لاَ تَخَفْ لأَنِّي مَعَكَ. لاَ تَتَلَفَّتْ لأَنِّي إِلهُكَ. قَدْ أَيَّدْتُكَ وَأَعَنْتُكَ وَعَضَدْتُكَ بِيَمِينِ بِرِّي.   (إشعياء 41:10)",
            "تَعَالَوْا إِلَيَّ يَا جَمِيعَ الْمُتْعَبِينَ وَالثَّقِيلِي الأَحْمَالِ، وَأَنَا أُرِيحُكُمْ.   (متى 11:28)"
        ]
        self.daily_verse_label.setText(f'آية اليوم \n\n {random.choice(verses)}')

    def update_date_time(self):
        current_datetime = QDateTime.currentDateTime()
        
        # تحديث التاريخ والوقت
        date_string = current_datetime.toString("dddd d MMMM yyyy")
        time_string = current_datetime.toString("hh:mm AP")
        self.date_time_label.setText(f"{date_string}\n{time_string}")
        
        # تحديث التقويم
        current_date = current_datetime.date()
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        today_format = QTextCharFormat()
        today_format.setBackground(Qt.GlobalColor.blue)
        today_format.setForeground(Qt.GlobalColor.white)
        self.calendar.setDateTextFormat(current_date, today_format)

    def toggle_night_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.setStyleSheet(StyleSheet.get_style(self.is_dark_mode))
        
        # تحديث لون إطار الآية
        verse_frame_style = "QFrame { border: 2px solid #3498db; border-radius: 5px; "
        verse_frame_style += "background-color: #34495e; }" if self.is_dark_mode else "background-color: #ecf0f1; }"
        self.verse_frame.setStyleSheet(verse_frame_style)
        
        # تحديث نص الزر
        self.night_mode_button.setText('الوضع العادي' if self.is_dark_mode else 'الوضع الليلي')

        # تحديث لون نص التاريخ والوقت
        date_time_color = "#ecf0f1" if self.is_dark_mode else "#2c3e50"
        self.date_time_label.setStyleSheet(f"color: {date_time_color}; font-size: 18px; font-weight: bold;")

    def update_stats(self):
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM servants")
        total_servants = c.fetchone()[0]
        c.execute("SELECT SUM(attendance), SUM(absence) FROM servants")
        result = c.fetchone()
        total_attendance = result[0] or 0
        total_absence = result[1] or 0
        conn.close()

        if total_servants > 0:
            attendance_rate = (total_attendance / (total_servants * 52)) * 100
            absence_rate = (total_absence / (total_servants * 52)) * 100
        else:
            attendance_rate = 0
            absence_rate = 0

        self.stats_label.setText(f'إحصائيات:\n'
                                 f'عدد المخدومين: {total_servants}\n'
                                 f'نسبة الحضور: {attendance_rate:.2f}%\n'
                                 f'نسبة الغياب: {absence_rate:.2f}%')
        
    def toggle_night_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.setStyleSheet(StyleSheet.get_style(self.is_dark_mode))
        
        # تحديث لون إطار الآية
        verse_frame_style = "QFrame { border: 2px solid #3498db; border-radius: 5px; "
        verse_frame_style += "background-color: #34495e; }" if self.is_dark_mode else "background-color: #ecf0f1; }"
        self.verse_frame.setStyleSheet(verse_frame_style)
        
        # تحديث نص الزر
        self.night_mode_button.setText('الوضع العادي' if self.is_dark_mode else 'الوضع الليلي')

class AttendanceStatisticsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إحصائية الغياب والحضور")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Date selection
        date_layout = QHBoxLayout()
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("من تاريخ:"))
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("إلى تاريخ:"))
        date_layout.addWidget(self.end_date)
        layout.addLayout(date_layout)

        # Period selection
        self.period_combo = QComboBox()
        self.period_combo.addItems(["يومي", "شهري", "سنوي"])
        layout.addWidget(self.period_combo)

        # Generate chart button
        generate_button = QPushButton("إنشاء الرسم البياني")
        generate_button.clicked.connect(self.generate_chart)
        layout.addWidget(generate_button)

        # Chart view
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        # Add Save Image button
        self.save_button = QPushButton("حفظ الصورة")
        self.save_button.clicked.connect(self.save_chart_image)
        self.save_button.setVisible(False)  # Hide it initially
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def generate_chart(self):
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        period = self.period_combo.currentText()

        # Fetch data from database
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()

        if period == "يومي":
            c.execute("""
                SELECT date, COUNT(CASE WHEN records LIKE '%حاضر%' THEN 1 END) as attendance,
                COUNT(CASE WHEN records LIKE '%غائب%' THEN 1 END) as absence
                FROM daily_records
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date
            """, (start_date, end_date))
        elif period == "شهري":
            c.execute("""
                SELECT strftime('%Y-%m', date) as month,
                COUNT(CASE WHEN records LIKE '%حاضر%' THEN 1 END) as attendance,
                COUNT(CASE WHEN records LIKE '%غائب%' THEN 1 END) as absence
                FROM daily_records
                WHERE date BETWEEN ? AND ?
                GROUP BY month
                ORDER BY month
            """, (start_date, end_date))
        else:  # سنوي
            c.execute("""
                SELECT strftime('%Y', date) as year,
                COUNT(CASE WHEN records LIKE '%حاضر%' THEN 1 END) as attendance,
                COUNT(CASE WHEN records LIKE '%غائب%' THEN 1 END) as absence
                FROM daily_records
                WHERE date BETWEEN ? AND ?
                GROUP BY year
                ORDER BY year
            """, (start_date, end_date))

        data = c.fetchall()
        conn.close()

        # Create chart
        chart = QChart()
        chart.setTitle(f"إحصائية الغياب والحضور ({period})")

        attendance_set = QBarSet("الحضور")
        absence_set = QBarSet("الغياب")
        categories = []

        for row in data:
            categories.append(row[0])
            attendance_set.append(row[1])
            absence_set.append(row[2])

        series = QBarSeries()
        series.append(attendance_set)
        series.append(absence_set)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chart_view.setChart(chart)

        # Show the save button after generating the chart
        self.save_button.setVisible(True)

    def save_chart_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "حفظ الصورة", "", "PNG Files (*.png);;All Files (*)")
        if file_name:
            pixmap = self.chart_view.grab()
            pixmap.save(file_name, "PNG")
            QMessageBox.information(self, "تم الحفظ", "تم حفظ الصورة بنجاح!")
            self.save_button.setVisible(False)  # Hide the button after successful save
        

class ServantDialog(QDialog):
    def __init__(self, parent=None, servant_data=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة/تعديل مخدوم")
        self.servant_data = servant_data
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setDisplayFormat("dd/MM/yyyy")
        self.phone_input = QLineEdit()
        self.service_input = QComboBox()
        self.service_input.addItems(["مدارس الأحد", "الشباب", "الخدمة الاجتماعية", "الكورال", "المسرح", "إعداد خدام", "الكشافة"])
        self.confession_father_input = QLineEdit()
        self.address_input = QLineEdit()
        
        layout.addRow("الاسم", self.name_input)
        layout.addRow("تاريخ الميلاد", self.birthdate_input)
        layout.addRow("رقم الهاتف", self.phone_input)
        layout.addRow("الخدمة", self.service_input)
        layout.addRow("أب الاعتراف", self.confession_father_input)
        layout.addRow("العنوان", self.address_input)
        
        if self.servant_data:
            self.name_input.setText(self.servant_data['name'])
            self.birthdate_input.setDate(QDate.fromString(self.servant_data['birthdate'], "yyyy-MM-dd"))
            self.phone_input.setText(self.servant_data['phone'])
            self.service_input.setCurrentText(self.servant_data['service'])
            self.confession_father_input.setText(self.servant_data['confession_father'])
            self.address_input.setText(self.servant_data['address'])
        
        buttons = QHBoxLayout()
        save_button = QPushButton("حفظ")
        cancel_button = QPushButton("إلغاء")
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)

class RemindersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("التذكيرات")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.reminders_list = QListWidget()
        layout.addWidget(self.reminders_list)

        refresh_button = QPushButton("تحديث التذكيرات")
        refresh_button.clicked.connect(self.refresh_reminders)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.refresh_reminders()

    def refresh_reminders(self):
        self.reminders_list.clear()
        self.add_weekly_visitation_reminders()
        self.add_birthday_reminders()

    def add_weekly_visitation_reminders(self):
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM servants")
        servants = c.fetchall()
        conn.close()

        for servant in servants:
            self.reminders_list.addItem(f"تذكير: افتقاد {servant[0]} هذا الأسبوع")

    def add_birthday_reminders(self):
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
        today = datetime.now().date()
        one_week_later = today + timedelta(days=7)

        c.execute("SELECT name, birthdate FROM servants")
        servants = c.fetchall()
        conn.close()

        for servant in servants:
            name, birthdate = servant
            birthday = datetime.strptime(birthdate, "%Y-%m-%d").date()
            birthday_this_year = birthday.replace(year=today.year)
            
            if today <= birthday_this_year <= one_week_later:
                days_until_birthday = (birthday_this_year - today).days
                self.reminders_list.addItem(f"عيد ميلاد {name} بعد {days_until_birthday} يوم")

    

class ChurchManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('نظام إدارة الكنيسة')
        self.setGeometry(100, 100, 1000, 700)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_window = LoginWindow(self.switch_to_main)
        self.main_window = MainWindow(self)  # تمرير الـ self هنا

        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.main_window)

        self.setStyleSheet(StyleSheet.get_style())

        # عرض رسائل البداية
        self.show_startup_messages()

        # إعداد مؤقت للتذكيرات
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(86400000)  # تحقق كل 24 ساعة (86400000 ميلي ثانية)

    def switch_to_main(self):
        self.stacked_widget.setCurrentWidget(self.main_window)

    def switch_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)

    def show_startup_messages(self):
        QMessageBox.information(self, "رسالة", "هذا المشروع خاص لمهرجان الكرازة المرقسية 2024")
        QMessageBox.information(self, "رسالة", "إعداد/ مينا روبير مجدي")

    def check_reminders(self):
        reminders = []
        
        # التحقق من تذكيرات الافتقاد الأسبوعي
        if datetime.now().weekday() == 0:  # افترض أن يوم الاثنين هو بداية الأسبوع
            reminders.append("تذكير: بدء أسبوع جديد للافتقاد")
        
        # التحقق من أعياد الميلاد القادمة
        conn = sqlite3.connect('church_database.db')
        c = conn.cursor()
        today = datetime.now().date()
        one_week_later = today + timedelta(days=7)

        c.execute("SELECT name, birthdate FROM servants")
        servants = c.fetchall()
        conn.close()

        for servant in servants:
            name, birthdate = servant
            birthday = datetime.strptime(birthdate, "%Y-%m-%d").date()
            birthday_this_year = birthday.replace(year=today.year)
            
            if today <= birthday_this_year <= one_week_later:
                days_until_birthday = (birthday_this_year - today).days
                reminders.append(f"عيد ميلاد {name} بعد {days_until_birthday} يوم")

        if reminders:
            reminder_text = "\n".join(reminders)
            QMessageBox.information(self, "تذكيرات", reminder_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('church_icon.png'))  
    app.setStyle('Fusion')  # استخدام نمط Fusion لواجهة مستخدم أكثر جاذبية
    church_system = ChurchManagementSystem()
    church_system.show()
    sys.exit(app.exec())
