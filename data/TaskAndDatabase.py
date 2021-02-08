import sqlite3
from datetime import datetime


class Task:
    def __init__(self, title, content, dateShouldBeDone, creationDate):
        self.id = None
        self.creationDate = creationDate
        self.title = title
        self.content = content
        self.dateShouldBeDone = dateShouldBeDone
        self.isImportant = 0
        self.isDone = 0

    def setTaskImportant(self):
        self.isImportant = 1

    def setTaskDone(self):
        self.isDone = 1

    def returnATupleForAdding(self):
        taskTuple = (
            self.title,
            self.content,
            self.creationDate,
            self.dateShouldBeDone
        )
        return taskTuple

    def returnATupleForUpdating(self):
        taskTuple = (
            self.title,
            self.content,
            self.dateShouldBeDone,
            self.id
        )
        return taskTuple


class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("data.sqlite")
        self.cursor = self.db.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            isDone INTEGER DEFAULT 0,
            isImportant INTEGER DEFAULT 0,
            creationDate DATETIME,
            dateShouldBeDone DATETIME
        )
        """)

    def getAllTasksFromDatabase(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        if tasks:
            return tasks

    def addTaskToDataBase(self, task):
        taskTuple = task.returnATupleForAdding()
        self.cursor.execute("INSERT INTO tasks(title,content,creationDate,dateShouldBeDone) VALUES(?,?,?,?)", taskTuple)
        self.db.commit()

    def deleteA_TaskById(self, tasksId):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", tasksId)
        self.db.commit()

    def updateExistingTask(self, task):
        taskTuple = task.returnATupleForUpdating()
        self.cursor.execute("""UPDATE tasks SET 
                            title=?,content=?, dateShouldBeDone=?
                            WHERE id=? """, taskTuple)
        self.db.commit()

    def getTaskWithId(self, taskId):
        self.cursor.execute("SELECT * FROM tasks WHERE id=? ", (taskId,))
        tasks = self.cursor.fetchall()
        if tasks:
            return tasks[0]

    def setImportant(self, taskId):
        task = self.getTaskWithId(taskId)
        takIsImportant = task[4]
        if takIsImportant:
            self.cursor.execute("UPDATE tasks SET isImportant = 0 WHERE id=?", (taskId,))
        else:
            self.cursor.execute("UPDATE tasks SET isImportant = 1 WHERE id=?", (taskId,))
        self.db.commit()

    def setTaskDone(self, taskId):
        task = self.getTaskWithId(taskId)
        takIsImportant = task[3]
        if takIsImportant:
            self.cursor.execute("UPDATE tasks SET isDone = 0 WHERE id=?", (taskId,))
        else:
            self.cursor.execute("UPDATE tasks SET isDone = 1 WHERE id=?", (taskId,))
        self.db.commit()

    def removeTask(self, taskId):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskId,))
        self.db.commit()
