from imports import *
from forms import *
sys.path.insert(0, "../")
from auth import Auth

def start_timer(end_date):
    current_date_time = QtCore.QDateTime.currentDateTime()
    fmt = current_date_time.toString("yyyy-MM-dd hh:mm:ss a")
    if datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]), int(end_date[9:11]), int(end_date[14:16]), int(end_date[17:19])) <= datetime(int(fmt[0:4]), int(fmt[5:7]), int(fmt[8:10]), int(fmt[9:11]), int(fmt[14:16]), int(fmt[17:19])):
        return "yes"
    else:
        return f"{days_in_between(fmt, end_date)} time left."


class QTreeWidgetCustom(QtWidgets.QTreeWidget):

    def __init__(self, parent, email):
        super().__init__(parent=parent)
        self.email = email
        self.itemChanged.connect(self.getItemText)

    def getItemText()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        archive = contextMenu.addAction("Archive")
        recycle = contextMenu.addAction("Recycle")
        edit = contextMenu.addAction("Edit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == archive:
            self.Archive()
        elif action == recycle:
            self.Recycle()
        elif action == edit:
            self.Edit()

    def Archive(self):
        pass

    def Recycle(self):
        pass

    def Edit(self):
        items = self.selectedItems()
        for item in items:
            a = [item.text(0), item.text(1), item.text(2)]
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.editItem(item, 1)
            if len(item.text(1)) < 1:
                item.setText(1, a[1])
            self.itemChanged(item, 1)
            b = [item.text(0), item.text(1), item.text(2)]
            
            change_item_from_query(a, b, f"users/{self.email}/data.txt")


class Ui_Timerist(object):
    def setupUi(self, Timerist, sound, email, password):
        Timerist.setObjectName("Timerist")
        Timerist.resize(650, 550)
        Timerist.setWindowIcon(QtGui.QIcon('app_icon.ico'))

        self.TodoOptionsLayout = QHBoxLayout()
        self.TodoLayout = QVBoxLayout()

        self.MainWidget = QtWidgets.QWidget()

        self.opened = False
        self.tool_btn_size = QtCore.QSize(400, 400)
        self.tool_btn_size_2 = QtCore.QSize(50, 50)
        self.tool_btn_size_3 = QtCore.QSize(15, 15)
        self.sound = sound

        self.email = email
        self.password = password

        font = QtGui.QFont()
        font.setPointSize(20)
        self.todo_label = QtWidgets.QLabel(self.MainWidget)
        self.todo_label.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.todo_label.setFont(font)
        self.todo_label.setText("To Do List: ")
        self.treeWidget = QTreeWidgetCustom(self.MainWidget, self.email)
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.setMinimumHeight(300)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setHeaderLabels(["Date", "Task", "Status"])
        self.treeWidget.installEventFilter(Timerist)
        self.fillTreeWidget()


        self.refresh = QtWidgets.QPushButton("Refresh")
        self.refresh.setToolTip("Refresh Your Tasks")
        self.refresh.clicked.connect(self.Refresh)

        self.clear = QtWidgets.QPushButton("Clear")
        self.clear.setToolTip("Clear Your Tasks")
        self.clear.clicked.connect(self.Clear)

        self.pushButton = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 83, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(115, 260, 83, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(205, 260, 83, 28))
        self.pushButton_3.setText("Update")
        self.pushButton_3.setToolTip("Update The Status")
        self.pushButton_4 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(295, 260, 83, 28))
        self.pushButton_4.setText("View")
        self.pushButton_4.setToolTip("View the Timer")
        self.pushButton_3.clicked.connect(self.update_todo)
        self.pushButton_4.clicked.connect(self.view_todo)
        self.color_theme_btn = AnimatedToggle(checked_color="#4c5375")
        self.color_theme_btn.setMinimumSize(80, 10)
        self.color_theme_btn.setToolTip("Dark Mode: Off")
        self.color_theme_btn.stateChanged.connect(
            lambda x: self.dark_theme() if x else self.light_theme()
        )

        self.username = self.email.partition('@')[0]
        self.usernameLabel = QLabel(f"Hello, {self.username}")
        id = QFontDatabase.addApplicationFont("assets/Poppins-Medium.ttf")
        _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        _font = QFont(_fontstr, 20)
        self.usernameLabel.setFont(_font)

        self.viewCopyright = QtWidgets.QToolButton(self.MainWidget)
        self.viewCopyright.setIcon(QtGui.QIcon("images/copyright.png"))
        self.viewCopyright.setToolTip("View Copyright")
        self.viewCopyright.setIconSize(self.tool_btn_size_2)
        self.viewCopyright.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.viewCopyright.clicked.connect(self.CopyrightShow)

        self.logout = QtWidgets.QToolButton(self.MainWidget)
        self.logout.setIcon(QtGui.QIcon("images/logout.png"))
        self.logout.setToolTip("Logout")
        self.logout.setIconSize(self.tool_btn_size_2)
        self.logout.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.logout.clicked.connect(self.Logout)

        self.TodoOptionsLayout.addWidget(self.todo_label, alignment=Qt.AlignTop)
        self.TodoOptionsLayout.addWidget(self.pushButton, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_2, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_3, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_4, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.refresh, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.clear, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addStretch(8)
        self.TodoOptionsLayout.addWidget(self.usernameLabel, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.color_theme_btn, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.viewCopyright, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.logout, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addStretch()
        self.main_layout = QHBoxLayout()
        self.TodoContextMenu=QTabWidget()
        self.ArchivedTodos = QWidget()
        self.RecycledTodos = QWidget()
        self.TodoContextMenu.addTab(self.ArchivedTodos, "Archived")
        self.TodoContextMenu.setTabIcon(0, QIcon("images/open.png"))
        self.TodoContextMenu.addTab(self.RecycledTodos, "Recycled")
        self.TodoContextMenu.setTabIcon(1, QIcon("images/recycle.png"))
        qf = QFont()
        qf.setPointSize(15)
        self.TodoContextMenu.setFont(qf)
        self.TodoContextMenu.setIconSize(QtCore.QSize(32, 32))


        self.main_layout.addWidget(self.treeWidget, 50)
        self.main_layout.addWidget(self.TodoContextMenu, 50)
        self.TodoLayout.addLayout(self.TodoOptionsLayout)
        self.TodoLayout.addLayout(self.main_layout)
        self.TodoLayout.setStretch(1, 1)
        # Newest Layout for MainWidget
        self.MainWidget.setLayout(self.TodoLayout)
        self.scrollWidget = QtWidgets.QScrollArea()
        self.scrollWidget.setWidget(self.MainWidget)
        self.scrollWidget.setWidgetResizable(True)
        g = QVBoxLayout()
        g.addWidget(self.scrollWidget)
        Timerist.setLayout(g)



        self.retranslateUi(Timerist)
        QtCore.QMetaObject.connectSlotsByName(Timerist)


    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        archive = contextMenu.addAction("Archive")
        recycle = contextMenu.addAction("Recycle")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == archive:
            self.Archive()
        elif action == recycle:
            self.Recycle()
    
    def Logout(self):
        Timerist.destroy()
        QApplication.instance().exit(0)
        os.system("python -u Timerist.py")
            

    def Clear(self):
        ask = QtWidgets.QMessageBox.question(Timerist, "Are you sure ?", "Are you sure that you want to delete all of your todos ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if ask == QtWidgets.QMessageBox.Yes:
            file=open(f"users/{self.email}/data.txt", "w").close() # Erases all of the Data
            self.treeWidget.clear()
        else:
            pass
    
    def Refresh(self):
        self.fillTreeWidget()
        
    def fillTreeWidget(self):
        self.treeWidget.clear()
        file = open(f"users/{self.email}/data.txt", "r", encoding='utf-8')
        data = file.readlines()
        file.close()
        data = [line.replace('\n', '') for line in data]
        desired_lines = data[0::1]
        fov = slice_per(desired_lines, 3)
        for e in fov:
            if start_timer(e[0]) == 'yes' and e[2] == "Incomplete ❌": # Checks for overdue todos.
                edit_item(e, e[0], e[1], 'Overdue ⌛', f"users/{self.email}/data.txt")
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
            else:
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)


    def retranslateUi(self, Timerist):
        _translate = QtCore.QCoreApplication.translate
        Timerist.setWindowTitle(_translate("Timerist", "Timerist"))
        self.pushButton.setText(_translate("Timerist", "Add"))
        self.pushButton.setToolTip("Add A Task")
        self.pushButton.clicked.connect(self.add_todo)
        self.pushButton_2.setText(_translate("Timerist", "Remove"))
        self.pushButton_2.setToolTip("Remove A Task")
        self.pushButton_2.clicked.connect(self.remove_todo)

    def add_todo(self):
        add = AddTodoForm(Timerist, "Add Todo", self.treeWidget, user=self.email)
        add.show()

    def remove_todo(self):
        ask = QtWidgets.QMessageBox.question(Timerist, "Are you sure ?", "Are you sure that you want to delete these todo(s) ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if ask == QtWidgets.QMessageBox.Yes:
            items = self.treeWidget.selectedItems()
            if len(items) >= 0:
                for item in items:
                    item_text = [item.text(0), item.text(1), item.text(2)]
                    self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
                    delete_item_from_query(item_text, path=f'users/{self.email}/data.txt')
            else:
                QtWidgets.QMessageBox.warning(Timerist, "Select a document", "Please select a document so that an action can be completed.")
        else:
            pass

    def update_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text_prev = [item.text(0), item.text(1), item.text(2)]
            if item_text_prev[2] == "Incomplete ❌":
                item.setText(2, "Completed ✅")
                item_text_new = [item.text(0), item.text(1), item.text(2)]
                change_item_from_query(item_text_prev, item_text_new, f'users/{self.email}/data.txt')
            elif item_text_prev[2] == "Overdue ⌛":
                item.setText(2, "Completed ✅")
                item_text_new = [item.text(0), item.text(1), item.text(2)]
                change_item_from_query(item_text_prev, item_text_new, f'users/{self.email}/data.txt')
            elif item_text_prev[2] == "Completed ✅":
                item.setText(2, "Incomplete ❌")
                item_text_new = [item.text(0), item.text(1), item.text(2)]
                change_item_from_query(item_text_prev, item_text_new, f'users/{self.email}/data.txt')


    def view_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text = [item.text(0), item.text(1), item.text(2)]
            task_name = item_text[1]
            text_data = start_timer(item_text[0])
            completion_of_task = item_text[2]
            is_task_completed = False
            task_closed_id = "Task Closed ✅"
            task_time_is_up_id = "Time is Up!"
            if completion_of_task == "Completed ✅":
                is_task_completed = True
            else:
                is_task_completed = False
            if text_data == "yes":
                if is_task_completed == True:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_closed_id, taskToComplete=item_text[1], tree=self.treeWidget)
                    edit_todo_win.show()
                elif is_task_completed == False:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_time_is_up_id, self.sound, is_task_completed, taskToComplete=item_text[1], soundAlarm=True, tree=self.treeWidget)
                    edit_todo_win.show()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            else:
                if is_task_completed == True:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_closed_id, taskToComplete=item_text[1], tree=self.treeWidget)
                    edit_todo_win.show()
                elif is_task_completed == False:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", text_data, taskToComplete=item_text[1], soundAlarm=True, newText=item_text[0], sound=self.sound, isTimeShowing=True, prev_date=item_text[0], prev_status=item_text[2], tree=self.treeWidget)
                    edit_todo_win.show()

    def dark_theme(self):
        # Loads the Dark Theme mode for the app
        app.setStyleSheet(load_from_stylesheet("assets/dark-theme.qss"))
        self.color_theme_btn.setToolTip("Dark Mode: On")

    def light_theme(self):
        # Loads the Light Theme mode for the app
        app.setStyleSheet(load_from_stylesheet("assets/light-theme.qss"))
        self.color_theme_btn.setToolTip("Dark Mode: Off")

    def CopyrightShow(self):
        CopyrightWin = QtWidgets.QMainWindow(Timerist)
        CopyrightWin.resize(500, 350)
        CopyrightWin.setWindowTitle("Copyright")
        CopyrightWin.setWindowIcon(QIcon("images/copyright.png"))
        layout = QVBoxLayout()
        widget = QtWidgets.QWidget()
        copyright_text = QTextEdit(widget)
        copyright_text.setReadOnly(True)
        copyright_text.setCursor(Qt.PointingHandCursor)
        copyright_text.setText(open("assets/LICENSE", "r").read())
        copyright_font_id = QFontDatabase.addApplicationFont("assets/Segoe UI.ttf")
        copyright_text_font_family = QFontDatabase.applicationFontFamilies(copyright_font_id)[0]
        copyright_text_font = QFont(copyright_text_font_family, 13)
        copyright_text.setFont(copyright_text_font)
        layout.addWidget(copyright_text)
        widget.setLayout(layout)
        CopyrightWin.setCentralWidget(widget)
        CopyrightWin.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
app.setStyleSheet(load_from_stylesheet('assets/light-theme.qss'))
Timerist = QtWidgets.QDialog()
Timerist.setWindowFlags(Qt.WindowType.Window)
Timerist.setObjectName("Timerist")
ui = Ui_Timerist()