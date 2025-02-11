document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menuToggle");
  const navLinks = document.querySelector(".nav-links");

  menuToggle.addEventListener("click", function () {
      navLinks.classList.toggle("active");
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const email = form.email.value.trim();
      const password = form.password.value;
      
      const emailError = document.getElementById("email-error");
      const passwordError = document.getElementById("password-error");
      emailError.textContent = "";
      passwordError.textContent = "";

      try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        console.log("Response:", data);
        if (!response.ok) {
          if (data.error === "Email not found") {
              emailError.textContent = " Email does not exist.";
              emailError.style.display = "block";
          } else if (data.error === "Incorrect password") {
              passwordError.textContent = " Incorrect password.";
              passwordError.style.display = "block";
          }
          return;
      }

        if (data.success) {
            window.location.href = data.redirect;
            console.log("sucess")
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error("Login Error:", error);
        alert("An error occurred while logging in.");
    }
});
});
   