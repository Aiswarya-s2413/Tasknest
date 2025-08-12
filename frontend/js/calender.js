let currentDate = new Date();
let tasks = []; 


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
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Received data:', data);
        if (Array.isArray(data)) {
            tasks = data;
        } else if (data && Array.isArray(data.results)) {
            tasks = data.results;
        } else {
            console.warn("API response is not an array:", data);
            tasks = [];
        }
        renderCalendar();
    })
    .catch(error => {
        console.error("Error fetching tasks:", error);
        tasks = [];
        renderCalendar();
    });
}

function renderCalendar() {
    if (!Array.isArray(tasks)) {
        tasks = [];
    }
    const monthYear = document.getElementById('month-year');
    const calendarGrid = document.getElementById('calendar-grid');
    
    if (!monthYear || !calendarGrid) {
        console.error("Calendar elements not found in DOM");
        return;
    }

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    monthYear.textContent = currentDate.toLocaleString('default', { 
        month: 'long', 
        year: 'numeric' 
    });

    calendarGrid.innerHTML = '';

    // First day of month (0 = Sunday, 1 = Monday, etc.)
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty slots before first day of month
    for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement('div');
        emptyDiv.classList.add('calendar-day', 'empty');
        calendarGrid.appendChild(emptyDiv);
    }

    // Days of month
    for (let day = 1; day <= daysInMonth; day++) {
        const dateDiv = document.createElement('div');
        dateDiv.classList.add('calendar-day');

        const dateSpan = document.createElement('div');
        dateSpan.classList.add('date');
        dateSpan.textContent = day;
        dateDiv.appendChild(dateSpan);

        // Find tasks for this specific date
        const dayTasks = (Array.isArray(tasks) ? tasks : []).filter(task => {
            if (!task || !task.due_date) return false;
            
            try {
                const taskDate = new Date(task.due_date);
                return taskDate.getDate() === day &&
                       taskDate.getMonth() === month &&
                       taskDate.getFullYear() === year;
            } catch (error) {
                console.warn("Invalid date in task:", task);
                return false;
            }
        });

        // Add tasks to the day
        dayTasks.forEach(task => {
            const taskDiv = document.createElement('div');
            taskDiv.classList.add('task');
            taskDiv.textContent = task.title || 'Untitled Task';
            
            // Add completion status
            if (task.is_completed) {
                taskDiv.classList.add('completed');
            }
            
            // Add priority class
            if (task.priority) {
                taskDiv.classList.add(`priority-${task.priority.toLowerCase()}`);
            }
            
            // Add click handler to view task details
            taskDiv.addEventListener('click', () => {
                showTaskDetails(task);
            });
            
            dateDiv.appendChild(taskDiv);
        });

        calendarGrid.appendChild(dateDiv);
    }
}

function changeMonth(delta) {
    currentDate.setMonth(currentDate.getMonth() + delta);
    renderCalendar();
}

function showTaskDetails(task) {
    const details = `
Title: ${task.title || 'Untitled'}
Description: ${task.description || 'No description'}
Due Date: ${task.due_date ? new Date(task.due_date).toLocaleString() : 'Not set'}
Priority: ${task.priority || 'Medium'}
Status: ${task.is_completed ? 'Completed ✅' : 'Pending ❌'}
    `;
    alert(details);
}

// Initialize calendar when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing calendar...");
    console.log("Current URL:", window.location.href);
    console.log("Available cookies:", document.cookie);
    
    // Set up navigation buttons if they exist
    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => changeMonth(-1));
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => changeMonth(1));
    }
    
    // Add a small delay to ensure cookies are fully loaded
    setTimeout(() => {
        console.log("Delayed initialization - cookies:", document.cookie);
        fetchTasks();
    }, 100);
});

// refresh function
function refreshCalendar() {
    fetchTasks();
}

//  Auto-refresh every 5 minutes
setInterval(refreshCalendar, 5 * 60 * 1000);