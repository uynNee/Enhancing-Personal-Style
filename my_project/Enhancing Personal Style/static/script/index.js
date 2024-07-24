function showExplanation(triggerElement, shape) {
    const explanationBoxes = document.querySelectorAll('.explanation-box');
    explanationBoxes.forEach(box => {
        box.style.display = 'none';
        const existingImgs = box.querySelectorAll('img');
        existingImgs.forEach(img => img.remove());
    });
    const explanationBoxId = `${shape}-explanation`;
    const explanationBox = document.getElementById(explanationBoxId);
    if (!explanationBox) {
        console.error('Explanation box not found for:', shape);
        return;
    }
    const imagePaths = [
        `static/assets/body_silhouette/${shape.toLowerCase()}_man.png`,
        `static/assets/body_silhouette/${shape.toLowerCase()}_woman.png`
    ];
    imagePaths.forEach((path, index) => {
        const imgElement = document.createElement('img');
        imgElement.src = path;
        imgElement.alt = shape;
        imgElement.classList.add(index === 0 ? 'man-image' : 'woman-image');
        explanationBox.appendChild(imgElement);
    });
    explanationBox.style.display = 'block';
    explanationBox.style.top = `20px`;
    const triggerRect = triggerElement.getBoundingClientRect();
    explanationBox.style.left = `${triggerRect.right + 45}px`;
}

const colorSwatches = {
    Spring: [
        "rgba(255, 223, 186, 1)", // Warm Spring Bright Pale
        "rgba(255, 206, 162, 1)", // Warm Spring Bright Fair
        "rgba(244, 180, 137, 1)", // Warm Spring Bright Medium
        "rgba(232, 149, 111, 1)", // Warm Spring Bright Tan
        "rgba(217, 116, 84, 1)",  // Warm Spring Bright Dark
        "rgba(255, 239, 213, 1)", // Warm Spring Light Pale
        "rgba(255, 224, 189, 1)", // Warm Spring Light Fair
        "rgba(244, 204, 163, 1)", // Warm Spring Light Medium
        "rgba(232, 185, 137, 1)", // Warm Spring Light Tan
        "rgba(217, 165, 111, 1)"  // Warm Spring Light Dark
    ],
    Summer: [
        "rgba(255, 228, 196, 1)", // Cool Summer Light Pale
        "rgba(248, 212, 180, 1)", // Cool Summer Light Fair
        "rgba(233, 186, 159, 1)", // Cool Summer Light Medium
        "rgba(221, 160, 140, 1)", // Cool Summer Light Tan
        "rgba(204, 136, 120, 1)", // Cool Summer Light Dark
        "rgba(255, 224, 189, 1)", // Cool Summer Mute Pale
        "rgba(245, 203, 174, 1)", // Cool Summer Mute Fair
        "rgba(224, 182, 155, 1)", // Cool Summer Mute Medium
        "rgba(210, 159, 138, 1)", // Cool Summer Mute Tan
        "rgba(193, 137, 118, 1)"  // Cool Summer Mute Dark
    ],
    Autumn: [
        "rgba(255, 204, 153, 1)", // Warm Autumn Mute Pale
        "rgba(244, 184, 143, 1)", // Warm Autumn Mute Fair
        "rgba(232, 164, 123, 1)", // Warm Autumn Mute Medium
        "rgba(213, 143, 103, 1)", // Warm Autumn Mute Tan
        "rgba(193, 123, 85, 1)",  // Warm Autumn Mute Dark
        "rgba(255, 195, 148, 1)", // Warm Autumn Deep Pale
        "rgba(237, 177, 135, 1)", // Warm Autumn Deep Fair
        "rgba(216, 157, 119, 1)", // Warm Autumn Deep Medium
        "rgba(196, 137, 99, 1)",  // Warm Autumn Deep Tan
        "rgba(176, 117, 82, 1)"   // Warm Autumn Deep Dark
    ],
    Winter: [
        "rgba(255, 239, 213, 1)", // Cool Winter Light Pale
        "rgba(248, 222, 191, 1)", // Cool Winter Light Fair
        "rgba(235, 195, 164, 1)", // Cool Winter Light Medium
        "rgba(220, 178, 147, 1)", // Cool Winter Light Tan
        "rgba(204, 157, 131, 1)", // Cool Winter Light Dark
        "rgba(193, 116, 84, 1)",  // Cool Winter Deep Pale
        "rgba(174, 106, 74, 1)",  // Cool Winter Deep Fair
        "rgba(155, 96, 64, 1)",   // Cool Winter Deep Medium
        "rgba(136, 86, 54, 1)",   // Cool Winter Deep Tan
        "rgba(117, 76, 44, 1)"    // Cool Winter Deep Dark
    ]
};

