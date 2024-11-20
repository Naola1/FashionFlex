document.addEventListener('DOMContentLoaded', () => {
  // Code for the main image and thumbnails (common for all pages)
  const mainImage = document.getElementById('main-image');
  const thumbnailImages = document.querySelectorAll('.thumbnail-images img');
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');

  if (mainImage && thumbnailImages.length > 0 && prevBtn && nextBtn) {
      console.log('Main Image:', mainImage);
      console.log('Thumbnail Images:', thumbnailImages);
      console.log('Previous Button:', prevBtn);
      console.log('Next Button:', nextBtn);

      let currentIndex = 0;
      let visibleRangeStart = 0;
      let autoRotateInterval;

      function updateMainImage(index) {
          mainImage.src = thumbnailImages[index].src;
      }

      function updateThumbnailVisibility() {
          thumbnailImages.forEach((thumbnail, index) => {
              thumbnail.style.display = (index >= visibleRangeStart && index < visibleRangeStart + 2) ? 'block' : 'none';
          });
      }

      function startAutoRotate() {
          autoRotateInterval = setInterval(() => {
              nextBtn.click();
          }, 9000);
      }

      thumbnailImages.forEach((thumbnail, index) => {
          thumbnail.addEventListener('click', () => {
              currentIndex = index;
              updateMainImage(currentIndex);
              visibleRangeStart = Math.floor(currentIndex / 3) * 3;
              updateThumbnailVisibility();
              resetAutoRotate();
          });
      });

      prevBtn.addEventListener('click', () => {
          currentIndex = (currentIndex - 1 + thumbnailImages.length) % thumbnailImages.length;
          updateMainImage(currentIndex);
          visibleRangeStart = Math.floor(currentIndex / 3) * 3;
          updateThumbnailVisibility();
          resetAutoRotate();
      });

      nextBtn.addEventListener('click', () => {
          currentIndex = (currentIndex + 1) % thumbnailImages.length;
          updateMainImage(currentIndex);
          visibleRangeStart = Math.floor(currentIndex / 3) * 3;
          updateThumbnailVisibility();
          resetAutoRotate();
      });

      function resetAutoRotate() {
          clearInterval(autoRotateInterval);
          startAutoRotate();
      }

      document.addEventListener('keydown', (event) => {
          if (event.key === 'ArrowLeft') {
              prevBtn.click();
          } else if (event.key === 'ArrowRight') {
              nextBtn.click();
          }
      });

      updateMainImage(currentIndex);
      updateThumbnailVisibility();
      startAutoRotate();
  } else {
      console.log('Thumbnail carousel elements not found on this page.');
  }

  // Code for the detail page (only executes if detail-specific elements exist)
  
    // Only initialize if we're on the rental detail page
    const rentalForm = document.getElementById('rentalForm');
    if (!rentalForm) return;

    const rentalDateInput = document.getElementById("rental_date");
    const durationSelect = document.getElementById("duration");
    const returnDateInput = document.getElementById("return_date");
    const totalPriceSpan = document.getElementById("totalPrice");
    
    // Get the price from the data attribute
    const priceElement = document.querySelector('[data-price]');
    
    if (rentalDateInput && durationSelect && returnDateInput && totalPriceSpan && priceElement) {
        console.log('Rental detail page detected.');
        
        // Get the price value from the data attribute
        const pricePerDay = parseFloat(priceElement.dataset.price);
        console.log('Price per day:', pricePerDay);

        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        rentalDateInput.setAttribute('min', today);
        
        function calculateReturnDateAndPrice() {
            const rentalDateValue = rentalDateInput.value;
            const durationValue = parseInt(durationSelect.value);
            
            if (rentalDateValue && durationValue) {
                const rentalDate = new Date(rentalDateValue);
                const returnDate = new Date(rentalDate);
                
                returnDate.setDate(rentalDate.getDate() + durationValue);
                returnDateInput.value = returnDate.toISOString().split("T")[0];
                
                const totalPrice = durationValue * pricePerDay;
                totalPriceSpan.textContent = `$${totalPrice.toFixed(2)}`;
            } else {
                returnDateInput.value = "";
                totalPriceSpan.textContent = "$0.00";
            }
        }
        
        // Add event listeners
        rentalDateInput.addEventListener("input", calculateReturnDateAndPrice);
        durationSelect.addEventListener("change", calculateReturnDateAndPrice);

        // Initialize form if duration has a default value
        if (durationSelect.value) {
            calculateReturnDateAndPrice();
        }
    }
    });