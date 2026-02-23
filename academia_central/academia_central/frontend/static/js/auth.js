// frontend/static/js/auth.js
// This file runs on EVERY page.
// It checks if the user is logged in and updates the navbar accordingly.

(function () {
  const token = localStorage.getItem("token");
  const role  = localStorage.getItem("role");

  if (token) {
    // User IS logged in — show the correct dashboard link and logout button
    document.getElementById("nav-login")?.classList.add("d-none");
    document.getElementById("nav-register")?.classList.add("d-none");
    document.getElementById("nav-logout")?.classList.remove("d-none");

    if (role === "admin") {
      document.getElementById("nav-admin-dash")?.classList.remove("d-none");
    } else {
      document.getElementById("nav-student-dash")?.classList.remove("d-none");
    }

    // Redirect to dashboard if user tries to visit login/register while logged in
    const currentPath = window.location.pathname;
    if (currentPath === "/login" || currentPath === "/register") {
      window.location.href = role === "admin" ? "/admin/dashboard" : "/student/dashboard";
    }
  } else {
    // User is NOT logged in — protect dashboard pages
    const protectedPaths = ["/student/dashboard", "/student/profile", "/student/courses", "/admin/dashboard"];
    if (protectedPaths.includes(window.location.pathname)) {
      window.location.href = "/login";
    }
  }
})();

/**
 * logout() — Called when user clicks the Logout button in the navbar.
 * Clears all stored data and redirects to the login page.
 */
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("name");
  window.location.href = "/login";
}
