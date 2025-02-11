document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.querySelector(".nav-links");

    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });
});
document.addEventListener("DOMContentLoaded", function () {
    fetch("../../users.json")
        .then(response => response.json())
        .then(data => {
            const user = data.users[0]; // Load first user
console.log('user')
            document.getElementById("user-name").textContent = user.name;
            document.getElementById("user-email").innerHTML = `<strong> Email:</strong> ${user.email}`;
            document.getElementById("user-location").innerHTML = `<strong> Location:</strong> ${user.location}`;
            document.getElementById("user-bio").textContent = user.bio;
            document.getElementById("profile-img").src = user.profilePicture || "../static/imges/default.jpg";

            document.getElementById("displayName").value = user.displayName;
            document.getElementById("email").value = user.email;
            document.getElementById("Location").value = user.location;
            document.getElementById("bio").value = user.bio;
        })
        .catch(error => console.error("Error loading user data:", error));

    /**  Open and Close Modal */
    window.openModal = function () {
        document.getElementById("editModal").style.display = "block";
    };

    window.closeModal = function () {
        document.getElementById("editModal").style.display = "none";
    };

    /**  **Validate Form Inputs** */
    function validateForm() {
        let isValid = true;
        let errorMessages = [];

        const editName = document.getElementById("displayName").value.trim();
        const editEmail = document.getElementById("email").value.trim();
        const editLocation = document.getElementById("Location").value.trim();
        const editBio = document.getElementById("bio").value.trim();

        if (editName === "") errorMessages.push("Name cannot be empty.");
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(editEmail)) errorMessages.push("Invalid email format.");
        if (editLocation === "") errorMessages.push("Location cannot be empty.");
        if (editBio.length < 10) errorMessages.push("Bio must be at least 10 characters long.");

        if (errorMessages.length > 0) {
            alert("Error:\n" + errorMessages.join("\n"));
            return false;
        }

        return true;
    }

    /**Save Edited Profile */
    window.saveProfile = function () {
        if (!validateForm()) return;

        document.getElementById("user-name").textContent = document.getElementById("displayName").value;
        document.getElementById("user-email").innerHTML = `<strong>Email:</strong> ${document.getElementById("email").value}`;
        document.getElementById("user-location").innerHTML = `<strong> Location:</strong> ${document.getElementById("Location").value}`;
        document.getElementById("user-bio").textContent =`<strong> bio:</strong> ${document.getElementById("bio").value}`;

        closeModal();
        alert("Profile updated successfully!");
    };

    /**  Handle Profile Picture Upload */
    document.getElementById("fileInput").addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById("profile-img").src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
