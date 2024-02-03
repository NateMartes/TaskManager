"""
Nathaniel Martes - TaskManager App using customtkinter, JSON, and time libraries
This app's purpose is to help users manging the many task one user may have throughout there day.
"""
from time import *
from customtkinter import *
from json import *
def main():
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = WINDOW_HEIGHT
    WHITE = "#FFFFFF"
    COLOR = "#0E0030"
    FONT = "Verdana"
    TASKSFILEPATH = "Task.json"
    WTASKFILEPATH = "WTask.json"
    Tasks = load(open(TASKSFILEPATH))
    
    def getTime():
        """
        changes timeLabel text to formatted date and time every
        1000 MS (1 second) using python's time module.
        """
        timeLabel.configure(text=strftime('%I:%M:%S %p'))
        app.after(1000, getTime)
    

    def submitTask(taskName: str):
        Tasks = load(open(TASKSFILEPATH))
        """
        checks if task exist in Task.json or if task is an empty str.
        """
        if taskName == "":
            resultLabel.configure(text="*All Task Must Have Names*")
        elif len(taskName) > 30:
            resultLabel.configure(text="*Task Name Max length is 30*")
        elif taskName in Tasks.keys():
            resultLabel.configure(text="*Task Already Exists*")
        else:
            subtask0 = getSubTasksNames(0)
            subtask1 = getSubTasksNames(1)
            subtask2 = getSubTasksNames(2)
            if (len(subtask0) > 30) or (len(subtask0) > 30) or (len(subtask0) > 30):
                resultLabel.configure(text="*Subtask Name Max length is 30*")
                return 0
            Task = {taskName : [subtask0, subtask1, subtask2]}
            resultLabel.configure(text="*Task Added!*")
            return addTaskToList(Task, taskName)
        
    def addTaskToList(formattedTask: dict, taskName):
        """
        adds task to Task.json then creates (CTKButtons) to display.
        Save CTKButtons to list of CTKButtons objects.
        """
        with open(TASKSFILEPATH) as Tasks:
            updatedTasks = load(Tasks)
            updatedTasks.update(formattedTask)
        with open(TASKSFILEPATH, 'w') as Tasks:
            dump(updatedTasks, Tasks,  indent=2)
        task = CTkButton(master=taskList, text=taskName, font=(FONT, 15), text_color=WHITE, width=200, command= lambda: addTaskToMain(taskName))
        task.pack(side=TOP)
        allTaskInGUIList.append(task)
    def loadTaskList():
        """
        Takes tasks from Task.json and creates CTKButtons(s) to display. 
        Save CTKButtons to list of CTKLabel objects.
        """
        taskObjects = []
        for taskName in Tasks.keys():
            task = CTkButton(master=taskList, text=taskName, font=(FONT, 15), text_color=WHITE, width=200,  command= lambda name = taskName : addTaskToMain(name))
            task.pack(side=TOP)
            taskObjects.append(task)
        return taskObjects
    
    def loadSubTask():
        """
        when CTkSwitch is in "on" state on AddTasksTab, load 3 Subtasks CTKentries and save to list of subtask CTKentries.
        else, remove CTKentries for subtasks
        """
        if subTaskSwitchVar.get() == "on":
            enterSubTaskNameEntry0 = CTkEntry(master=taskListFrame, placeholder_text="Subtask",font=(FONT,25), width=275, border_color=COLOR)
            enterSubTaskNameEntry0.pack(pady=10)
            SubTasksList.append(enterSubTaskNameEntry0)

            enterSubTaskNameEntry1 = CTkEntry(master=taskListFrame, placeholder_text="Subtask",font=(FONT,25), width=275, border_color=COLOR)
            enterSubTaskNameEntry1.pack(pady=10)
            SubTasksList.append(enterSubTaskNameEntry1)

            enterSubTaskNameEntry2 = CTkEntry(master=taskListFrame, placeholder_text="Subtask",font=(FONT,25), width=275, border_color=COLOR)
            enterSubTaskNameEntry2.pack(pady=10)
            SubTasksList.append(enterSubTaskNameEntry2)
        else:
            for i in SubTasksList:
                i.destroy()
            SubTasksList.clear()

    def getSubTasksNames(index):
        """
        returns subtask according to index recived. If no subtask exist, return empty str
        
        """
        if len(SubTasksList) > 1:
            return SubTasksList[index].get()
        return ""
    
    def addTaskToMain(taskName):
        """
        takes task name from buttton in taskList and changes workingTask CTKLabel name
        adds CTKButton to taskList 
        """
        oldTaskName = workingTask.cget("text")
        workingTask.configure(text=taskName)
        workingTask.configure(fg_color=COLOR)
        finishTaskBtn.configure(fg_color=COLOR)
        finishTaskBtn.configure(state=NORMAL)
        for i in allTaskInGUIList:
            if i.cget("text") == taskName:
                workingTaskObj.clear()
                workingTaskObj.append(i)
                allTaskInGUIList.remove(i)
                i.destroy()
                if oldTaskName != "":
                    task = CTkButton(master=taskList, text=oldTaskName, font=(FONT, 15), width=200, text_color=WHITE, \
                                     command= lambda: addTaskToMain(oldTaskName))
                    task.pack(side=TOP)
                    allTaskInGUIList.append(task)
                    oldTask = {oldTaskName : load(open(WTASKFILEPATH))[oldTaskName]}
                    saveWorkingTask(taskName, oldTask)
                    break
                saveWorkingTask(taskName)
                break

    def saveWorkingTask(taskName, oldTask=""):
        """
        formats workingTask and save task to WTask.json
        removes working task from Task.json
        """
        Tasks = load(open(TASKSFILEPATH))
        for task in Tasks.keys():
            if task == taskName:
                workingTaskFormatted = {taskName : Tasks[task]}
                print(Tasks[task])
                finishTaskBtn.configure(text="")
                
                #set first subtask if any
                subtasks = Tasks[task]
                for i in range(len(subtasks)):
                    if subtasks[i] != "":
                        finishTaskBtn.configure(text=subtasks[i])
                        break
                    elif subtasks[i]=="" and i==2:
                        finishTaskBtn.configure(text="Finish Task")

                with open(WTASKFILEPATH, 'w') as WTaskFile:
                    dump(workingTaskFormatted, WTaskFile,  indent=2)
                break
        Tasks.pop(task)
        updatedTasks = Tasks

        if oldTask !="":
            with open(TASKSFILEPATH) as Tasks:
                updatedTasks.update(oldTask)
        with open(TASKSFILEPATH, 'w') as Tasks:
            dump(updatedTasks, Tasks,  indent=2) 
        
    def loadWorkingTask():
        """
        loads WorkingTask from WTask.json into workingTask text
        """
        WorkingTask = load(open(WTASKFILEPATH))
        if WorkingTask:
            workingTask.configure(text=list(WorkingTask.keys())[0])
            workingTask.configure(fg_color=COLOR)
            finishTaskBtn.configure(fg_color=COLOR)
            finishTaskBtn.configure(state=NORMAL)
            subtasks = list(WorkingTask.values())[0]
            for i in range(len(subtasks)):
                if subtasks[i] != "":
                    finishTaskBtn.configure(text=subtasks[i])
                    break
                elif subtasks[i]=="" and i==2:
                    finishTaskBtn.configure(text="Finish Task")
    def CurrentSubtask(Task):
        """
        change Subtasks user is working on. once finishTaskBtn is pressed, current subtask is changed to empty str in file.
        once all subtask are empty str, finishTaskBtn will no longer display subtasks
        """
        if finishTaskBtn.cget("text") == "Finish Task":
            removeWorkingTask(Task)
            return 0
        taskName = list(Task.keys())[0]
        if workingTask.cget("text") == taskName:
            subtasks = list(Task.values())[0]
            for i in range(len(subtasks)):
                if subtasks[i] != "":
                    newSubTask = subtasks
                    newSubTask[i] = ""
                    #check if next more subtask exist. if so, change set current subtask to subtask[i+1]
                    try: 
                        finishTaskBtn.configure(text=subtasks[i+1])
                    except:
                        finishTaskBtn.configure(text="Finish Task")
                    with open(WTASKFILEPATH, 'w') as WTaskFile:
                        dump({taskName : newSubTask}, WTaskFile,  indent=2)
                    return 0

    def removeWorkingTask(Task):
        """
        reconfigures workingTask and finishTaskBtn to defualt and Clears WTask.json
        """
        workingTask.configure(fg_color="transparent")
        finishTaskBtn.configure(fg_color="transparent")
        workingTask.configure(text="")
        finishTaskBtn.configure(text="")
        finishTaskBtn.configure(state=DISABLED)

        with open(WTASKFILEPATH, 'r') as WTaskFile:
            WorkingTask = load(WTaskFile)
            print(Task)
            del WorkingTask[list(Task.keys())[0]]
        with open(WTASKFILEPATH, 'w') as WTaskFile:
            dump(WorkingTask, WTaskFile,  indent=2)
