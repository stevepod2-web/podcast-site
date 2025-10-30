/* ===== dashboard.js =====
   Handles navbar highlighting, page detection,
   and any cross-page dynamic initialization.
*/

document.addEventListener("DOMContentLoaded", function() {
  // === Active Navbar Highlight ===
  const currentPath = window.location.pathname;
  document.querySelectorAll(".navbar-nav .nav-link").forEach(link => {
    const href = link.getAttribute("href");
    if (href && currentPath.startsWith(href)) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });

  // === Optional Tooltip Init (Bootstrap) ===
  if (window.bootstrap) {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  // === Shared Scheduler Refresh Handling (optional hook) ===
  const schedulerBtn = document.getElementById('scanBtn');
  if (schedulerBtn) {
    schedulerBtn.addEventListener('click', async () => {
      try {
        const res = await fetch('/production/api/run_scheduler', { method: 'POST' });
        console.log('Scheduler triggered', await res.text());
      } catch (err) {
        console.error('Scheduler trigger failed:', err);
      }
    });
  }

  // === Global Refresh Button ===
  const refreshBtn = document.getElementById('refreshBtn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      location.reload();
    });
  }
});
