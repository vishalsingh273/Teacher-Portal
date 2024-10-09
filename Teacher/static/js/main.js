document.querySelectorAll('.edit-marks').forEach(input => {
    input.addEventListener('change', function() {
        let studentId = this.dataset.id;
        let marks = this.value;
        fetch('/update_student/', {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Function to get the CSRF token
                'Content-Type': 'application/json'
            },
            // ... rest of your code
        });
        
        fetch(`/update_student/${studentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'marks': marks })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                alert('Marks updated successfully!');
            }
        });
    });
});
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function updateStudent(id, field, value) {
    const data = {
        id: id,
        field: field,
        value: value
    };

    console.log("Sending data:", data); // Log the data being sent

    fetch('/update_student/', {
        method: 'PUT',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}', // Make sure to include the CSRF token correctly
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data); // Log the response from the server
        if (data.success) {
            alert('Student updated successfully!');
        } else {
            alert('Error updating student: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating student');
    });
}


function deleteStudent(studentId) {
    fetch(`/delete_student/${studentId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        }
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert('Student deleted successfully!');
            location.reload();
        } else {
            alert(data.error || 'An error occurred');
        }
    }).catch(error => console.error('Error:', error));
}
