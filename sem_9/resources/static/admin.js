const
    taskSelector = document.getElementById("taskSelector"),
    addBtn = document.getElementById("addBtn"),
    editBtn = document.getElementById("editBtn"),
    delBtn = document.getElementById("delBtn")


function fillTaskSelector() {
    axios.get("/todo")
        .then(({data: {tasks}}) => {
            taskSelector.length = 0
            for (let i = 0; i < tasks.length; i++) {
                let {id, text} = tasks[i]
                taskSelector.add(new Option(text, id))
            }
    })
}

function addTask() {
    let text = prompt("Input task:", "")
    axios.post("/todo", {
        text: text
    }).then(({data: {id, text}}) => {
        taskSelector.add(new Option(text, id))
        taskSelector.selectedIndex = taskSelector.length - 1
    })
}

function editTask() {
    let taskId = taskSelector.value
    let text = prompt("Input task:", "")
    axios.put("/todo", {
        text: text
    }, {
        params: {id: taskId}
    }).then(response => {
        taskSelector[taskSelector.selectedIndex].text = text
    })
}

function delTask() {
    let taskId = taskSelector.value
    let accepted = confirm(`Are you sure, delete task  ${taskSelector[taskSelector.selectedIndex].text}?`)
    if (accepted) {
        axios.delete("/todo", {
            params: {id: taskId}
        }).then(response => {
            taskSelector.options[taskSelector.selectedIndex] = undefined
        })
    }
}


addBtn.addEventListener("click", addTask)
editBtn.addEventListener("click", editTask)
delBtn.addEventListener("click", delTask)


fillTaskSelector()
