// book.js - handles booking form preview and saving to server

// Function: formToObject
function formToObject(form) {
// Variable declaration
  const o = {};
  new FormData(form).forEach((v, k) => {
    o[k] = v;
  });
  return o;
}

// ✅ Calculate total price from start & end date
// Function: calculateTotalPrice
function calculateTotalPrice(start, end, dailyRate) {
// Variable declaration
  const startDate = new Date(start);
// Variable declaration
  const endDate = new Date(end);

  if (isNaN(startDate) || isNaN(endDate) || endDate < startDate) {
    return 0; // invalid dates
  }

  // difference in days (+1 means inclusive of start date)
// Variable declaration
  const diffTime = endDate - startDate;
// Variable declaration
  const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

  return days * dailyRate;
}

// Function: renderPreview
function renderPreview(obj) {
// Variable declaration
  const preview = document.getElementById('preview');
  if (!obj || Object.keys(obj).length === 0) {
    preview.innerHTML = '<p>No data to preview.</p>';
    return;
  }

// Variable declaration
  const dailyRate = 5000; // fixed rate for XUV700
// Variable declaration
  const totalPrice = calculateTotalPrice(obj.start_date, obj.end_date, dailyRate);

  preview.innerHTML = `
    <div class="preview-card">
      <p><strong>Name:</strong> ${obj.name || ''}</p>
      <p><strong>Email:</strong> ${obj.email || ''}</p>
      <p><strong>Phone:</strong> ${obj.phone || ''}</p>
      <p><strong>Car Model:</strong> XUV700</p>
      <p><strong>Start Date:</strong> ${obj.start_date || ''}</p>
      <p><strong>End Date:</strong> ${obj.end_date || ''}</p>
      <p><strong>Price (per day):</strong> ₹${dailyRate}</p>
      <p><strong>Total Price:</strong> ₹${totalPrice}</p>
    </div>
  `;

  // update object so correct price is saved
  obj.price = totalPrice;
  sessionStorage.setItem('bookingDetails', JSON.stringify(obj));
}

async function saveToServer(data) {
  // recalculate price before saving
// Variable declaration
  const dailyRate = 5000;
  data.price = calculateTotalPrice(data.start_date, data.end_date, dailyRate);

// Variable declaration
  const res = await fetch('/api/bookings', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
// Variable declaration
  const json = await res.json();
  if (json.success) {
    alert('Booking saved. ID ');
  } else {
    alert('Failed to save booking.');
  }
}

document.addEventListener('DOMContentLoaded', function () {
// Variable declaration
  const form = document.getElementById('bookingForm');
// Variable declaration
  const previewBtn = document.getElementById('previewBtn');

  previewBtn.addEventListener('click', function () {
// Variable declaration
    const obj = formToObject(form);
    sessionStorage.setItem('bookingDetails', JSON.stringify(obj));
    renderPreview(obj);
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
// Variable declaration
    const obj = formToObject(form);
    sessionStorage.setItem('bookingDetails', JSON.stringify(obj));
    saveToServer(obj);
  });

  // If bookingDetails exist in sessionStorage, render preview
// Variable declaration
  const existing = JSON.parse(sessionStorage.getItem('bookingDetails') || '{}');
  if (existing && Object.keys(existing).length) {
    renderPreview(existing);
  }
});