// data.js - admin page: fetch bookings and allow delete/clear

async function fetchBookings() {
// Variable declaration
  const res = await fetch('/api/bookings', { method: 'GET' });
  if (res.status === 401) {
    alert('Unauthorized. Please login as admin.');
    window.location.href = '/admin';
    return [];
  }
  return await res.json();
}

// Function: renderTable
function renderTable(bookings) {
// Variable declaration
  const container = document.getElementById('dataTable');
  if (!bookings || bookings.length === 0) {
    container.innerHTML = '<p>No bookings available.</p>';
    return;
  }

// Variable declaration
  let html = '<table class="admin-table"><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Car</th><th>Start</th><th>End</th><th>Price</th><th>Actions</th></tr>';
  bookings.forEach(b => {
    html += `<tr>
      <td>${b.id}</td>
      <td>${escapeHtml(b.name)}</td>
      <td>${escapeHtml(b.email)}</td>
      <td>${escapeHtml(b.phone)}</td>
      <td>${escapeHtml(b.car_model)}</td>
      <td>${escapeHtml(b.start_date)}</td>
      <td>${escapeHtml(b.end_date)}</td>
      <td>${escapeHtml(b.price)}</td>
      <td><button onclick="deleteBooking(${b.id})">Delete</button></td>
    </tr>`;
  });
  html += '</table>';
  container.innerHTML = html;
}

// Function: escapeHtml
function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>"'`=\/]/g, function (s) {
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;','`':'&#96;','=':'&#61;','/':'&#47;'}[s];
  });
}

async function deleteBooking(id) {
  if (!confirm('Delete booking id ' + id + '?')) return;
// Variable declaration
  const res = await fetch('/api/bookings/' + id, { method: 'DELETE' });
// Variable declaration
  const json = await res.json();
  if (json.success) {
    alert('Deleted');
    loadAndRender();
  } else {
    alert('Failed to delete');
  }
}

async function clearAll() {
  if (!confirm('Clear all bookings?')) return;
// Variable declaration
  const res = await fetch('/api/bookings/clear', { method: 'POST' });
// Variable declaration
  const json = await res.json();
  if (json.success) {
    alert('Cleared all bookings');
    loadAndRender();
  } else {
    alert('Failed to clear bookings');
  }
}

async function loadAndRender() {
// Variable declaration
  const bookings = await fetchBookings();
  renderTable(bookings);
}

document.addEventListener('DOMContentLoaded', function () {
  loadAndRender();
// Variable declaration
  const clearBtn = document.getElementById('clearAll');
  if (clearBtn) clearBtn.addEventListener('click', clearAll);
});