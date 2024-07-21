document.addEventListener('DOMContentLoaded', function() {
    console.log('recommend.js loaded and DOM fully loaded');
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const form = button.closest('.like-form');
            const productId = form.getAttribute('data-product-id');
            const liked = button.querySelector('img').alt === 'Unlike';
            const url = form.getAttribute('action');

            const csrfTokenElement = document.querySelector('input[name="csrf_token"]');
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ product_id: productId, liked: !liked })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const img = button.querySelector('img');
                    if (liked) {
                        img.src = '/static/assets/like/unlike.svg';
                        img.alt = 'Like';
                        button.title = 'You haven\'t liked this item!';
                    } else {
                        img.src = '/static/assets/like/like.svg';
                        img.alt = 'Unlike';
                        button.title = 'You liked this item!';
                    }
                }
            });
        });
    });
});