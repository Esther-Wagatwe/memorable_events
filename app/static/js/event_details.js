function updateEvent() {
    const name = document.getElementById('event-name-input').value;
    const date = document.getElementById('event-date-input').value;
    const description = document.getElementById('event-description-input').value;

    fetch(`/events/{{ event.event_id }}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, date, description })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Event updated successfully');
            window.location.href = '/';
        } else {
            alert(`Failed to update event: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update event');
    });
}

function editEventAttribute(attribute) {
    const inputId = `event-${attribute}-input`;
    const inputElement = document.getElementById(inputId);
    inputElement.disabled = !inputElement.disabled;
    if (!inputElement.disabled) {
        inputElement.focus();
    } else {
        const newValue = inputElement.value;
        fetch(`/events/{{ event.event_id }}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ [attribute]: newValue })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert('Event updated successfully');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update event');
        });
    }
}

function showReviewForm(vendorId) {
    document.getElementById(`review-form-${vendorId}`).style.display = 'block';
}

function submitReview(event, vendorId) {
    event.preventDefault();
    const form = event.target;
    const rating = form.rating.value;
    const comment = form.comment.value;

    fetch('/reviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rating, comment, vendor_id: vendorId, event_id: {{ event.event_id }} })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Review added successfully');
            location.reload();
        } else {
            alert(`Failed to add review: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add review');
    });
}

function removeVendor(vendorId) {
    fetch(`/vendors/${vendorId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            alert('Vendor removed successfully');
            location.reload();
        } else {
            response.json().then(data => alert(data.error));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to remove vendor');
    });
}

function submitGuestForm(event) {
    event.preventDefault();
    const form = event.target;
    const name = form.name.value;
    const email = form.email.value;
    const phone = form.phone.value;

    fetch('/guests/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, phone, status: 'pending', event_id: {{ event.event_id }} })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Guest added successfully');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add guest');
    });
}

function editTask(button) {
    const row = button.closest('tr');
    row.querySelectorAll('input, select').forEach(element => element.disabled = false);
    button.style.display = 'none';
    row.querySelector('.save-task-button').style.display = 'inline';
}

function saveTask(button) {
    const row = button.closest('tr');
    const taskId = button.getAttribute('data-id');
    const description = row.querySelector('input[type="text"]').value;
    const status = row.querySelector('select').value;
    const dueDate = row.querySelector('input[type="date"]').value;

    fetch(`/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ description, status, due_date: dueDate })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Task updated successfully');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update task');
    });
}

function deleteTask(button) {
    const taskId = button.getAttribute('data-id');

    fetch(`/tasks/${taskId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            alert('Task deleted successfully');
            location.reload();
        } else {
            response.json().then(data => alert(data.error));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to delete task');
    });
}

function showAddTaskForm() {
    document.querySelector('.add-task-form').style.display = 'block';
}

function submitTaskForm(event) {
    event.preventDefault();
    const form = event.target;
    const description = form.description.value;
    const status = form.status.value;
    const dueDate = form.due_date.value;

    fetch('/tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ description, status, due_date: dueDate, event_id: {{ event.event_id }} })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Task added successfully');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add task');
    });
}