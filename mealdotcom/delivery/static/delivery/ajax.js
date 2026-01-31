document.addEventListener("DOMContentLoaded", () => {
  /* =========================
     HOME PAGE: Restaurant Search
     ========================= */

  const searchBox = document.getElementById("searchBox");
  const restaurantContainer = document.getElementById("restaurantContainer");

  // =========================
  // Veg / Non-Veg Toggle
  // =========================

  let vegOnly = localStorage.getItem("vegOnly") === "true";

  const vegToggle = document.getElementById("vegToggle");

  if (vegToggle) {
    vegToggle.checked = vegOnly;
  }

  if (vegToggle) {
    vegToggle.addEventListener("change", () => {
      vegOnly = vegToggle.checked;
      localStorage.setItem("vegOnly", vegOnly);
      triggerSearch();
      triggerMenuSearch();
      triggerAdminSearch();
    });
  }

  function triggerSearch() {
    if (!searchBox || !restaurantContainer) return;

    const query = searchBox.value.trim();
    fetch(`/live-search/?q=${query}&veg=${vegOnly}`)
      .then((res) => res.json())
      .then(renderRestaurants);
  }

  function renderRestaurants(data) {
    restaurantContainer.innerHTML = "";

    if (data.results.length === 0) {
      restaurantContainer.innerHTML = "<p>No restaurants found</p>";
      return;
    }

    data.results.forEach((r) => {
      restaurantContainer.innerHTML += `
        <div class="cards">
          <img src="${r.picture}">
          <h4>${r.name}</h4>
          <p><strong>Cuisine:</strong> ${r.cuisine}</p>
          <p><strong>Rating:</strong> ${r.rating}</p>
          <a href="/view_menu/${r.id}/${CUSTOMER_NAME}">View Menu</a>
        </div>
      `;
    });
  }

  if (searchBox && restaurantContainer) {
    searchBox.addEventListener("keyup", triggerSearch);
  }

  // Initial load (show all restaurants)
  if (searchBox && restaurantContainer) {
    triggerSearch();
  }

  /* =========================
     CUSTOMER MENU: Food Search
     ========================= */

  const foodSearchBox = document.getElementById("foodSearchBox");
  const menuContainer = document.getElementById("menuContainer");

  function triggerMenuSearch() {
    if (!foodSearchBox || !menuContainer) return;

    const query = foodSearchBox.value.trim();

    fetch(
      `/menu-live-search/?q=${query}&restaurant_id=${RESTAURANT_ID}&veg=${vegOnly}`,
    )
      .then((res) => res.json())
      .then((data) => {
        menuContainer.innerHTML = "";

        if (data.results.length === 0) {
          menuContainer.innerHTML = "<p>No items found</p>";
          return;
        }

        data.results.forEach((item) => {
          menuContainer.innerHTML += `
          <div class="cards">
            <img src="${item.picture}">
            <h4>${item.name}</h4>
            <p>${item.description}</p>
            <p><strong>₹ ${item.price}</strong></p>
            <a href="/add_to_cart/${item.id}/${CUSTOMER_NAME}">
              Add to cart
            </a>
          </div>
        `;
        });
      });
  }

  /* =========================
     ADMIN HOME: Restaurant Search
     ========================= */

  const adminSearchBox = document.getElementById("adminSearchBox");
  const adminTable = document.getElementById("adminRestaurantTable");

  function triggerAdminSearch() {
    if (!adminSearchBox || !adminTable) return;

    const query = adminSearchBox.value.trim();

    fetch(`/live-search/?q=${query}&veg=${vegOnly}`)
      .then((res) => res.json())
      .then((data) => {
        adminTable.innerHTML = "";

        if (data.results.length === 0) {
          adminTable.innerHTML = `
          <tr>
            <td colspan="7">No restaurants found</td>
          </tr>`;
          return;
        }

        data.results.forEach((r) => {
          adminTable.innerHTML += `
          <tr>
            <td>${r.name}</td>
            <td><img src="${r.picture}" width="80"></td>
            <td>${r.address ?? "-"}</td>
            <td><a href="${r.location ?? "#"}" target="_blank">Map</a></td>
            <td>${r.cuisine}</td>
            <td>${r.rating}</td>
            <td>
              <a href="/admin_restaurant_detail/${r.id}/">
                <button>View</button>
              </a>
            </td>
          </tr>
        `;
        });
      });
  }

  if (foodSearchBox && menuContainer) {
    foodSearchBox.addEventListener("keyup", triggerMenuSearch);
    triggerMenuSearch(); // initial load
  }

  if (adminSearchBox && adminTable) {
    adminSearchBox.addEventListener("keyup", triggerAdminSearch);
    triggerAdminSearch();
  }

  /* =========================
     ADMIN RESTAURANT DETAILS:
     Menu Item Search
     ========================= */

  const adminFoodSearchBox = document.getElementById("adminFoodSearchBox");
  const adminMenuContainer = document.getElementById("adminMenuContainer");

  if (adminFoodSearchBox && adminMenuContainer) {
    adminFoodSearchBox.addEventListener("keyup", () => {
      const query = adminFoodSearchBox.value.trim();

      fetch(
        `/menu-live-search/?q=${query}&restaurant_id=${ADMIN_RESTAURANT_ID}`,
      )
        .then((res) => res.json())
        .then((data) => {
          adminMenuContainer.innerHTML = "";

          if (data.results.length === 0) {
            adminMenuContainer.innerHTML = "<p>No items found</p>";
            return;
          }

          data.results.forEach((item) => {
            adminMenuContainer.innerHTML += `
              <div class="cards">
                <h4>${item.name}</h4>
                <p><strong>Price:</strong> ₹${item.price}</p>
                <p><strong>Type:</strong> ${item.vegeterian ? "Veg" : "Non-Veg"}</p>
                ${item.picture ? `<img src="${item.picture}">` : ""}
                <form action="/delete_menu_item/${item.id}" method="post">
                  <button type="submit" class="delete-btn">Delete</button>
                </form>
              </div>
            `;
          });
        });
    });
  }
});
