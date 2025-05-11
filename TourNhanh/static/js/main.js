document.addEventListener('DOMContentLoaded', function() {
    // Function to handle sticky navigation
    function handleStickyNav() {
        const nav = document.querySelector('.navbar');
        if (nav) {
            if (window.scrollY > 100) {
                nav.classList.add('navbar-shrink');
            } else {
                nav.classList.remove('navbar-shrink');
            }
        }
    }

    // Add event listener for scroll
    window.addEventListener('scroll', handleStickyNav);

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    // Destination carousel
    const destinationCarousel = document.querySelector('#destinationCarousel');
    if (destinationCarousel) {
        new bootstrap.Carousel(destinationCarousel, {
            interval: 5000,
            wrap: true
        });
    }

    // Featured tours carousel
    const toursCarousel = document.querySelector('#featuredToursCarousel');
    if (toursCarousel) {
        new bootstrap.Carousel(toursCarousel, {
            interval: 3000,
            wrap: true
        });
    }

    // Handle search form submission
    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            // Validate the form before submission
            const destination = document.querySelector('#id_destination');
            const dateFrom = document.querySelector('#id_date_from');
            
            if (!destination.value && !dateFrom.value) {
                e.preventDefault();
                alert('Vui lòng chọn điểm đến hoặc ngày khởi hành.');
            }
        });
    }

    // Tour filter handling
    const filterForm = document.querySelector('#tourFilterForm');
    if (filterForm) {
        // Filter toggle for mobile
        const filterToggle = document.querySelector('#filterToggle');
        const filterContent = document.querySelector('#filterContent');
        
        if (filterToggle && filterContent) {
            filterToggle.addEventListener('click', function() {
                if (filterContent.style.display === 'none' || !filterContent.style.display) {
                    filterContent.style.display = 'block';
                    filterToggle.textContent = 'Ẩn bộ lọc';
                } else {
                    filterContent.style.display = 'none';
                    filterToggle.textContent = 'Hiện bộ lọc';
                }
            });
        }
        
        // Handle filter change
        const filterInputs = filterForm.querySelectorAll('input, select');
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // Handle price range input
    const priceRange = document.querySelector('#priceRange');
    const priceDisplay = document.querySelector('#priceDisplay');
    if (priceRange && priceDisplay) {
        priceRange.addEventListener('input', function() {
            const value = Number(priceRange.value).toLocaleString('vi-VN');
            priceDisplay.textContent = `${value} VNĐ`;
        });
    }

    // Initialize date pickers
    const datePickers = document.querySelectorAll('.datepicker');
    if (datePickers.length > 0) {
        datePickers.forEach(picker => {
            picker.addEventListener('focus', function() {
                this.type = 'date';
            });
            picker.addEventListener('blur', function() {
                if (!this.value) {
                    this.type = 'text';
                }
            });
        });
    }
});
