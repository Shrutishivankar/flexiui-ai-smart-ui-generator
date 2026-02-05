// ============================================
// FlexiUI AI Generator - Main JavaScript
// ============================================

// Configuration
const API_URL = 'http://localhost:5000'; // Backend URL

// State
let currentCode = {
    html: '',
    css: '',
    js: ''
};

let conversationHistory = [];

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const quickBtns = document.querySelectorAll('.quick-btn');
const previewFrame = document.getElementById('previewFrame');
const htmlCode = document.getElementById('htmlCode');
const cssCode = document.getElementById('cssCode');
const jsCode = document.getElementById('jsCode');
const copyBtns = document.querySelectorAll('.btn-copy');
const refreshBtn = document.getElementById('refreshPreview');
const exportBtn = document.getElementById('exportCode');
const themeToggle = document.getElementById('themeToggle');

// Loading Modal
const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

// ============================================
// Event Listeners
// ============================================

// Send button click
sendBtn.addEventListener('click', handleSendMessage);

// Enter key in textarea (Ctrl+Enter to send)
userInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        handleSendMessage();
    }
});

// Quick action buttons
quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const prompt = btn.getAttribute('data-prompt');
        userInput.value = prompt;
        handleSendMessage();
    });
});

// Copy buttons
copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const codeType = btn.getAttribute('data-code');
        copyCode(codeType);
    });
});

// Refresh preview
refreshBtn.addEventListener('click', updatePreview);

// Export code
exportBtn.addEventListener('click', exportCode);

// Theme toggle
themeToggle.addEventListener('click', toggleTheme);

// ============================================
// Main Functions
// ============================================

async function handleSendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        showToast('Please enter a prompt!', 'warning');
        return;
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    loadingModal.show();
    
    try {
        // Call API to generate UI
        const response = await fetch(`${API_URL}/api/generate-ui`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: message,
                component_type: 'general'
            })
        });
        
        const data = await response.json();
        
        // Hide loading
        loadingModal.hide();
        
        if (data.success) {
            // Store generated code
            currentCode = data.code;
            
            // Update code displays
            htmlCode.textContent = currentCode.html || '<!-- No HTML generated -->';
            cssCode.textContent = currentCode.css || '/* No CSS generated */';
            jsCode.textContent = currentCode.js || '// No JavaScript generated';
            
            // Update preview
            updatePreview();
            
            // Add bot response to chat
            addMessage('✅ UI component generated successfully! Check the preview and code tabs.', 'bot');
            
            // Show success toast
            showToast('UI generated successfully!', 'success');
            
        } else {
            throw new Error(data.error || 'Failed to generate UI');
        }
        
    } catch (error) {
        console.error('Error:', error);
        loadingModal.hide();
        addMessage('❌ Sorry, there was an error generating the UI. Please try again.', 'bot');
        showToast('Error: ' + error.message, 'danger');
    }
}

// ============================================
// Helper Functions
// ============================================

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert chat-message ${sender === 'user' ? 'alert-primary' : 'alert-secondary'}`;
    messageDiv.innerHTML = text;
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updatePreview() {
    if (!currentCode.html && !currentCode.css && !currentCode.js) {
        showToast('No code to preview yet!', 'warning');
        return;
    }
    
    // Create complete HTML document
    const fullHTML = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    margin: 0;
                    padding: 20px;
                    font-family: system-ui, -apple-system, sans-serif;
                }
                ${currentCode.css}
            </style>
        </head>
        <body>
            ${currentCode.html}
            <script>
                ${currentCode.js}
            </script>
        </body>
        </html>
    `;
    
    // Update iframe
    const iframe = previewFrame;
    iframe.srcdoc = fullHTML;
    
    showToast('Preview updated!', 'info');
}

function copyCode(type) {
    let code = '';
    
    switch(type) {
        case 'html':
            code = currentCode.html;
            break;
        case 'css':
            code = currentCode.css;
            break;
        case 'js':
            code = currentCode.js;
            break;
    }
    
    if (!code) {
        showToast('No code to copy!', 'warning');
        return;
    }
    
    // Copy to clipboard
    navigator.clipboard.writeText(code).then(() => {
        showToast(`${type.toUpperCase()} copied to clipboard!`, 'success');
    }).catch(err => {
        showToast('Failed to copy!', 'danger');
        console.error('Copy error:', err);
    });
}

function exportCode() {
    if (!currentCode.html && !currentCode.css && !currentCode.js) {
        showToast('No code to export!', 'warning');
        return;
    }
    
    // Create complete HTML file
    const fullHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlexiUI Generated Component</title>
    <style>
        ${currentCode.css}
    </style>
</head>
<body>
    ${currentCode.html}
    
    <script>
        ${currentCode.js}
    </script>
</body>
</html>`;
    
    // Create download
    const blob = new Blob([fullHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flexiui-component.html';
    a.click();
    
    showToast('Code exported successfully!', 'success');
}

function toggleTheme() {
    document.body.classList.toggle('bg-dark');
    document.body.classList.toggle('text-light');
    document.body.classList.toggle('bg-light');
    document.body.classList.toggle('text-dark');
    
    const icon = themeToggle.querySelector('i');
    icon.classList.toggle('bi-moon-fill');
    icon.classList.toggle('bi-sun-fill');
}

function showToast(message, type = 'info') {
    // Create toast element
    const toastHTML = `
        <div class="toast align-items-center text-bg-${type} border-0 toast-custom" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Add to body
    const toastContainer = document.createElement('div');
    toastContainer.innerHTML = toastHTML;
    document.body.appendChild(toastContainer);
    
    // Show toast
    const toastElement = toastContainer.querySelector('.toast');
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    // Remove after hiding
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastContainer.remove();
    });
}

// ============================================
// Initialize
// ============================================

console.log('🚀 FlexiUI AI Generator initialized!');
console.log('📡 Backend URL:', API_URL);

// Welcome message
setTimeout(() => {
    showToast('Welcome to FlexiUI AI Generator! 🎨', 'info');
}, 500);