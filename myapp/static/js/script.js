// document.addEventListener("DOMContentLoaded", function () {
//     showCategory('today');
// });

// // function showCategory(category){
// //     document.querySelectorAll('.category-section').forEach(section => {
// //         section.style.display = 'none';
// //     });

// //     document.getElementById(category).style.display = 'block';
// // }

// function showCategory(category){
//     if (document.querySelectorAll('.category-section.past').forEach(section => {
//         section.style.display = 'none';
//     }));
// }

document.addEventListener("DOMContentLoaded", function () {
    showCategory('today'); // 기본값: 오늘의 편지 보이기
});

function showCategory(category) {
    // 모든 편지 리스트 숨김 처리
    document.querySelectorAll('.category').forEach(el => {
        el.classList.remove('active');
    });

    // 선택된 카테고리만 보이도록 설정
    document.getElementById(category).classList.add('active');
}

