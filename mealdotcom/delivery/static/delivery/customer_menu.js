document.addEventListener("DOMContentLoaded", () => {
  const menuTopBar = document.querySelector(".menu-top-bar");
  const hero = document.getElementById("heroSection");
  const menuSection = document.getElementById("menuSection");

  if (!menuTopBar || !hero || !menuSection) return;

  let snapped = false;
  let isAnimating = false;

  /* ---------- Shadow ---------- */
  window.addEventListener("scroll", () => {
    menuTopBar.classList.toggle("scrolled", window.scrollY > 10);
  });

  /* ---------- Smooth scroll with easing ---------- */
  function smoothScrollTo(targetY, duration = 320) {
    const startY = window.scrollY;
    const distance = targetY - startY;
    let startTime = null;

    function easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    }

    function animation(currentTime) {
      if (!startTime) startTime = currentTime;
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = easeOutCubic(progress);

      window.scrollTo(0, startY + distance * ease);

      if (progress < 1) {
        requestAnimationFrame(animation);
      } else {
        isAnimating = false;
      }
    }

    requestAnimationFrame(animation);
  }

  /* ---------- Intersection Observer ---------- */
  const observer = new IntersectionObserver(
    ([entry]) => {
      // Hero leaving → snap
      if (!entry.isIntersecting && !snapped && !isAnimating) {
        snapped = true;
        isAnimating = true;

        const targetY =
          menuSection.getBoundingClientRect().top +
          window.scrollY -
          menuTopBar.offsetHeight;

        smoothScrollTo(targetY, 300);
      }

      // Hero back → rearm
      if (entry.isIntersecting) {
        snapped = false;
      }
    },
    {
      threshold: 0.5,
    },
  );

  observer.observe(hero);
});