function getSwatchDescriptions(color) {
    const descriptions = {
        Spring: {
            firstBold: "Warm Spring bright: ",
            first: "Includes pure, high-chroma colors with a yellow base. These colors are vivid and clear, enhancing the skin's brightness.",
            lastBold: "Warm Spring light:",
            last: "Features low-chroma and high-value colors with a yellow base. These colors are softer and lighter, blending well with the skin's natural warmth."
        },
        Summer: {
            firstBold: "Cool Summer light: ",
            first: "Contains low-chroma and high-value colors with a blue base. These colors are gentle and light, enhancing the coolness of the skin.",
            lastBold: "Cool Summer mute:",
            last: "Includes low-chroma and medium-to-low value colors with a blue base. These colors are more muted, providing a subtle and understated look."
        },
        Autumn: {
            firstBold: "Warm Autumn mute: ",
            first: "Consists of medium-to-low chroma and medium-to-low value colors with a yellow base. These colors have a touch of gray, giving a more subdued and natural appearance.",
            lastBold: "Warm Autumn deep:",
            last: "Features medium-to-low chroma and medium-to-low value colors with a yellow base. These colors are darker and richer, adding depth to the skin's warm undertone."
        },
        Winter: {
            firstBold: "Cool Winter bright: ",
            first: "Features high-chroma and pure colors with a blue base. These colors are vivid and clear, enhancing the skin's brightness and coolness.",
            lastBold: "Cool Winter deep:",
            last: "Contains high-to-low chroma and low-value colors with a blue base. These colors are dark and intense, providing a dramatic contrast to the skin."
        }
    };
    return descriptions[color];
}

function showSwatches(triggerElement, color) {
    const explanationBoxes = document.querySelectorAll('.explanation-box');
    explanationBoxes.forEach(box => {
        box.style.display = 'none';
        const colorContainer = box.querySelector('.color-container');
        if (colorContainer) {
            colorContainer.remove();
        }
    });
    const explanationBoxId = `${color}-swatches`;
    const explanationBox = document.getElementById(explanationBoxId);
    if (!explanationBox) {
        console.error('Swatches box not found for:', color);
        return;
    }
    const colors = colorSwatches[color];
    if (!colors) {
        console.error('Color swatches not found for:', color);
        return;
    }
    const description = getSwatchDescriptions(color);
    explanationBox.innerHTML = `
        <h3>Skin swatches for Skin Tone ${color}</h3>
        <p><strong>Description:</strong> ${description.first}</p>
        <p><strong>${description.firstBold}</strong> ${description.first}</p>
    `;
    const firstColorContainer = document.createElement('div');
    firstColorContainer.classList.add('color-container');
    colors.slice(0, 5).forEach(colorValue => {
        const colorSquare = document.createElement('div');
        colorSquare.classList.add('color-box');
        colorSquare.style.backgroundColor = colorValue;
        firstColorContainer.appendChild(colorSquare);
    });
    explanationBox.appendChild(firstColorContainer);
    const lastDescriptionHTML = `
        <p><strong>${description.lastBold}</strong> ${description.last}</p>
    `;
    explanationBox.innerHTML += lastDescriptionHTML;
    const lastColorContainer = document.createElement('div');
    lastColorContainer.classList.add('color-container');
    colors.slice(-5).forEach(colorValue => {
        const colorSquare = document.createElement('div');
        colorSquare.classList.add('color-box');
        colorSquare.style.backgroundColor = colorValue;
        lastColorContainer.appendChild(colorSquare);
    });
    explanationBox.appendChild(lastColorContainer);
    explanationBox.style.display = 'block';
    explanationBox.style.top = `20px`;
    const triggerRect = triggerElement.getBoundingClientRect();
    explanationBox.style.left = `${triggerRect.right + 45}px`;
}

function closeExplanationBoxes() {
    const explanationBoxes = document.querySelectorAll('.explanation-box');
    explanationBoxes.forEach(box => {
        box.style.display = 'none';
    });
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
    const isAnyFieldInvalid = Array.from(numberFields).some(field => field.value < 0);

    if (isAnyFieldInvalid) {
        alert('Please ensure all number fields have values greater than or equal to 0.');
        return;
    }

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
    closeExplanationBoxes();
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