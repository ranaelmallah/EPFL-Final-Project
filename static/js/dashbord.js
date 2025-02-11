document.addEventListener("DOMContentLoaded", function () {
    const houseForm = document.getElementById("houseForm");
    const houseTableBody = document.getElementById("houseTableBody");

    function loadHouses() {
        fetch("/view_houses")
            .then(response => response.text())
            .then(html => {
                const tempDiv = document.createElement("div");
                tempDiv.innerHTML = html;
                const newTableBody = tempDiv.querySelector("#houseTableBody");

                if (newTableBody) {
                    houseTableBody.innerHTML = newTableBody.innerHTML;
                }
            })
            .catch(error => console.error("Error loading houses:", error));
    }

    houseForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(houseForm);

        fetch("/add_house", {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    loadHouses();
                    houseForm.reset();
                    closeModal("addModal")
                } else {
                    return response.text();
                }

            })
            .then(errorMessage => {
                if (errorMessage) alert(errorMessage);
            })
            .catch(error => console.error("Error adding house:", error));
    });


    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-btn")) {
            const houseId = event.target.dataset.id;

            fetch(`/delete_house/${houseId}`, {
                    method: "POST"
                })
                .then(response => {
                    if (response.ok) {
                        loadHouses();
                    } else {
                        alert("Error deleting house");
                    }
                })
                .catch(error => console.error("Error deleting house:", error));
        }
    });
    loadHouses();
});

function openModal(id) {
    document.getElementById(id).style.display = "block";
}

function closeModal(id) {
    document.getElementById(id).style.display = "none";
}