/**
 * Authentication Module
 * Handles user registration, login, logout, and session management
 */

// Show login page
function showLoginPage() {
    const loginPage = document.getElementById('login-page');
    loginPage.innerHTML = `
        <div class="auth-container">
            <div class="auth-card">
                <h2>Login to Finalytics</h2>
                <form id="login-form" class="auth-form">
                    <div class="form-group">
                        <label for="login-email">Email</label>
                        <input 
                            type="email" 
                            id="login-email" 
                            class="form-control" 
                            placeholder="your@email.com"
                            required
                        />
                    </div>
                    <div class="form-group">
                        <label for="login-password">Password</label>
                        <input 
                            type="password" 
                            id="login-password" 
                            class="form-control" 
                            placeholder="••••••••"
                            required
                        />
                    </div>
                    <div id="login-error" class="error-message hidden"></div>
                    <button type="submit" class="btn btn-primary btn-block">Login</button>
                </form>
                <p class="auth-switch">
                    Don't have an account? 
                    <a href="#register" class="link" onclick="navigate('register'); return false;">Register</a>
                </p>
            </div>
        </div>
    `;

    // Attach form handler
    document.getElementById('login-form').addEventListener('submit', handleLogin);
}

// Show register page
function showRegisterPage() {
    const registerPage = document.getElementById('register-page');
    registerPage.innerHTML = `
        <div class="auth-container">
            <div class="auth-card">
                <h2>Create Account</h2>
                <form id="register-form" class="auth-form">
                    <div class="form-group">
                        <label for="register-email">Email</label>
                        <input 
                            type="email" 
                            id="register-email" 
                            class="form-control" 
                            placeholder="your@email.com"
                            required
                        />
                    </div>
                    <div class="form-group">
                        <label for="register-password">Password</label>
                        <input 
                            type="password" 
                            id="register-password" 
                            class="form-control" 
                            placeholder="Minimum 8 characters"
                            minlength="8"
                            required
                        />
                    </div>
                    <div class="form-group">
                        <label for="register-password-confirm">Confirm Password</label>
                        <input 
                            type="password" 
                            id="register-password-confirm" 
                            class="form-control" 
                            placeholder="Re-enter password"
                            required
                        />
                    </div>
                    <div id="register-error" class="error-message hidden"></div>
                    <button type="submit" class="btn btn-primary btn-block">Create Account</button>
                </form>
                <p class="auth-switch">
                    Already have an account? 
                    <a href="#login" class="link" onclick="navigate('login'); return false;">Login</a>
                </p>
            </div>
        </div>
    `;

    // Attach form handler
    document.getElementById('register-form').addEventListener('submit', handleRegister);
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    
    try {
        const response = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        // Store token (also stored in httpOnly cookie by backend)
        localStorage.setItem('access_token', response.access_token);
        
        // Update app state
        await checkAuth();
        
        // Redirect to dashboard
        navigate('documents');
        
    } catch (error) {
        errorDiv.textContent = error.message || 'Login failed. Please try again.';
        errorDiv.classList.remove('hidden');
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const passwordConfirm = document.getElementById('register-password-confirm').value;
    const errorDiv = document.getElementById('register-error');
    
    // Validate password match
    if (password !== passwordConfirm) {
        errorDiv.textContent = 'Passwords do not match';
        errorDiv.classList.remove('hidden');
        return;
    }
    
    try {
        // Register user
        await apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        // Auto-login after successful registration
        const loginResponse = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        // Store token
        localStorage.setItem('access_token', loginResponse.access_token);
        
        // Update app state
        await checkAuth();
        
        // Redirect to dashboard
        navigate('documents');
        
    } catch (error) {
        errorDiv.textContent = error.message || 'Registration failed. Please try again.';
        errorDiv.classList.remove('hidden');
    }
}

// Export functions to window for use by navigate()
window.showLoginPage = showLoginPage;
window.showRegisterPage = showRegisterPage;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;

