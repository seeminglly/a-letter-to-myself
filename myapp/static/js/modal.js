// modal.js
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".modalList").forEach(item => {
        item.addEventListener("click", function () {
            const letterId = this.getAttribute("data-id");
            console.log("Clicked Letter ID:", letterId);  // ✅ letterId 값 출력
            openLetter(letterId);
        });
    });
});

async function openLetter(letterId) {
    try {
        if (!letterId || letterId === "undefined") {
            console.error("에러: 잘못된 letterId 값");
            return;
        }

        console.log("Fetching letter with ID:", letterId);

        const response = await fetch(`/api/letters/${letterId}/`);
        if (!response.ok) {
            throw new Error("데이터를 가져오는 데 실패했습니다.");
        }

        const letter = await response.json();

        document.getElementById("modalTitle").textContent = letter.title;
        document.getElementById("modalDate").textContent = "📅 " + letter.letter_date;
        document.getElementById("modalContent").textContent = letter.content;

        document.getElementById("modalOverlay").style.display = "block";
        document.getElementById("letterModal").style.display = "block";
    } catch (error) {
        console.error("에러 발생:", error);
    }
}

function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
    document.getElementById("letterModal").style.display = "none";
}
