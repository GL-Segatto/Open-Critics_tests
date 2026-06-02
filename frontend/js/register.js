/**
 * Script para a página de cadastro
 */
document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById("registerForm");
  const togglePasswordBtn = document.getElementById("togglePassword");
  const togglePassword2Btn = document.getElementById("togglePassword2");
  const passwordField = document.getElementById("password");
  const password2Field = document.getElementById("password2");

  function setupPasswordToggle(button, field) {
    if (!button || !field) return;

    button.addEventListener("click", function () {
      const type =
        field.getAttribute("type") === "password" ? "text" : "password";
      field.setAttribute("type", type);

      this.querySelector("i").classList.toggle("fa-eye");
      this.querySelector("i").classList.toggle("fa-eye-slash");
    });
  }

  setupPasswordToggle(togglePasswordBtn, passwordField);
  setupPasswordToggle(togglePassword2Btn, password2Field);

  if (registerForm) {
    registerForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const username = document.getElementById("username").value.trim();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
      const password2 = document.getElementById("password2").value;

      if (!username) {
        showMessage("O nome de usuário é obrigatório", "error");
        return;
      }

      if (!email) {
        showMessage("O e-mail é obrigatório", "error");
        return;
      }

      if (password !== password2) {
        showMessage("As senhas não conferem", "error");
        return;
      }

      showMessage("Criando conta...", "info");

      ApiService.auth
        .register({ username, email, password, password2 })
        .then((response) => {
          showMessage("Conta criada com sucesso!", "success");

          localStorage.setItem("auth_token", response.token);
          localStorage.setItem("auth_username", response.user.username);
          localStorage.setItem("user_info", JSON.stringify(response.user));

          const expirationDate = new Date();
          expirationDate.setHours(expirationDate.getHours() + 1);
          localStorage.setItem(
            "auth_expiration",
            expirationDate.getTime().toString()
          );

          setTimeout(function () {
            window.location.href = "dashboard.html";
          }, 1000);
        })
        .catch((error) => {
          console.error("Erro no cadastro:", error);
          showMessage(error.message || "Erro ao criar conta", "error");
        });
    });
  }

  function showMessage(message, type) {
    const existingMessage = document.querySelector(".message");
    if (existingMessage) {
      existingMessage.remove();
    }

    const messageElement = document.createElement("div");
    messageElement.classList.add("message", type);
    messageElement.textContent = message;

    const loginContainer = document.querySelector(".login-container");
    loginContainer.insertBefore(messageElement, registerForm);

    if (type !== "info") {
      setTimeout(function () {
        messageElement.remove();
      }, 5000);
    }
  }
});
