function editField(field) {
    document.getElementById(`${field}-input`).classList.remove('hidden');
    document.querySelectorAll('.save-button').forEach(btn => btn.classList.remove('hidden'));
}

function saveField(field) {
    const newValue = document.getElementById(`${field}-input`).value;
    const eventId = {{ event.id }}; // Get event ID dynamically

    fetch(`/events/${eventId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ [field]: newValue })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            location.reload(); // Refresh the page to show updated values
        }
    })
    .catch(error => console.error('Error:', error));
}
