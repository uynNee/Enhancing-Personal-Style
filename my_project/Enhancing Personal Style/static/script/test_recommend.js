// /static/script/test_recommend.js
document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;
    const productContainer = document.getElementById('product-container');
    const ratingForm = document.getElementById('rating-form');
    const nextButton = document.getElementById('next-product-btn');
    const prevButton = document.getElementById('previous-product-btn');
    const messageContainer = document.getElementById('message-container'); // Message container
    let currentFilteringType = '';
    const userId = document.querySelector('meta[name="user-id"]').getAttribute('content');
    const preloadImages = () => {
        products.forEach(product => {
            const img = new Image();
            img.src = product.link;
        });
    };
    function showProduct(index) {
        if (index < 0 || index >= products.length) return;
        const product = products[index];
        productContainer.innerHTML = `
            <img src="${product.link}" alt="${product.productDisplayName}" style="height:250px;width:auto;padding: 10px 0;">
            <p class="product-element"><strong>${product.productDisplayName}</strong></p>
            <p class="product-element"><strong>Product's Color:</strong> ${product.baseColour}</p>
            <p class="product-element"><strong>Product's Season:</strong> ${product.season}</p>
            <p class="product-element"><strong>Product's Usage:</strong> ${product.usage}</p>
        `;
        document.getElementById('product-id').value = product.id;
        currentFilteringType = product.filtering;
        const loadingPlaceholder = document.getElementById('loading-placeholder');
        if (loadingPlaceholder) {
            loadingPlaceholder.style.display = 'none';
        }
        fetchUserRating(product.id);
    }
    function fetchUserRating(productId) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch(`/get_rating?user_id=${userId}&product_id=${productId}&filtering=${currentFilteringType}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.rating) {
                const rating = data.rating;
                document.getElementById('likert-scale').value = rating.likert_scale;
                document.getElementById('matching_slider').value = rating.matching_slider;
                document.getElementById('shape-slider').value = rating.shape_slider;
                document.getElementById('skin-tone-slider').value = rating.skin_tone_slider;
            } else {
                resetSliders();
            }
        })
        .catch(error => {
            console.error('Error fetching rating:', error);
            resetSliders();
        });
    }
    function resetSliders() {
        document.getElementById('likert-scale').value = 3;
        document.getElementById('matching_slider').value = 3;
        document.getElementById('shape-slider').value = 3;
        document.getElementById('skin-tone-slider').value = 3;
    }
    function handleFormSubmit(event) {
        event.preventDefault();
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const formData = new FormData(ratingForm);
        const data = Object.fromEntries(formData.entries());
        data.filtering = currentFilteringType;
        fetch('/save_rating', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showMessage('Rated successfully!', 'green');
                nextProduct();
            } else {
                showMessage('Failed to save rating: ' + data.message, 'red');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An error occurred: ' + error.message, 'red');
        });
    }
    function showMessage(message, color) {
        messageContainer.innerText = message;
        messageContainer.style.color = color;
        messageContainer.style.display = 'block';
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 3000); // Hide the message after 3 seconds
    }
    function nextProduct() {
        if (currentIndex < products.length - 1) {
            currentIndex++;
            showProduct(currentIndex);
        } else {
            alert('You have reached the end of the product list.');
        }
    }
    function prevProduct() {
        if (currentIndex > 0) {
            currentIndex--;
            showProduct(currentIndex);
        }
    }
    ratingForm.addEventListener('submit', handleFormSubmit);
    nextButton.addEventListener('click', nextProduct);
    prevButton.addEventListener('click', prevProduct);
    preloadImages();
    showProduct(currentIndex);
});