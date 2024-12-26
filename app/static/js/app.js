document.addEventListener('DOMContentLoaded', function () {

    // Dinamik Form Gönderme
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        // Formun otomatik olarak gönderilmesini engelle
        filterForm.addEventListener('input', function (event) {
            event.preventDefault(); // Formun otomatik olarak gönderilmesini engeller
        });
    }

    // Reset butonu ile formu sıfırlama
    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function () {
            document.querySelector('.filter-form').reset();
        });
    }

    // Error Message: Dinamik hata mesajlarını gösterme
    function showErrorMessage(message) {
        const errorMessageElement = document.getElementById('error-message');
        if (errorMessageElement) {
            errorMessageElement.textContent = message;
            errorMessageElement.style.display = 'block';
        }
    }

    // Form verisi doğrulama (Yıl veya Takım adı girmeden filtrelemeyi engelleme)
    document.addEventListener("DOMContentLoaded", function() {
        const yearInput = document.getElementById('year');
        const form = document.getElementById('filter-form');
    
        // Listen for input in the year field to prevent auto-submit
        yearInput.addEventListener('input', function(event) {
            // Prevent form submission on year input change
            form.submit = function() {
                // Only submit form when filter button is clicked
            };
        });
    });
    

    // Wins Slider: Slider değeri dinamik olarak gösterme
    const winsSlider = document.getElementById('wins');
    if (winsSlider) {
        const winsValue = document.getElementById('wins-value');
        winsSlider.addEventListener('input', function () {
            winsValue.textContent = winsSlider.value;
            // Filtreyi anında uygula
        });
    }

    // Loading Spinner: Form gönderildiğinde yükleme simgesini gösterme
    filterForm?.addEventListener('submit', function () {
        document.getElementById('loading-spinner').style.display = 'block'; // Spinner'ı göster
    });

});
