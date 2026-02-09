console.log("API load....")
const API_URL = 'https://instant-dashboard-app.onrender.com/api/v1/generate-dashboard';
let currentHTML = '';

// validate json as user types
document.getElementById('jsonInput').addEventListener('input', function() {
    const validationEl = document.getElementById('jsonValidation');
    try {
        JSON.parse(this.value);
        validationEl.innerHTML = '<span class="json-valid">✓ Valid JSON</span>';
    } catch (e) {
        validationEl.innerHTML = '<span class="json-invalid">✗ Invalid JSON</span>';
    }
});

// initial validation
document.getElementById('jsonInput').dispatchEvent(new Event('input'));

// set example prompt
function setPrompt(text) {
    document.getElementById('userPrompt').value = text;
    document.getElementById('userPrompt').focus();
}

// show status message
function showStatus(message, type) {
    const status = document.getElementById('status');
    status.className = `status ${type} visible`;
    status.innerHTML = type === 'loading'
        ? `<span class="spinner"></span>${message}`
        : message;
}

// hide status message
function hideStatus() {
    const status = document.getElementById('status');
    status.className = 'status';
}

// core function: Generate Dashboard
async function generateDashboard() {
    const jsonInput = document.getElementById('jsonInput').value.trim();
    const userPrompt = document.getElementById('userPrompt').value.trim();
    const generateBtn = document.getElementById('generateBtn');
    const iframe = document.getElementById('previewFrame');
    const placeholder = document.getElementById('placeholder');

    // error handling: validate inputs
    if (!jsonInput) {
        showStatus('❌ Please enter JSON data', 'error');
        return;
    }

    if (!userPrompt) {
        showStatus('❌ Please enter a prompt describing your dashboard', 'error');
        return;
    }

    // error handling: validate JSON format
    let parsedJson;
    try {
        parsedJson = JSON.parse(jsonInput);
    } catch (e) {
        showStatus(`❌ Invalid JSON format: ${e.message}`, 'error');
        return;
    }

    // update UI to loading state
    generateBtn.disabled = true;
    showStatus('🤖 Generating your dashboard...', 'loading');

    try {
        // process: api calling
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                json_data: jsonInput,
                user_prompt: userPrompt
            })
        });

        // error handling: check response
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log('response:', data)

        // error handling: validate response
        if (data.status !== 200) {
            throw new Error(data.detail || 'Failed to generate dashboard');
        }

        // output: Render in Preview
        console.log(data.html)
        currentHTML = data.html;
        iframe.srcdoc = currentHTML;

        // show preview, hide placeholder
        iframe.classList.add('visible');
        placeholder.classList.add('hidden');

        // success message
        showStatus('✅ Dashboard generated successfully!', 'success');

        // auto-hide success message after 3 seconds
        setTimeout(() => hideStatus(), 3000);

        // log data summary
        console.log('Data processed:', data.data_summary);

    } catch (error) {
        console.error('Error:', error);

        // error handling: User-friendly error messages
        let errorMessage = error.message;

        if (errorMessage.includes('Failed to fetch')) {
            errorMessage = '⚠️ Cannot connect to backend. Please ensure the server is running at ' + API_URL;
        } else if (errorMessage.includes('JSON')) {
            errorMessage = '❌ ' + errorMessage;
        } else {
            errorMessage = '❌ Error: ' + errorMessage;
        }

        showStatus(errorMessage, 'error');

    } finally {
        generateBtn.disabled = false;
    }
}

// refresh preview
function refreshPreview() {
    const iframe = document.getElementById('previewFrame');
    if (currentHTML) {
        iframe.srcdoc = currentHTML;
        showStatus('✅ Preview refreshed', 'success');
        setTimeout(() => hideStatus(), 2000);
    }
}

// open in new tab
function openInNewTab() {
    if (currentHTML) {
        const newWindow = window.open();
        newWindow.document.write(currentHTML);
        newWindow.document.close();
    } else {
        showStatus('⚠️ Generate a dashboard first', 'error');
        setTimeout(() => hideStatus(), 2000);
    }
}

// keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // ctrl/cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        generateDashboard();
    }
});

// show helpful message on load
console.log('🎨 The Instant Dashboard loaded successfully');
console.log('📋 Keyboard shortcut: Ctrl/Cmd + Enter to generate');