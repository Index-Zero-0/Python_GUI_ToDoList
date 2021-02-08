from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from datetime import datetime
from data.TaskAndDatabase import *


class Ui(QtWidgets.QMainWindow):
    # The style of the active button
    buttonActiveStyle = "QPushButton{border:2px solid #ddd;color:#fff;background-color:#324048}"
    # The style of buttons in the navbar
    buttonStyle = "QPushButton{border:2px solid #ddd;color:#000;background-color:#ddd}" \
                  "QPushButton:hover{background-color:#324048}"
    # Navbar buttons will be stored in this list
    navbarButtons = []

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.database = DataBase()
        self.activeButton = self.btn_Today
        self.currentPage = None
        self.showTodayTasks()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1247, 804)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        # Add a vertical layout ot centralwidget
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(100, 20, 100, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(50)

        # The Window is divided to two different section
        # The top one which is the navbar (today, other , mostimportant, done and Add button)
        # And the bottom section where will tasks will be displayed

        self.mainFrameTop = QtWidgets.QFrame(self.centralwidget)
        self.mainFrameTop.setStyleSheet("border:none;background-color:#324048;")
        self.mainFrameTop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrameTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrameTop.setObjectName("mainFrameTop")
        self.mainFrameTop.setMinimumHeight(50)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.mainFrameTop)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Buttton today to show today tasks
        self.btn_Today = QtWidgets.QPushButton(self.mainFrameTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Today.sizePolicy().hasHeightForWidth())
        self.btn_Today.setSizePolicy(sizePolicy)
        self.btn_Today.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.btn_Today.setFont(font)
        self.btn_Today.setStyleSheet(self.buttonStyle)
        self.btn_Today.clicked.connect(self.showTodayTasks)
        self.btn_Today.setCursor(QtCore.Qt.PointingHandCursor)
        self.horizontalLayout.addWidget(self.btn_Today)
        self.navbarButtons.append(self.btn_Today)
        self.navbarButtons.append(self.btn_Today)

        # button other: if task is not for today by clicking on this button we will see it
        self.btn_Other = QtWidgets.QPushButton(self.mainFrameTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Other.sizePolicy().hasHeightForWidth())
        self.btn_Other.setSizePolicy(sizePolicy)
        self.btn_Other.setMinimumSize(QtCore.QSize(150, 0))
        self.btn_Other.setFont(font)
        self.btn_Other.setStyleSheet(self.buttonStyle)
        self.btn_Other.setObjectName("pushButton_2")
        self.btn_Other.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_Other.clicked.connect(self.showOtherTaskThenToday)
        self.navbarButtons.append(self.btn_Other)
        self.horizontalLayout.addWidget(self.btn_Other)
        self.navbarButtons.append(self.btn_Other)

        # Button to show most important tasks
        self.btn_MostImportant = QtWidgets.QPushButton(self.mainFrameTop)
        self.btn_MostImportant.setSizePolicy(sizePolicy)
        self.btn_MostImportant.setMinimumSize(QtCore.QSize(150, 0))
        self.btn_MostImportant.setFont(font)
        self.btn_MostImportant.setStyleSheet(self.buttonStyle)
        self.btn_MostImportant.setObjectName("btn_MostImportant")
        self.btn_MostImportant.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_MostImportant.clicked.connect(self.showImportantTasks)
        self.navbarButtons.append(self.btn_MostImportant)
        self.horizontalLayout.addWidget(self.btn_MostImportant)
        self.navbarButtons.append(self.btn_MostImportant)

        # Button to show tasks which are done
        self.btn_Done = QtWidgets.QPushButton(self.mainFrameTop)
        self.btn_Done.setSizePolicy(sizePolicy)
        self.btn_Done.setMinimumSize(QtCore.QSize(150, 0))
        self.btn_Done.setFont(font)
        self.btn_Done.setStyleSheet(self.buttonStyle)
        self.btn_Done.setObjectName("btn_Done")
        self.btn_Done.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_Done.clicked.connect(self.showDoneTasks)
        self.navbarButtons.append(self.btn_Done)
        self.horizontalLayout.addWidget(self.btn_Done)
        self.navbarButtons.append(self.btn_Done)

        spacerItem = QtWidgets.QSpacerItem(444, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        # Add a new task
        self.btn_Add = QtWidgets.QPushButton(self.mainFrameTop)
        self.btn_Add.setSizePolicy(sizePolicy)
        self.btn_Add.setMinimumSize(QtCore.QSize(80, 0))
        self.btn_Add.setFont(font)
        self.btn_Add.setStyleSheet("QPushButton{border:2px solid #ddd;color:#000;background-color:#ddd}")
        self.btn_Add.setObjectName("btn_Add")
        self.btn_Add.setIcon(QtGui.QIcon("Images/add.png"))
        self.btn_Add.setIconSize(QtCore.QSize(30, 30))
        self.btn_Add.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_Add.clicked.connect(self.showAddPage)
        self.horizontalLayout.addWidget(self.btn_Add)

        # Add top section to centralwidgets layout
        self.verticalLayout.addWidget(self.mainFrameTop)

        # This represent the bottom part of main frame
        # Add a scroll area to display the specific tasks on it
        self.mainFrameBottom = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainFrameBottom.sizePolicy().hasHeightForWidth())
        self.mainFrameBottom.setSizePolicy(sizePolicy)
        self.mainFrameBottom.setStyleSheet("border:none;")
        self.mainFrameBottom.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.mainFrameBottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrameBottom.setObjectName("mainFrameBottom")

        self.mainFrameBottomLayout = QtWidgets.QVBoxLayout(self.mainFrameBottom)
        self.mainFrameBottomLayout.setContentsMargins(5, 0, 0, 0)

        self.verticalLayout.addWidget(self.mainFrameBottom)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 15)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1247, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)

    def showTodayTasks(self):
        if self.deleteMainFrameBottomChild("Today"):
            self.activeButton = self.btn_Today
            self.currentPage = "Today"
            self.createNewScrollArea()
            self.getTasksFromDatabase("Today")

    def showOtherTaskThenToday(self):
        if self.deleteMainFrameBottomChild("Other"):
            self.activeButton = self.btn_Other
            self.currentPage = "Other"
            self.createNewScrollArea()
            self.getTasksFromDatabase("Other")

    def showImportantTasks(self):
        if self.deleteMainFrameBottomChild("Important"):
            self.activeButton = self.btn_MostImportant
            self.currentPage = "Important"
            self.createNewScrollArea()
            self.getTasksFromDatabase("Important")

    def showDoneTasks(self):
        if self.deleteMainFrameBottomChild("Done"):
            self.activeButton = self.btn_Done
            self.currentPage = "Done"
            self.createNewScrollArea()
            self.getTasksFromDatabase("Done")

    def createNewScrollArea(self):
        self.scrollArea = QtWidgets.QScrollArea(self.mainFrameBottom)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("border:none;")

        self.scrollAreaWidgetContents = QtWidgets.QFrame()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.scrollLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)

        self.scrollLayout.setObjectName("formLayout")

        self.changeButtonStyle()

    def deleteMainFrameBottomChild(self, page=None):
        if self.currentPage != page:
            for child in self.mainFrameBottom.children():
                if child != self.mainFrameBottomLayout:
                    child.deleteLater()
            return True
        return False

    def showAddPage(self, task=None):
        if self.deleteMainFrameBottomChild("Add"):
            self.currentPage = "Add"
            data = {"title": "", "content": "", "dateShouldBeDone": ""}
            if task:
                data["id"] = task[0]
                data["title"] = task[1]
                data["content"] = task[2]
                data["dateShouldBeDone"] = datetime.strptime(task[-1], "%a %b %d %Y").date()
                self.currentPage = "UPDATE"
                self.setupAddPage(data, update=True)
            else:
                today = datetime.today().date()
                data["dateShouldBeDone"] = today
                self.setupAddPage(data)

    def setupAddPage(self, task, update=False):
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        addFrame = QtWidgets.QFrame(self.mainFrameBottom)
        addFrame.setStyleSheet("border:none;")
        addFrame.setObjectName("mainFrameBottom")
        addFrameLayout = QtWidgets.QFormLayout(addFrame)
        addFrameLayout.setLabelAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        addFrameLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        addFrameLayout.setContentsMargins(10, 50, 10, 10)
        addFrameLayout.setSpacing(30)
        addFrameLayout.setObjectName("horizontalLayout")

        lblTitle = QtWidgets.QLabel(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lblTitle.sizePolicy().hasHeightForWidth())
        lblTitle.setSizePolicy(sizePolicy)
        lblTitle.setMinimumSize(QtCore.QSize(50, 0))
        lblTitle.setBaseSize(QtCore.QSize(50, 0))
        lblTitle.setFont(font)
        lblTitle.setObjectName("label")
        lblTitle.setText("Title")
        addFrameLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, lblTitle)
        self.inputTitle = QtWidgets.QLineEdit(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTitle.sizePolicy().hasHeightForWidth())
        self.inputTitle.setSizePolicy(sizePolicy)
        self.inputTitle.setMinimumSize(QtCore.QSize(700, 40))
        font.setPointSize(10)
        font.setBold(False)
        self.inputTitle.setFont(font)
        self.inputTitle.setStyleSheet("border:1px solid #aaa;border-radius:3px;")
        self.inputTitle.setText(task["title"])
        addFrameLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inputTitle)
        lblDescription = QtWidgets.QLabel(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lblDescription.sizePolicy().hasHeightForWidth())
        lblDescription.setSizePolicy(sizePolicy)
        lblDescription.setMinimumSize(QtCore.QSize(50, 250))
        lblDescription.setBaseSize(QtCore.QSize(50, 0))
        lblDescription.setText("Description")
        font.setPointSize(12)
        font.setBold(True)
        lblDescription.setFont(font)
        lblDescription.setObjectName("label_2")
        addFrameLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, lblDescription)
        self.inputDescription = QtWidgets.QTextEdit(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputDescription.sizePolicy().hasHeightForWidth())
        self.inputDescription.setSizePolicy(sizePolicy)
        self.inputDescription.setMinimumSize(QtCore.QSize(700, 250))
        font.setBold(False)
        font.setPointSize(10)
        self.inputDescription.setFont(font)
        self.inputDescription.setStyleSheet("border:1px solid #aaa;border-radius:3px;")
        self.inputDescription.setText(task["content"])
        addFrameLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inputDescription)
        lblDate = QtWidgets.QLabel(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lblDate.sizePolicy().hasHeightForWidth())
        lblDate.setSizePolicy(sizePolicy)
        lblDate.setMinimumSize(QtCore.QSize(50, 0))
        lblDate.setBaseSize(QtCore.QSize(50, 0))
        font.setPointSize(12)
        font.setBold(True)
        lblDate.setFont(font)
        lblDate.setObjectName("label_3")
        lblDate.setText("Date")
        addFrameLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, lblDate)

        self.inputDate = QtWidgets.QCalendarWidget(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputDate.sizePolicy().hasHeightForWidth())
        self.inputDate.setSizePolicy(sizePolicy)
        self.inputDate.setMinimumSize(QtCore.QSize(331, 183))
        self.inputDate.setStyleSheet("QCalendarWidget QAbstractItemView{"
                                     "background-color:#72bcdb;}"
                                     "QCalendarWidget  QWidget#qt_calendar_navigationbar{"
                                     "background-color : #3097bf;color:black;}")
        self.inputDate.setSelectedDate(task["dateShouldBeDone"])
        addFrameLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.inputDate)

        frameAddButton = QtWidgets.QFrame(addFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frameAddButton.sizePolicy().hasHeightForWidth())
        frameAddButton.setSizePolicy(sizePolicy)
        frameAddButton.setMinimumSize(QtCore.QSize(700, 100))
        frameAddButton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frameAddButton.setFrameShadow(QtWidgets.QFrame.Raised)
        btnAdd = QtWidgets.QPushButton(frameAddButton)
        btnAdd.setGeometry(QtCore.QRect(240, 20, 191, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btnAdd.sizePolicy().hasHeightForWidth())
        btnAdd.setSizePolicy(sizePolicy)
        btnAdd.setMinimumSize(QtCore.QSize(150, 30))
        btnAdd.setFont(font)
        btnAdd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnAdd.setStyleSheet("color:#fff;background-color:#324048;border-radius:3px;")
        btnAdd.setObjectName("pushButton_5")
        if not update:
            btnAdd.setText("Add")
            btnAdd.clicked.connect(self.saveTheTaskIntoDatabase)
        else:
            btnAdd.setText("Update")
            btnAdd.clicked.connect(lambda: self.updateTask(task["id"]))
        addFrameLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, frameAddButton)
        self.mainFrameBottomLayout.addWidget(addFrame)

    def saveTheTaskIntoDatabase(self):
        task = self.getInputFromFieldsInAddPage()
        self.database.addTaskToDataBase(task)
        self.currentPage = "Today"
        self.activeButton = self.btn_Today
        self.reloadCurrentPage()

    def updateTask(self, taskId):
        task = self.getInputFromFieldsInAddPage()
        task.id = taskId
        self.database.updateExistingTask(task)
        self.reloadCurrentPage()

    def getInputFromFieldsInAddPage(self):
        title = self.inputTitle.text()
        content = self.inputDescription.toPlainText()
        dateShouldBeDone = self.inputDate.selectedDate().toString()
        dateItIsCreated = datetime.today().date()
        task = Task(title, content, dateShouldBeDone, dateItIsCreated)
        return task

    def setATaskAsImportant(self, taskId):
        self.database.setImportant(taskId)
        self.reloadCurrentPage()

    def taskIsDone(self, taskId):
        self.database.setTaskDone(taskId)
        self.reloadCurrentPage()

    def deleteTask(self, taskId):
        self.database.removeTask(taskId)
        self.reloadCurrentPage()

    def reloadCurrentPage(self):
        self.deleteMainFrameBottomChild()
        self.createNewScrollArea()
        self.getTasksFromDatabase(self.currentPage)

    def getTasksFromDatabase(self, page):
        tasks = self.database.getAllTasksFromDatabase()
        if tasks:
            if page == "Today":
                self.showPage_Today(tasks)
            elif page == "Other":
                self.showPage_Other(tasks)
            elif page == "Important":
                self.showPage_Important(tasks)
            elif page == "Done":
                self.showPage_Done(tasks)
        else:
            self.showEmptyPage()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.mainFrameBottomLayout.addWidget(self.scrollArea)

    def showPage_Today(self, tasks):
        taskNumberForScrollLayout = 0
        todayDate = datetime.today().date()
        pageIsEmpty = True
        for task in tasks:
            dateShouldBeDone = datetime.strptime(task[-1], "%a %b %d %Y").date()
            if dateShouldBeDone == todayDate and not task[3]:
                pageIsEmpty = False
                self.showTaskInUI(task, taskNumberForScrollLayout)
                taskNumberForScrollLayout += 1

        if pageIsEmpty:
            self.showEmptyPage()



    def showPage_Other(self, tasks):
        taskNumberForScrollLayout = 0
        todayDate = datetime.today().date()
        pageIsEmpty = True
        for task in tasks:
            dateShouldBeDone = datetime.strptime(task[-1], "%a %b %d %Y").date()
            if dateShouldBeDone > todayDate and not task[3]:
                pageIsEmpty = False
                self.showTaskInUI(task, taskNumberForScrollLayout)
                taskNumberForScrollLayout += 1

        if pageIsEmpty:
            self.showEmptyPage()

    def showPage_Important(self, tasks):
        taskNumberForScrollLayout = 0
        pageIsEmpty = True
        for task in tasks:
            if task[4]:
                self.showTaskInUI(task, taskNumberForScrollLayout)
                pageIsEmpty = False
                taskNumberForScrollLayout += 1

        if pageIsEmpty:
            self.showEmptyPage()

    def showPage_Done(self, tasks):
        taskNumberForScrollLayout = 0
        pageIsEmpty = True
        for task in tasks:
            if task[3]:
                self.showTaskInUI(task, taskNumberForScrollLayout)
                pageIsEmpty = False
                taskNumberForScrollLayout += 1

        if pageIsEmpty:
            self.showEmptyPage()

    def showTaskInUI(self, task, taskNumber):
        font = QtGui.QFont()
        # Frame which task's info will be shown in. Actually one taskFrame means one task.
        # In taskFrame will be stored:
        # Button to see more info about the task, button to delete and set to done list , if a task is important
        # And the datum of the task
        taskFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(taskFrame.sizePolicy().hasHeightForWidth())
        taskFrame.setSizePolicy(sizePolicy)
        taskFrame.setMinimumSize(QtCore.QSize(1000, 51))
        taskFrame.setStyleSheet("QFrame{border-radius:5px;border:1px solid #888;}"
                                "QFrame:hover{border:2px solid #324048;}"
                                "QPushButton{color:black}")
        taskFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        taskFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        taskFrame.setObjectName("ToDoFrame_2")

        btnSetTaskAsImportant = QtWidgets.QPushButton(taskFrame)
        btnSetTaskAsImportant.setGeometry(QtCore.QRect(0, 0, 50, 51))
        font.setFamily("Verdana")
        font.setPointSize(10)
        btnSetTaskAsImportant.setFont(font)
        btnSetTaskAsImportant.setIcon(QtGui.QIcon('Images/empty_star.png'))
        # task[4] == isImportant (a column in tasks table)
        if task[4]:
            btnSetTaskAsImportant.setIcon(QtGui.QIcon('Images/star.png'))
        btnSetTaskAsImportant.setIconSize(QtCore.QSize(20, 20))
        btnSetTaskAsImportant.setText("")
        btnSetTaskAsImportant.setStyleSheet("QPushButton{border:none;margin-right:4;}"
                                            "QPushButton::hover{background-color:#324048;}")
        btnSetTaskAsImportant.setCursor(QtCore.Qt.PointingHandCursor)
        btnSetTaskAsImportant.clicked.connect(lambda: self.setATaskAsImportant(task[0]))
        btnSetTaskAsImportant.setObjectName(f"task_")

        # Button to show details of the task
        getTasksDetailsAndShowThem = QtWidgets.QPushButton(taskFrame)
        getTasksDetailsAndShowThem.setGeometry(QtCore.QRect(50, 0, 731, 51))
        font.setPointSize(10)
        getTasksDetailsAndShowThem.setFont(font)
        getTasksDetailsAndShowThem.setText(task[1])
        getTasksDetailsAndShowThem.setStyleSheet("QPushButton{text-align:left;border:none;}")
        getTasksDetailsAndShowThem.clicked.connect(lambda: self.showAddPage(task))

        # Button to remove the task
        btnRemoveTask = QtWidgets.QPushButton(taskFrame)
        btnRemoveTask.setGeometry(QtCore.QRect(910, 10, 31, 31))
        btnRemoveTask.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnRemoveTask.setStyleSheet("border-radius:15;border:none;")
        btnRemoveTask.setText("")
        btnRemoveTask.setIcon(QtGui.QIcon('Images/remove.png'))
        btnRemoveTask.setIconSize(QtCore.QSize(28, 28))
        btnRemoveTask.setCheckable(False)
        btnRemoveTask.setObjectName(f"task-{task[0]}")
        btnRemoveTask.clicked.connect(lambda: self.deleteTask(task[0]))

        # Button to set the task done
        btnSetDone = QtWidgets.QPushButton(taskFrame)
        btnSetDone.setGeometry(QtCore.QRect(950, 10, 31, 31))
        btnSetDone.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnSetDone.setStyleSheet("border-radius:15;border:none;")
        btnSetDone.setText("")
        btnSetDone.setIcon(QtGui.QIcon("Images/check.png"))
        btnSetDone.setIconSize(QtCore.QSize(28, 28))
        btnSetDone.clicked.connect(lambda: self.taskIsDone(task[0]))
        if self.currentPage == "Done":
            btnSetDone.deleteLater()
            btnRemoveTask.setGeometry(QtCore.QRect(950, 10, 31, 31))
        labelTasksDatum = QtWidgets.QLabel(taskFrame)
        labelTasksDatum.setGeometry(QtCore.QRect(740, 0, 151, 51))
        font.setPointSize(9)
        labelTasksDatum.setFont(font)
        labelTasksDatum.setStyleSheet("border:none;")
        labelTasksDatum.setAlignment(QtCore.Qt.AlignCenter)
        labelTasksDatum.setText(task[-1])
        self.scrollLayout.setWidget(taskNumber, QtWidgets.QFormLayout.LabelRole, taskFrame)

    def showEmptyPage(self):
        self.scrollLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        taskFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(taskFrame.sizePolicy().hasHeightForWidth())
        taskFrame.setSizePolicy(sizePolicy)
        taskFrame.setMinimumSize(QtCore.QSize(600, 600))
        taskFrame.setObjectName("ToDoFrame_2")
        emptyLabel = QtWidgets.QLabel(taskFrame)
        emptyLabel.setMinimumSize(QtCore.QSize(600, 500))
        emptyLabel.setStyleSheet("background-image: url(Images/empty.png);background-repeat:no-repeat;")
        self.scrollLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, taskFrame)

    def changeButtonStyle(self):
        for button in self.navbarButtons:
            if button == self.activeButton:
                button.setStyleSheet(self.buttonActiveStyle)
            else:
                button.setStyleSheet(self.buttonStyle)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_Today.setText(_translate("MainWindow", "Today"))
        self.btn_Other.setText(_translate("MainWindow", "Other"))
        self.btn_MostImportant.setText(_translate("MainWindow", "Most important"))
        self.btn_Done.setText(_translate("MainWindow", "Done"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
