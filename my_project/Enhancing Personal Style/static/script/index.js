function showExplanation(triggerElement, shape) {
    const explanationBoxes = document.querySelectorAll('.explanation-box');
    explanationBoxes.forEach(box => {
        box.style.display = 'none';
        const existingImg = box.querySelector('img');
        if (existingImg) {
            existingImg.remove();
        }
    });
    const explanationBoxId = `${shape}-explanation`;
    const explanationBox = document.getElementById(explanationBoxId);
    if (!explanationBox) {
        console.error('Explanation box not found for:', shape);
        return;
    }
    const imagePath = `static/assets/body_silhouette/${shape.toLowerCase()}.png`;
    const imgElement = document.createElement('img');
    imgElement.src = imagePath;
    imgElement.alt = shape;
    const titleElement = explanationBox.querySelector('h3');
    titleElement.insertAdjacentElement('afterend', imgElement);
    const screenHeight = window.innerHeight;
    const boxHeight = explanationBox.offsetHeight;
    const middleHeight = (screenHeight / 2) - (boxHeight / 2);
    explanationBox.style.display = 'block';
    explanationBox.style.top = `${middleHeight}px`;
    const triggerRect = triggerElement.getBoundingClientRect();
    explanationBox.style.left = `${triggerRect.right + 45}px`;
}

function showAdditionalFields(show) {
    const additionalFields = document.getElementById('additional-fields');
    const shapeGroup = document.getElementById('shape-group');
    const shapeRadioButtons = shapeGroup.querySelectorAll('input[type="radio"]');
    const numberFields = additionalFields.querySelectorAll('input[type="number"]');

    if (show) {
        additionalFields.style.display = 'block';
        shapeGroup.style.display = 'none';
        shapeRadioButtons.forEach(radio => radio.removeAttribute('required'));
        numberFields.forEach(field => field.setAttribute('required', 'true'));
    } else {
        additionalFields.style.display = 'none';
        shapeGroup.style.display = 'block';
        shapeRadioButtons.forEach(radio => radio.setAttribute('required', 'true'));
        numberFields.forEach(field => field.removeAttribute('required'));
    }
}

let currentPage = 1;
const totalPages = 3;

function showPage(pageNumber) {
    const pages = document.querySelectorAll('.form-page');
    pages.forEach((page, index) => {
        page.classList.remove('active');
        if (index + 1 === pageNumber) {
            page.classList.add('active');
        }
    });
}

function nextPage() {
    const currentPageElement = document.querySelector('.form-page.active');
    const radioButtons = currentPageElement.querySelectorAll('input[type="radio"]');
    const numberFields = currentPageElement.querySelectorAll('input[type="number"]');
    const isChecked = Array.from(radioButtons).some(radio => radio.checked);

    if (!isChecked) {
        alert('Please make a selection before proceeding.');
        return;
    }

    const predictYes = document.querySelector('input[name="predict"][value="yes"]').checked;
    if (predictYes) {
        const allFilled = Array.from(numberFields).every(field => field.value.trim() !== '');
        if (!allFilled) {
            alert('Please fill in all the measurements before proceeding.');
            return;
        }
    } else {
        const bodyShapeSelected = Array.from(radioButtons).some(radio => radio.checked && radio.name === 'shape');
        if (!bodyShapeSelected && currentPageElement.id === 'page1') {
            alert('Please select a body shape before proceeding.');
            return;
        }
    }

    if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    showPage(currentPage);
    const radioButtons = document.querySelectorAll('.radio-button');
    radioButtons.forEach(button => {
        button.addEventListener('click', () => {
            radioButtons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
        });
    });
});