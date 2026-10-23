let rooms = [];
let selectedRoom = null;
let notifications = [];
let currentFilter = 'all';
let searchTerm = '';

async function loadRooms() {
const response = await fetch('/api/rooms/');
rooms = await response.json();
updateStats();
renderRooms();
}

function updateStats() {
  document.getElementById('count-free').textContent     = rooms.filter(r => r.status === 'free').length;
  document.getElementById('count-occupied').textContent = rooms.filter(r => r.status === 'occupied').length;
  document.getElementById('count-cleaning').textContent = rooms.filter(r => r.status === 'cleaning').length;
}

function addNotif(type, text) {
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  notifications.unshift({ type, text, time });
  renderNotifs();
}

function renderNotifs() {
  const list = document.getElementById('notif-list');
  document.getElementById('notif-count').textContent = notifications.length;
  if (!notifications.length) {
    list.innerHTML = '<div style="font-size:13px;color:#999;text-align:center;padding:20px 0;">No notifications yet</div>';
    return;
  }
  const ico = { occupied: 'ti-alert-circle', free: 'ti-circle-check', info: 'ti-info-circle' };
  list.innerHTML = notifications.map(n =>
    `<div class="notif-item ${n.type}">
      <i class="ti ${ico[n.type]}"></i>
      <div>${n.text}<div class="notif-time">${n.time}</div></div>
    </div>`
  ).join('');
}

function clearNotifs() { notifications = []; renderNotifs(); }

function getFiltered() {
  return rooms.filter(r => {
    const matchFilter = currentFilter === 'all' || r.status === currentFilter;
    const matchSearch = !searchTerm || r.id.toLowerCase().includes(searchTerm.toLowerCase());
    return matchFilter && matchSearch;
  });
}

function renderRooms() {
  const grid = document.getElementById('rooms-grid');
  const filtered = getFiltered();
  if (!filtered.length) {
    grid.innerHTML = '<div class="empty-msg">No rooms match your filter</div>';
    return;
  }
  const label = { free: 'Available', occupied: 'Occupied', cleaning: 'Cleaning' };
  grid.innerHTML = filtered.map(room =>
    `<div class="room-card ${selectedRoom && selectedRoom.id === room.id ? 'selected' : ''}"
          onclick="selectRoom('${room.id}')">
      <div class="room-thumb ${room.status}">
        <i class="ti ti-bed"></i>
        <div class="status-dot ${room.status}"></div>
      </div>
      <div class="room-body">
        <div class="room-number">${room.id}</div>
        <div class="room-type">${room.type}</div>
        <span class="room-status-badge badge-${room.status}">${label[room.status]}</span>
        <div class="room-price">KES <span>${(room.price * 130).toLocaleString()}</span>/night</div>
      </div>
    </div>`
  ).join('');
}

function filterRooms(filter, btn) {
  currentFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderRooms();
}

function searchRooms(val) {
  searchTerm = val;
  renderRooms();
}

async function selectRoom(id) {
  const room = rooms.find(r => r.id === id);
  if (!room) return;
  selectedRoom = room;
  renderRooms();

  const infoEl = document.getElementById('selected-info');

  if (room.status === 'occupied') {
    alert(`Sorry, ${room.id} is already occupied. Please choose another room.`);
    infoEl.innerHTML = `Selected: ${room.id} — Occupied`;
    addNotif('occupied', `${room.id} is already occupied. Please select a different room.`);
  } else if (room.status === 'cleaning') {
    alert(`${room.id} is currently being cleaned. Please choose another room.`);
    infoEl.innerHTML = `Selected: ${room.id} — Cleaning`;
    addNotif('info', `${room.id} is being cleaned and is not yet available for booking.`);
  } else {
    const guestName = prompt(`Enter your name to book ${room.id} (${room.type}):`);
    if (guestName && guestName.trim()) {
      const checkIn = prompt("Check-in date (YYYY-MM-DD):");
      const checkOut = prompt("Check-out date (YYYY-MM-DD):");
      const payment = prompt("Payment method (Cash/Card):");
      if (checkIn && checkOut && payment) {
        const response = await fetch('/api/book/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            room_id: room.id,
            guest_name: guestName.trim(),
            check_in: checkIn,
            check_out: checkOut,
            payment: payment
          })
        });
        if (response.ok) {
          room.status = 'occupied';
          room.guest = guestName.trim();
          addNotif('info', `${room.id} booked successfully for ${guestName} from ${checkIn} to ${checkOut} via ${payment}!`);
          infoEl.innerHTML = `Booked: ${room.id} for ${guestName}`;
          updateStats();
          renderRooms();
        } else {
          alert('Booking failed.');
        }
      } else {
        alert("Booking cancelled due to incomplete information.");
        infoEl.innerHTML = `Booking cancelled for ${room.id}`;
        selectedRoom = null;
        renderRooms();
      }
    } else {
      infoEl.innerHTML = `Booking cancelled for ${room.id}`;
      selectedRoom = null;
      renderRooms();
    }
  }
}

loadRooms();
addNotif('info', 'System online — Rooms loaded from database.');
