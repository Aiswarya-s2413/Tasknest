document.addEventListener("DOMContentLoaded", function () {
    fetchTasks();
    setupModal();
    setupFormSubmit();
});

// Fetch tasks
function fetchTasks() {
    console.log('Document cookies:', document.cookie);
    fetch("https://3.27.123.53.sslp.io/api/tasks/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include", 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }
        return response.json();
    })
    .then(data => {
        displayTasks(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Display tasks
function displayTasks(tasks) {
    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    if (tasks.length === 0) {
        taskList.innerHTML = `
            <li class="task-item text-center" style="border: 2px dashed #e1e5e9;">
                <div class="task-content">
                    <h3 style="color: #999; margin-bottom: 1rem;">No tasks available</h3>
                    <p style="color: #666;">Create your first task to get started!</p>
                </div>
            </li>
        `;
        return;
    }

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = `task-item ${task.is_completed ? 'completed' : ''}`;
        
        const dueDate = task.due_date ? new Date(task.due_date) : null;
        const scheduledTime = task.scheduled_time ? new Date(task.scheduled_time) : null;
        
        li.innerHTML = `
            <div class="task-priority-indicator priority-${task.priority || 'medium'}"></div>
            <div class="task-content">
                <h3 class="task-title">${task.title}</h3>
                <p class="task-description">${task.description || 'No description provided'}</p>
                <div class="task-meta">
                    <span><strong>Due:</strong> ${dueDate ? dueDate.toLocaleDateString() + ' ' + dueDate.toLocaleTimeString() : 'Not set'}</span>
                    <span><strong>Priority:</strong> ${(task.priority || 'medium').charAt(0).toUpperCase() + (task.priority || 'medium').slice(1)}</span>
                    <span><strong>Status:</strong> ${task.is_completed ? 'Completed ✅' : 'Pending ⏳'}</span>
                    ${scheduledTime ? `<span><strong>Scheduled:</strong> ${scheduledTime.toLocaleDateString()}</span>` : ''}
                </div>
                <div class="task-actions">
                    ${!task.is_completed ? `<button class="task-action-btn complete-btn" onclick="toggleTaskCompletion('${task.id}', true)">Mark Complete</button>` : `<button class="task-action-btn complete-btn" onclick="toggleTaskCompletion('${task.id}', false)">Mark Incomplete</button>`}
                    <button class="task-action-btn edit-btn" onclick="editTask('${task.id}')">Edit</button>
                    <button class="task-action-btn delete-btn" onclick="deleteTask('${task.id}')">Delete</button>
                </div>
            </div>
        `;
        taskList.appendChild(li);
    });
}

function setupModal() {
    const openBtn = document.getElementById("open-modal-btn");
    const closeBtn = document.getElementById("close-modal-btn");
    const modal = document.getElementById("create-task-modal");
    const modalTitle = document.getElementById("modal-title");

    openBtn.onclick = () => {
        modal.style.display = "block";
        modalTitle.textContent = "Create New Task";
        document.getElementById("task-form").reset();
        document.getElementById("task-form").removeAttribute("data-editing-id");
    };
    
    closeBtn.onclick = () => modal.style.display = "none";

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}

function setupFormSubmit() {
    const form = document.getElementById("task-form");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const payload = {};
        formData.forEach((value, key) => {
            if (value) {
                payload[key] = key.includes('date') ? new Date(value).toISOString() : value;
            }
        });

        // Added: check if editing or creating
        const taskId = form.getAttribute("data-editing-id");
        const url = taskId 
            ? `https://3.27.123.53.sslp.io/api/tasks/${taskId}/` 
            : "https://3.27.123.53.sslp.io/api/tasks/create/";
        const method = taskId ? "PUT" : "POST";

        fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(payload),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            alert(taskId ? "Task updated successfully!" : "Task created successfully!");
            document.getElementById("create-task-modal").style.display = "none";
            form.reset();
            form.removeAttribute("data-editing-id"); // Clear edit mode
            fetchTasks();  // Refresh task list
        })
        .catch(error => {
            console.error("Error:", error);
            alert(taskId ? "Failed to update task." : "Failed to create task.");
        });
    });
}

/* --- NEW FUNCTIONS --- */

// Populate modal with existing task data
function editTask(id) {
    fetch(`https://3.27.123.53.sslp.io/api/tasks/${id}/`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
    })
    .then(res => res.json())
    .then(task => {
        const form = document.getElementById("task-form");
        const modal = document.getElementById("create-task-modal");
        const modalTitle = document.getElementById("modal-title");
        
        form.title.value = task.title;
        form.description.value = task.description || "";
        form.due_date.value = task.due_date ? task.due_date.slice(0, 16) : "";
        form.priority.value = task.priority || "medium";
        form.scheduled_time.value = task.scheduled_time ? task.scheduled_time.slice(0, 16) : "";
        form.setAttribute("data-editing-id", id); // Store task ID for update
        
        modalTitle.textContent = "Edit Task";
        modal.style.display = "block";
    })
    .catch(err => console.error("Error fetching task:", err));
}

// Toggle task completion
function toggleTaskCompletion(id, isCompleted) {
    fetch(`https://3.27.123.53.sslp.io/api/tasks/${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ is_completed: isCompleted }),
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to update task");
        return res.json();
    })
    .then(data => {
        fetchTasks(); // Refresh the task list
    })
    .catch(err => console.error("Error updating task:", err));
}

// Delete task
function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) return;

    fetch(`https://3.27.123.53.sslp.io/api/tasks/${id}/`, {
        method: "DELETE",
        credentials: "include",
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to delete task");
        alert("Task deleted successfully!");
        fetchTasks();
    })
    .catch(err => console.error("Error deleting task:", err));
}
