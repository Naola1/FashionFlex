const mainImage = document.getElementById('main-image');
const thumbnailImages = document.querySelectorAll('.thumbnail-images img');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let currentIndex = 0;
let visibleRangeStart = 0; // Starting index of visible thumbnails
let autoRotateInterval; // Variable to hold the interval for auto-rotation

function updateMainImage(index) {
  mainImage.src = thumbnailImages[index].src;
}

function updateThumbnailVisibility() {
  thumbnailImages.forEach((thumbnail, index) => {
    // Show only two thumbnails at a time based on the visible range
    thumbnail.style.display = (index >= visibleRangeStart && index < visibleRangeStart + 2) ? 'block' : 'none';
  });
}

function startAutoRotate() {
  autoRotateInterval = setInterval(() => {
    nextBtn.click(); // Simulate a click on the next button
  }, 9000); // Change image every 9 seconds
}

thumbnailImages.forEach((thumbnail, index) => {
  thumbnail.addEventListener('click', () => {
    currentIndex = index;
    updateMainImage(currentIndex);
    visibleRangeStart = Math.floor(currentIndex / 3) * 3; // Adjust visible range based on current index
    updateThumbnailVisibility();
    resetAutoRotate(); // Reset the auto-rotate timer on user interaction
  });
});

prevBtn.addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + thumbnailImages.length) % thumbnailImages.length; // Wrap around
  updateMainImage(currentIndex);

  // Adjust visible range for thumbnails
  visibleRangeStart = Math.floor(currentIndex / 3) * 3; // Always set to the correct range
  updateThumbnailVisibility();
  resetAutoRotate(); // Reset the auto-rotate timer on user interaction
});

nextBtn.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % thumbnailImages.length; // Wrap around
  updateMainImage(currentIndex);

  // Adjust visible range for thumbnails
  visibleRangeStart = Math.floor(currentIndex / 3) * 3; // Always set to the correct range
  updateThumbnailVisibility();
  resetAutoRotate(); // Reset the auto-rotate timer on user interaction
});

// Function to reset the auto-rotate timer
function resetAutoRotate() {
  clearInterval(autoRotateInterval); // Clear existing interval
  startAutoRotate(); // Restart the auto-rotate
}

// Keyboard navigation functionality
document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft') {
    prevBtn.click(); // Simulate click on previous button
  } else if (event.key === 'ArrowRight') {
    nextBtn.click(); // Simulate click on next button
  }
});

// Initialize
updateMainImage(currentIndex);
updateThumbnailVisibility();
startAutoRotate(); // Start the auto-rotation