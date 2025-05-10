document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');

    // Flash messages handling
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });

    // View password button
    const viewPasswordBtn = document.querySelector('.view-password');
    console.log('View password button:', viewPasswordBtn);

    if (viewPasswordBtn) {
        viewPasswordBtn.addEventListener('click', function(e) {
            console.log('Button clicked');
            e.preventDefault();
            
            const passwordField = document.getElementById('password');
            console.log('Password field:', passwordField);
            
            const icon = this.querySelector('i');
            console.log('Icon:', icon);
            
            if (passwordField.type === 'password') {
                console.log('Changing to text');
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                console.log('Changing to password');
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    }

    // Password strength evaluation
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', async function() {
            const password = this.value;
            if (!password) {
                resetPasswordStrength();
                return;
            }

            try {
                const response = await fetch('/evaluate_password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ password: password })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                if (data.error) {
                    throw new Error(data.error);
                }

                updatePasswordStrength(data);
            } catch (error) {
                console.error('Error:', error);
                showError('Error evaluating password strength');
                resetPasswordStrength();
            }
        });
    }

    // Password generator
    const generatorForm = document.getElementById('generator-form');
    if (generatorForm) {
        generatorForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get form data
            const length = parseInt(document.getElementById('length').value);
            const include_uppercase = document.getElementById('include_uppercase').checked;
            const include_lowercase = document.getElementById('include_lowercase').checked;
            const include_numbers = document.getElementById('include_numbers').checked;
            const include_special = document.getElementById('include_special').checked;

            // Validate at least one option is selected
            if (!include_uppercase && !include_lowercase && !include_numbers && !include_special) {
                showError('Please select at least one character type');
                return;
            }

            const data = {
                length: length,
                include_uppercase: include_uppercase,
                include_lowercase: include_lowercase,
                include_numbers: include_numbers,
                include_special: include_special
            };

            showSpinner();
            try {
                const response = await fetch('/generate_password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                if (result.error) {
                    throw new Error(result.error);
                }

                const passwordInput = document.getElementById('password');
                passwordInput.value = result.password;
                passwordInput.dispatchEvent(new Event('input'));
            } catch (error) {
                console.error('Error:', error);
                showError('Error generating password. Please try again.');
            } finally {
                hideSpinner();
            }
        });
    }
});

// Utility functions
function updatePasswordStrength(data) {
    const strengthBar = document.getElementById('password-strength');
    const strengthText = document.getElementById('strength-text');
    const suggestionsList = document.getElementById('suggestions-list');
    
    if (!strengthBar || !strengthText || !suggestionsList) return;

    // Update progress bar
    strengthBar.style.width = `${data.score}%`;
    
    // Update color based on strength
    if (data.score < 40) {
        strengthBar.className = 'progress-bar bg-danger';
    } else if (data.score < 60) {
        strengthBar.className = 'progress-bar bg-warning';
    } else if (data.score < 80) {
        strengthBar.className = 'progress-bar bg-info';
    } else if (data.score < 90) {
        strengthBar.className = 'progress-bar bg-primary';
    } else {
        strengthBar.className = 'progress-bar bg-success';
    }
    
    // Update text
    strengthText.textContent = data.strength;
    
    // Update suggestions
    suggestionsList.innerHTML = '';
    if (data.suggestions && data.suggestions.length > 0) {
        data.suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });
    }
}

function resetPasswordStrength() {
    const strengthBar = document.getElementById('password-strength');
    const strengthText = document.getElementById('strength-text');
    const suggestionsList = document.getElementById('suggestions-list');
    
    if (strengthBar) {
        strengthBar.style.width = '0%';
        strengthBar.className = 'progress-bar';
    }
    if (strengthText) {
        strengthText.textContent = '';
    }
    if (suggestionsList) {
        suggestionsList.innerHTML = '';
    }
}

function showSpinner() {
    const spinner = document.querySelector('.spinner');
    if (spinner) spinner.style.display = 'block';
}

function hideSpinner() {
    const spinner = document.querySelector('.spinner');
    if (spinner) spinner.style.display = 'none';
}

function showError(message) {
    const flashContainer = document.querySelector('.flash-messages');
    if (flashContainer) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'flash-message error fade-in';
        errorDiv.textContent = message;
        flashContainer.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
    }
} 