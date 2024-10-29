document.getElementById('review-form').addEventListener('submit', function (event) {
    const rating = document.getElementById('rating').value;
    const review = document.getElementById('review').value;

    // Prevent the form submission if rating is not valid
    if (rating < 1 || rating > 5) {
        alert("Please enter a valid rating between 1 and 5.");
        event.preventDefault();
    }

    if (review.trim() === "") {
        alert("Please enter a review text.");
        event.preventDefault();
    }
});


