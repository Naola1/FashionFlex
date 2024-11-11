// JavaScript to enhance the interaction of nested dropdown menus

document.addEventListener("DOMContentLoaded", () => {
    const dropdownItems = document.querySelectorAll(".dropdown-item");
  
    dropdownItems.forEach((item) => {
      item.addEventListener("mouseenter", () => {
        const submenu = item.querySelector(".submenu");
        if (submenu) {
          submenu.style.display = "block";
        }
      });
  
      item.addEventListener("mouseleave", () => {
        const submenu = item.querySelector(".submenu");
        if (submenu) {
          submenu.style.display = "none";
        }
      });
    });
  });
  