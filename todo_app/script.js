const addTodoButton = document.getElementById("add-todo");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");

addTodoButton.addEventListener("click", function() {
    const todoText = todoInput.value;
    if (todoText) {
        const li = document.createElement("li");
        li.textContent = todoText;
        const deleteIcon = document.createElement("span");
        deleteIcon.textContent = " 🗑️";
        deleteIcon.className = "delete-icon";
        deleteIcon.addEventListener("click", function() {
            todoList.removeChild(li);
        });
        li.appendChild(deleteIcon);
        todoList.appendChild(li);
        todoInput.value = "";
    }
});
