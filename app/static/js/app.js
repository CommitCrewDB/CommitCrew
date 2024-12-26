document.addEventListener('DOMContentLoaded', function () {

    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        filterForm.addEventListener('input', function (event) {
            event.preventDefault();
        });
    }

    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function () {
            document.querySelector('.filter-form').reset();
        });
    }

    function showErrorMessage(message) {
        const errorMessageElement = document.getElementById('error-message');
        if (errorMessageElement) {
            errorMessageElement.textContent = message;
            errorMessageElement.style.display = 'block';
        }
    }

    document.addEventListener("DOMContentLoaded", function() {
        const yearInput = document.getElementById('year');
        const form = document.getElementById('filter-form');

        yearInput.addEventListener('input', function(event) {
            form.submit = function() {};
        });
    });
    
    const winsSlider = document.getElementById('wins');
    if (winsSlider) {
        const winsValue = document.getElementById('wins-value');
        winsSlider.addEventListener('input', function () {
            winsValue.textContent = winsSlider.value;
        });
    }

    filterForm?.addEventListener('submit', function () {
        document.getElementById('loading-spinner').style.display = 'block'; 
    });

    document.addEventListener('DOMContentLoaded', function () {
        // Handle "Sort By" change
        const radioButtons = document.querySelectorAll('input[name="sort_by"]');
        radioButtons.forEach(button => {
            button.addEventListener('change', function () {
                document.getElementById('filter-form').submit(); // Automatically submit the form on change
            });
        });
    });
    

});
