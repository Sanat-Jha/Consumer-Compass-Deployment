// Function to show the selected reviews section
function showReviews(platform) {
    // Hide all review sections initially
    document.getElementById('amazon-reviews').style.display = 'none';
    document.getElementById('flipkart-reviews').style.display = 'none';
    document.getElementById('cc-reviews').style.display = 'none';

    // Show the selected reviews section
    if (platform === 'amazon') {
        console.log(platform)
        document.getElementById('amazon-reviews').style.display = 'block';
    } else if (platform === 'flipkart') {
        document.getElementById('flipkart-reviews').style.display = 'block';
    } else if (platform === 'cc') {
        document.getElementById('cc-reviews').style.display = 'block';
    }
}

// On page load, default to showing CC Reviews
window.onload = function () {
    showReviews('cc');
};


// AJAX function to handle form submission and update review content on the page

// Function to open the edit modal and populate it with existing review content
function openEditModal(content) {
    document.getElementById('edit-review-content').value = content;
    document.getElementById('editReviewModal').style.display = 'block';
}

// Function to close the edit modal
function closeEditModal() {
    document.getElementById('editReviewModal').style.display = 'none';
}