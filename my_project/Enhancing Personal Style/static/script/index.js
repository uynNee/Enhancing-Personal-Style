function showAdditionalFields(show) {
    const additionalFields = document.getElementById("additional-fields");
    const shapeGroup = document.getElementById("shape-group");
    if (show) {
        additionalFields.style.display = "block";
        shapeGroup.style.display = "none";
    } else {
        additionalFields.style.display = "none";
        shapeGroup.style.display = "block";
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