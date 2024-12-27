document.addEventListener('DOMContentLoaded', function () {

    // Filter form event handling
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        // Prevent default input event submission
        filterForm.addEventListener('input', function (event) {
            event.preventDefault();
        });

        // Form submission event
        filterForm.addEventListener('submit', function () {
            const spinner = document.getElementById('loading-spinner');
            if (spinner) {
                spinner.style.display = 'block'; // Show loading spinner
            }
        });
    }

    // Reset button functionality
    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function () {
            if (filterForm) {
                filterForm.reset(); // Reset all form fields
            }
        });
    }

    // Show error messages
    function showErrorMessage(message) {
        const errorMessageElement = document.getElementById('error-message');
        if (errorMessageElement) {
            errorMessageElement.textContent = message;
            errorMessageElement.style.display = 'block';
        }
    }

    // Year input handling
    const yearInput = document.getElementById('year');
    if (yearInput) {
        yearInput.addEventListener('input', function () {
            const form = document.getElementById('filter-form');
            if (form) {
                form.submit = function () {}; // Prevent auto-submit
            }
        });
    }

});
