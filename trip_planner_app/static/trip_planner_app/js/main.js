// trip_planner_app/static/trip_planner_app/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // ... (existing code for downloadPdfButton, location detection) ...

    // --- Interactive Background Effect ---
    const backgroundElement = document.getElementById('interactive-background');
    if (backgroundElement) {
        // Use hardcoded static paths directly
        const backgroundImages = [
            '/static/trip_planner_app/images/bg1.jpg',
            '/static/trip_planner_app/images/bg2.jpg',
            '/static/trip_planner_app/images/bg3.jpg',
            '/static/trip_planner_app/images/bg4.jpg'
            // Add more images as needed
        ];

        let currentIndex = 0;

        function changeBackground() {
            backgroundElement.style.backgroundImage = `url('${backgroundImages[currentIndex]}')`;
            // Trigger reflow to restart animation for each new image
            backgroundElement.style.animation = 'none';
            void backgroundElement.offsetWidth; 
            backgroundElement.style.animation = 'fadeZoom 20s infinite alternate forwards';

            currentIndex = (currentIndex + 1) % backgroundImages.length;
        }

        // Set initial background immediately
        changeBackground();

        // Change background every 8 seconds (adjust timing as desired)
        setInterval(changeBackground, 8000); 
    }

    // ... (existing code for form submission loading state, input field focus, checkbox/radio hover) ...

    // --- Form Submission Loading State ---
    const tripPlanningForm = document.getElementById('trip-planning-form');
    const generateButton = document.getElementById('generate-itinerary-btn');

    if (tripPlanningForm && generateButton) {
        tripPlanningForm.addEventListener('submit', function() {
            generateButton.disabled = true;
            generateButton.classList.add('loading');
            generateButton.querySelector('.button-text').textContent = 'Generating...';
            generateButton.querySelector('.spinner-border').classList.remove('d-none');
        });
    }

    // --- Input Field Focus Effect ---
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        input.addEventListener('focus', () => {
            input.closest('.col-md-6, .mb-4').querySelector('.form-label').style.color = '#4a54ff';
        });
        input.addEventListener('blur', () => {
            input.closest('.col-md-6, .mb-4').querySelector('.form-label').style.color = '#34495e';
        });
    });

    // --- Checkbox/Radio Hover Effect ---
    document.querySelectorAll('.form-check').forEach(check => {
        const input = check.querySelector('.form-check-input');
        if (input) {
            check.addEventListener('mouseenter', () => {
                if (!input.checked) {
                    check.style.borderColor = '#9bb2ff'; // Lighter blue on hover if not checked
                }
            });
            check.addEventListener('mouseleave', () => {
                if (!input.checked) {
                    check.style.borderColor = '#dde3ea'; // Revert if not checked
                }
            });
        }
    });

});