#Main
    app = CTk()
    app.geometry(f"{WINDOW_HEIGHT}x{WINDOW_WIDTH}")
    app._set_appearance_mode("system")
    app.title("Task Manager")
    set_default_color_theme("NightTrain.json")
    frame = CTkFrame(master=app, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    frame.pack(expand=True, fill=BOTH, anchor=CENTER)
    taskListFrame = CTkFrame(master=frame, corner_radius=10, height=400, width=730)
    taskListFrame.pack(expand=True, side=BOTTOM)
    timeLabel = CTkLabel(master=frame, text="00:00", font=(FONT, 25), fg_color="transparent")
    timeLabel.pack(expand=False, side=LEFT, pady=10, padx=10, anchor="nw")
    getTime()

    workingTaskFrame = CTkFrame(master=taskListFrame, width=200, fg_color="#000e1e")
    workingTaskFrame.pack(expand=True, fill=Y)

    workingTask = CTkLabel(master=workingTaskFrame, text="", font=(FONT, 20),height=50, width=50, \
                           corner_radius=10, fg_color="transparent", text_color=WHITE)
    workingTask.pack(padx=5, side=LEFT)
    workingTask.configure()
    workingTaskObj=[workingTask]
    finishTaskBtn = CTkButton(master=workingTaskFrame, text="", font=(FONT, 15),height=50, width=50, \
                           corner_radius=10, fg_color="transparent", text_color=WHITE, command=lambda: \
                            CurrentSubtask(load(open(WTASKFILEPATH))))
    finishTaskBtn.pack(side=LEFT)
    finishTaskBtn.configure()
    finishTaskBtn.configure(state=DISABLED)
    loadWorkingTask()

    taskList = CTkScrollableFrame(master=taskListFrame, height=250, width=300, corner_radius=10, fg_color="transparent")
    taskList.pack(expand=True, fill=BOTH,side=LEFT)
    taskListLabel = CTkLabel(master=taskList, text="All Tasks:", font=(FONT, 15))
    taskListLabel.pack(expand=True, anchor="nw")
    allTaskInGUIList = loadTaskList()

    subTaskSwitchVar = StringVar(value="off")
    subTaskSwitch = CTkSwitch(master=taskListFrame, text="Use Subtasks", command=loadSubTask,
                                variable=subTaskSwitchVar, onvalue="on", offvalue="off")
    subTaskSwitch.pack(expand=True,side=RIGHT, padx=5, pady=5, anchor="ne")

    enterTaskNameEntry = CTkEntry(master=taskListFrame, placeholder_text="Enter Task Name",font=(FONT,25), width=275, border_color=COLOR)
    enterTaskNameEntry.pack(padx=10, pady=10, anchor="n")
        
    SubTasksList = []

    submitTaskButton = CTkButton(master=taskListFrame, text="Add",font=(FONT,25), command=lambda: 
                                    submitTask(enterTaskNameEntry.get()))
    submitTaskButton.pack(pady=80,side="bottom")

    resultLabel = CTkLabel(master=taskListFrame, text="", font=(FONT,15, "bold"))
    resultLabel.pack(side="bottom")

    app.mainloop()

if __name__ == "__main__":
    main()