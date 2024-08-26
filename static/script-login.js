const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const profileLink = document.getElementById('profile-link');
const profileDropdown = document.querySelector('.profile-dropdown');
const usernameDisplay = document.getElementById('username-display');
const emailDisplay = document.getElementById('email-display');

loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  // Call API or perform login logic here
  localStorage.setItem('username', username);
  window.location.href = 'project.html';
});

signupForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  // Call API or perform signup logic here
  localStorage.setItem('username', username);
  localStorage.setItem('email', email);
  window.location.href = 'project.html';
});

profileLink.addEventListener('mouseover', () => {
  profileDropdown.style.display = 'block';
  usernameDisplay.textContent = `Username: ${localStorage.getItem('username')}`;
  emailDisplay.textContent = `Email: ${localStorage.getItem('email')}`;
});

profileLink.addEventListener('mouseout', () => {
  profileDropdown.style.display = 'none';
});
