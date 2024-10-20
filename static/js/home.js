document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search-bar input');
    const productCards = document.querySelectorAll('.product-card');

    searchInput.addEventListener('input', function () {
        const searchText = this.value.toLowerCase();

        productCards.forEach(card => {
            const title = card.getAttribute('data-title').toLowerCase();
            if (title.includes(searchText)) {
                card.style.display = 'block'; // Show card if title matches
            } else {
                card.style.display = 'none'; // Hide card if no match
            }
        });
    });
});
