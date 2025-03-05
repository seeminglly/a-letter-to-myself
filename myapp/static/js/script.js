document.addEventListener("DOMContentLoaded", function () {
    showCategory('today');
});

function showCategory(category){
    document.querySelectorAll('.category-section').forEach(section => {
        section.style.display = 'none';
    });

    document.getElementById(category).style.display = 'block';
}