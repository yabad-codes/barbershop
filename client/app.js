const API_URL = 'http://localhost:8000/api';

// Fetch all bookings
async function getBookings() {
    const response = await fetch(`${API_URL}/bookings/`);
    const bookings = await response.json();
    displayBookings(bookings);
}

// Display bookings in the DOM
function displayBookings(bookings) {
    const bookingsDiv = document.getElementById('bookings');
    bookingsDiv.innerHTML = bookings.map(booking => `
        <div class="booking-item">
            <p>Name: ${booking.name}</p>
            <p>Date: ${booking.date}</p>
            <p>Time: ${booking.time}</p>
            <p>Phone: ${booking.phone}</p>
            ${booking.email ? `<p>Email: ${booking.email}</p>` : ''}
            <button onclick="deleteBooking(${booking.id})">Cancel</button>
        </div>
    `).join('');
}

// Create new booking
document.getElementById('bookingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const booking = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value || null,
        phone: document.getElementById('phone').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value
    };

    try {
        const response = await fetch(`${API_URL}/bookings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(booking)
        });

        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            return;
        }

        document.getElementById('bookingForm').reset();
        getBookings();
    } catch (error) {
        alert('Error creating booking');
    }
});

// Delete booking
async function deleteBooking(id) {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
        const response = await fetch(`${API_URL}/bookings/${id}/`, {
            method: 'DELETE'
        });

        if (response.ok) {
            getBookings();
        }
    } catch (error) {
        alert('Error deleting booking');
    }
}

// Load bookings on page load
getBookings();