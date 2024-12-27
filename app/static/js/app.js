// app.js
document.addEventListener('DOMContentLoaded', function () {
    // Reset Button Functionality
    const resetButton = document.querySelector('button[type="reset"]');
    const formInputs = document.querySelectorAll('.filter-form input, .filter-form select');

    if (resetButton) {
        resetButton.addEventListener('click', () => {
            formInputs.forEach(input => {
                if (input.type === 'checkbox') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });
        });
    }

    // Search Functionality Feedback
    const searchForm = document.querySelector('.search-form');
    const searchInput = searchForm.querySelector('input[name="search"]');

    if (searchForm) {
        searchForm.addEventListener('submit', (event) => {
            if (searchInput.value.trim() === '') {
                event.preventDefault();
                alert('Please enter a valid search term.');
            }
        });
    }

    // Filter Feedback
    const filterForm = document.querySelector('#filter-form');

    if (filterForm) {
        filterForm.addEventListener('submit', (event) => {
            const yearInput = document.querySelector('#year');
            const yearValue = yearInput.value.trim();

            if (yearValue && isNaN(yearValue)) {
                event.preventDefault();
                alert('Year must be a numeric value.');
            }
        });
    }

    // Smooth Scrolling to Results
    const resultsTable = document.querySelector('table.table');
    if (resultsTable) {
        resultsTable.scrollIntoView({ behavior: 'smooth' });
    }
});
