// Переключение между вкладками
const tabButtons = document.querySelectorAll(".tab-btn")
const tabContents = document.querySelectorAll(".tab-content")

tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const tabName = button.getAttribute("data-tab")

    tabButtons.forEach((btn) => btn.classList.remove("active"))
    tabContents.forEach((content) => content.classList.remove("active"))

    button.classList.add("active")
    document.getElementById(tabName).classList.add("active")
  })
})

const usernameInput = document.getElementById("register-username")
if (usernameInput) {
  usernameInput.addEventListener("input", validateUsername)
  usernameInput.addEventListener("focus", () => {
    document.getElementById("username-hint").style.display = "block"
  })
}

function validateUsername() {
  const username = usernameInput.value
  const requirements = {
    length: username.length >= 3 && username.length <= 20,
    chars: /^[a-zA-Z0-9_]+$/.test(username),
  }

  updateRequirementStatus("username-hint", requirements)
  return Object.values(requirements).every(Boolean)
}

const passwordInput = document.getElementById("register-password")
const confirmInput = document.getElementById("register-confirm")

if (passwordInput) {
  passwordInput.addEventListener("input", validatePassword)
  passwordInput.addEventListener("focus", () => {
    document.getElementById("password-hint").style.display = "block"
  })
}

if (confirmInput) {
  confirmInput.addEventListener("input", validatePasswordMatch)
  confirmInput.addEventListener("focus", () => {
    document.getElementById("confirm-hint").style.display = "block"
  })
}

function validatePassword() {
  const password = passwordInput.value
  const requirements = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
  }

  updateRequirementStatus("password-hint", requirements)

  if (confirmInput.value) {
    validatePasswordMatch()
  }

  return Object.values(requirements).every(Boolean)
}

function validatePasswordMatch() {
  const password = passwordInput.value
  const confirm = confirmInput.value

  if (!confirm) {
    document.getElementById("confirm-hint").style.display = "none"
    return false
  }

  const requirements = {
    match: password === confirm && confirm.length > 0,
  }

  updateRequirementStatus("confirm-hint", requirements)
  return requirements.match
}

function updateRequirementStatus(hintId, requirements) {
  const hint = document.getElementById(hintId)
  if (!hint) return

  Object.keys(requirements).forEach((key) => {
    const requirement = hint.querySelector(`[data-requirement="${key}"]`)
    if (requirement) {
      requirement.classList.remove("valid", "invalid")
      requirement.classList.add(requirements[key] ? "valid" : "invalid")

      const icon = requirement.querySelector(".icon")
      icon.textContent = requirements[key] ? "✓" : "✗"
    }
  })
}

// Обработка формы входа
document.getElementById("loginForm").addEventListener("submit", (e) => {
  e.preventDefault()

  const email = document.getElementById("login-email").value
  const password = document.getElementById("login-password").value

  console.log("Вход:", { email, password })
  alert(`Попытка входа с email: ${email}`)
})

document.getElementById("registerForm").addEventListener("submit", (e) => {
  e.preventDefault()

  const username = document.getElementById("register-username").value
  const name = document.getElementById("register-name").value
  const email = document.getElementById("register-email").value
  const password = document.getElementById("register-password").value
  const confirmPassword = document.getElementById("register-confirm").value

  // Validate username
  if (!validateUsername()) {
    alert("Имя пользователя не соответствует требованиям!")
    return
  }

  // Validate password
  if (!validatePassword()) {
    alert("Пароль не соответствует требованиям безопасности!")
    return
  }

  // Check password match
  if (password !== confirmPassword) {
    alert("Пароли не совпадают!")
    return
  }

  console.log("Регистрация:", { username, name, email, password })
  alert(`Регистрация пользователя: ${name} (${username})`)
})

// OAuth функции
function loginWithGoogle() {
  console.log("Вход через Google")
  alert("Перенаправление на Google OAuth...")
}

function loginWithGithub() {
  console.log("Вход через GitHub")
  alert("Перенаправление на GitHub OAuth...")
}

function loginWithFacebook() {
  console.log("Вход через Facebook")
  alert("Перенаправление на Facebook OAuth...")
}

function loginWithApple() {
  console.log("Вход через Apple")
  alert("Перенаправление на Apple OAuth...")
}
