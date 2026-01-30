document.addEventListener("DOMContentLoaded", () => {
  const menuTopBar = document.querySelector(".menu-top-bar");

  if (!menuTopBar) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 10) {
      menuTopBar.classList.add("scrolled");
    } else {
      menuTopBar.classList.remove("scrolled");
    }
  });
});
