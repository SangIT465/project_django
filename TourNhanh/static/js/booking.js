document.addEventListener('DOMContentLoaded', function() {
    // Function to calculate total price
    function calculateTotal() {
        const adultCount = parseInt(document.getElementById('id_adults').value) || 0;
        const childCount = parseInt(document.getElementById('id_children').value) || 0;
        
        // Get base prices from data attributes
        const adultPrice = parseFloat(document.getElementById('adultPrice').dataset.price) || 0;
        const childPrice = adultPrice * 0.7; // 70% of adult price
        
        // Calculate totals
        const adultTotal = adultCount * adultPrice;
        const childTotal = childCount * childPrice;
        const grandTotal = adultTotal + childTotal;
        
        // Update display
        document.getElementById('adultSubtotal').textContent = adultTotal.toLocaleString('vi-VN') + ' VNĐ';
        document.getElementById('childSubtotal').textContent = childTotal.toLocaleString('vi-VN') + ' VNĐ';
        document.getElementById('grandTotal').textContent = grandTotal.toLocaleString('vi-VN') + ' VNĐ';
    }
    
    // Initialize price calculation
    const adultsInput = document.getElementById('id_adults');
    const childrenInput = document.getElementById('id_children');
    
    if (adultsInput && childrenInput) {
        adultsInput.addEventListener('change', calculateTotal);
        childrenInput.addEventListener('change', calculateTotal);
        
        // Calculate initial total
        calculateTotal();
    }
    
    // Tour date selection
    const dateSelect = document.getElementById('tourDateSelect');
    if (dateSelect) {
        dateSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const datePrice = selectedOption.dataset.price;
            const availableSeats = selectedOption.dataset.seats;
            
            // Update price information
            if (datePrice) {
                document.getElementById('adultPrice').dataset.price = datePrice;
                document.getElementById('adultPrice').textContent = parseInt(datePrice).toLocaleString('vi-VN') + ' VNĐ';
                
                // Recalculate total
                calculateTotal();
            }
            
            // Update available seats information
            if (availableSeats) {
                document.getElementById('availableSeats').textContent = availableSeats;
            }
        });
    }
    
    // Form validation
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const fullName = document.getElementById('id_full_name').value;
            const email = document.getElementById('id_email').value;
            const phone = document.getElementById('id_phone').value;
            const adults = document.getElementById('id_adults').value;
            
            if (!fullName || !email || !phone || !adults || adults < 1) {
                e.preventDefault();
                alert('Vui lòng điền đầy đủ thông tin và ít nhất 1 người lớn.');
                return false;
            }
            
            // Validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                alert('Vui lòng nhập đúng định dạng email.');
                return false;
            }
            
            // Validate phone number format
            const phoneRegex = /^[0-9]{10,11}$/;
            if (!phoneRegex.test(phone)) {
                e.preventDefault();
                alert('Vui lòng nhập đúng số điện thoại (10-11 số).');
                return false;
            }
        });
    }
    
    // Payment method selection
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    const paymentDetails = document.querySelectorAll('.payment-details');
    
    if (paymentMethods.length > 0 && paymentDetails.length > 0) {
        paymentMethods.forEach(method => {
            method.addEventListener('change', function() {
                const selectedMethod = this.value;
                
                // Hide all details first
                paymentDetails.forEach(detail => {
                    detail.style.display = 'none';
                });
                
                // Show the selected method's details
                const selectedDetail = document.getElementById(`${selectedMethod}_details`);
                if (selectedDetail) {
                    selectedDetail.style.display = 'block';
                }
            });
        });
        
        // Show the initially selected payment method details
        const checkedMethod = document.querySelector('input[name="payment_method"]:checked');
        if (checkedMethod) {
            const initialMethod = checkedMethod.value;
            const initialDetail = document.getElementById(`${initialMethod}_details`);
            if (initialDetail) {
                initialDetail.style.display = 'block';
            }
        }
    }
    
    // Online payment simulation
    const payNowBtn = document.getElementById('payNowBtn');
    const paymentForm = document.getElementById('onlinePaymentForm');
    
    if (payNowBtn && paymentForm) {
        payNowBtn.addEventListener('click', function() {
            // Simulate processing
            this.textContent = 'Đang xử lý...';
            this.disabled = true;
            
            // Submit the form after 2 seconds (simulating payment processing)
            setTimeout(() => {
                paymentForm.submit();
            }, 2000);
        });
    }
});
