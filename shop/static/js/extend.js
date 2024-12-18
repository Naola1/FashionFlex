function confirmExtension() {
    const extensionDays = parseInt(document.getElementById('extensionDays').value);

    fetch(`/rentals/${currentRentalId}/extend/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            days: extensionDays
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to extend the return date');
        }
        return response.json();
    })
    .then(data => {
        // Find the rental item card and update its return date
        const rentalCard = document.querySelector(`.rental-item[data-id='${currentRentalId}']`);
        if (rentalCard) {
            rentalCard.querySelector('.return-date').textContent = `Return Date: ${data.extended_return_date}`;
        }
        closeExtendModal();
    })
    .catch(error => {
        console.error('Error extending return date:', error);
        alert('Could not extend the return date. Please try again.');
    });
}