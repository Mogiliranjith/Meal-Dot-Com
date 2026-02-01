function showSignIn() {
  document.getElementById("signin").classList.remove("hidden");
  document.getElementById("signup").classList.add("hidden");
}

function showSignUp() {
    document.getElementById("signup").classList.remove("hidden");
    document.getElementById("signin").classList.add("hidden");
}

function autoToggleForm(form) {
  if (form === "signup") {
    showSignUp();
  } else {
    showSignIn();
  }
}

// Customer profile menu (open + close on outside click)
document.addEventListener("DOMContentLoaded", () => {
  const icon = document.getElementById("profileIcon");
  const menu = document.getElementById("profileMenu");

  if (!icon || !menu) return;

  // Toggle when clicking the icon
  icon.addEventListener("click", (event) => {
    event.stopPropagation(); // prevent document click
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  });

  // Prevent menu clicks from closing it
  menu.addEventListener("click", (event) => {
    event.stopPropagation();
  });

  // Close when clicking anywhere else
  document.addEventListener("click", () => {
    menu.style.display = "none";
  });
});
