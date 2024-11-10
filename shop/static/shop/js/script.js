document.addEventListener("DOMContentLoaded", function() {
    let currentImageIndex = 0;
    const images = document.querySelectorAll(".slider-image");
    const totalImages = images.length;

    // Initialize the first image
    images[currentImageIndex].classList.add("active");

    document.getElementById("next").addEventListener("click", function() {
        images[currentImageIndex].classList.remove("active");
        currentImageIndex = (currentImageIndex + 1) % totalImages;
        images[currentImageIndex].classList.add("active");
    });

    document.getElementById("prev").addEventListener("click", function() {
        images[currentImageIndex].classList.remove("active");
        currentImageIndex = (currentImageIndex - 1 + totalImages) % totalImages;
        images[currentImageIndex].classList.add("active");
    });

    // Login/Logout Toggle Logic
    const isLoggedIn = false; // Replace with actual login status
    const loginLink = document.querySelector("nav ul li a[href='#login']");
    const signupLink = document.querySelector("nav ul li a[href='#signup']");
    const logoutLink = document.getElementById("logout");

    if (isLoggedIn) {
        loginLink.style.display = "none";
        signupLink.style.display = "none";
        logoutLink.style.display = "block";
    } else {
        loginLink.style.display = "block";
        signupLink.style.display = "block";
        logoutLink.style.display = "none";
    }
});
