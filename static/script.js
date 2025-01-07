document.addEventListener('DOMContentLoaded', () => {
    const h1bForm = document.getElementById('h1bForm');
    const resultSection = document.getElementById('result-section'); // Doğru şekilde seçildi

    h1bForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = {
            firstName: document.getElementById('firstName').value,
            lastName: document.getElementById('lastName').value,
            jobTitle: document.getElementById('jobTitle').value,
            company: document.getElementById('company').value,
            worksite: document.getElementById('worksite').value,
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const result = await response.json();

            if (response.ok) {
                // Sonucu sayfada göster
                resultSection.innerHTML = `<p>${result.message}</p>`;
                resultSection.style.border = "1px solid #3498db";
                resultSection.style.padding = "10px";
                resultSection.style.marginTop = "20px";
                resultSection.style.borderRadius = "5px";
            } else {
                resultSection.innerHTML = `<p>Error: ${result.error}</p>`;
            }
        } catch (error) {
            resultSection.innerHTML = `<p>An unexpected error occurred: ${error.message}</p>`;
        }

        // Formu sıfırla
        h1bForm.reset();
    });

    // Navigation functions
    window.goToForm = () => {
        document.getElementById('info-section').style.display = 'none';
        document.getElementById('form-section').style.display = 'block';
    };

    window.goToInfo = () => {
        document.getElementById('form-section').style.display = 'none';
        document.getElementById('info-section').style.display = 'block';
    };
});
