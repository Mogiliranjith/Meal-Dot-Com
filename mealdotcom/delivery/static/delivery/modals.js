// ADD RESTAURANT MODAL
function openAddModal() {
  document.getElementById("addRestaurantModal").style.display = "block";
}
function closeAddModal() {
  document.getElementById("addRestaurantModal").style.display = "none";
}

// UPDATE RESTAURANT MODAL
function openUpdateModal() {
  document.getElementById("updateRestaurantModal").style.display = "block";
}
function closeUpdateModal() {
  document.getElementById("updateRestaurantModal").style.display = "none";
}

// ADD MENU ITEM MODAL
function openAddMenuModal() {
  document.getElementById("addMenuModal").style.display = "block";
}
function closeAddMenuModal() {
  document.getElementById("addMenuModal").style.display = "none";
}

// CLOSE MODAL WHEN CLICKING OUTSIDE THE MODAL WINDOW
window.onclick = function(event) {
  const profileModal = this.document.getElementById("profileModal");
  const addModal = this.document.getElementById("addRestaurantModal");
  const updateModal = this.document.getElementById("updateRestaurantModal");
  const addMenuModal = this.document.getElementById("addMenuModal");

  if (event.target === profileModal) profileModal.style.display = "none";
  if (event.target === addModal) addModal.style.display = "none";
  if (event.target === updateModal) updateModal.style.display = "none";
  if (event.target === addMenuModal) addMenuModal.style.display = "none";
};

// CUSTOMER PROFILE MODAL
function openProfileModal() {
  document.getElementById("profileModal").style.display = "block";
}

function closeProfileModal() {
  document.getElementById("profileModal").style.display = "none";
}


// Order history
function loadOrderHistory() {
  console.log("My orders clicked");
  const container = document.getElementById("orderHistory");
  container.innerHTML = "Loading...";

  fetch("/order-history/")
    .then(response => response.json())
    .then(data => {
      if (!data.orders || data.orders.length === 0) {
        container.innerHTML = "<p>No previous orders found.</p>";
        return;
      }

      let html = "";

      data.orders.forEach((order, index) => {
        html += `<div style="border:1px solid #ddd; padding:10px; margin-bottom:10px;">
          <strong>Order ${index + 1}</strong>
          <ul>`;
        
        order.items.forEach(item => {
          html += `<li>${item.name} - ₹${item.price}</li>`;
        });

        html += `</ul>
          <strong>Total: ₹${order.total_price}</strong>
        </div>`;
      });

      container.innerHTML = html;
    })
    .catch(() => {
      container.innerHTML = "<p>Error loading orders.</p>";
    });
}
