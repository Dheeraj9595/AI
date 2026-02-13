// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        // Update active tab
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');
    });
});

// Character counters
const textareas = {
    'summarize-input': 'summarize-count',
    'polish-input': 'polish-count',
    'image-input': 'image-count'
};

Object.keys(textareas).forEach(inputId => {
    const textarea = document.getElementById(inputId);
    const counter = document.getElementById(textareas[inputId]);
    
    textarea.addEventListener('input', () => {
        counter.textContent = textarea.value.length;
    });
});

// Show/hide loading overlay
function showLoading() {
    document.getElementById('loading').classList.add('active');
}

function hideLoading() {
    document.getElementById('loading').classList.remove('active');
}

// Show toast notification
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// Clear functions
function clearSummarize() {
    document.getElementById('summarize-input').value = '';
    document.getElementById('summarize-count').textContent = '0';
    document.getElementById('summarize-output').textContent = '';
    document.getElementById('summarize-result').style.display = 'none';
    showToast('Cleared!');
}

function clearPolish() {
    document.getElementById('polish-input').value = '';
    document.getElementById('polish-count').textContent = '0';
    document.getElementById('polish-output').textContent = '';
    document.getElementById('polish-result').style.display = 'none';
    showToast('Cleared!');
}

function clearImage() {
    document.getElementById('image-input').value = '';
    document.getElementById('image-count').textContent = '0';
    document.getElementById('generated-image').src = '';
    document.getElementById('image-result').style.display = 'none';
    showToast('Cleared!');
}

// Copy to clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(err => {
        showToast('Failed to copy text');
        console.error('Copy failed:', err);
    });
}

// Summarize text
async function summarizeText() {
    const input = document.getElementById('summarize-input').value.trim();
    
    if (!input) {
        showToast('Please enter some text to summarize');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: input })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to summarize text');
        }
        
        const data = await response.json();
        
        // Display result
        document.getElementById('summarize-output').textContent = data.result;
        document.getElementById('summarize-result').style.display = 'block';
        
        showToast('Text summarized successfully!');
    } catch (error) {
        showToast('Error: ' + error.message);
        console.error('Summarize error:', error);
    } finally {
        hideLoading();
    }
}

// Polish text
async function polishText() {
    const input = document.getElementById('polish-input').value.trim();
    
    if (!input) {
        showToast('Please enter some text to polish');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/polish-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: input })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to polish text');
        }
        
        const data = await response.json();
        
        // Display result
        document.getElementById('polish-output').textContent = data.result;
        document.getElementById('polish-result').style.display = 'block';
        
        showToast('Text polished successfully!');
    } catch (error) {
        showToast('Error: ' + error.message);
        console.error('Polish error:', error);
    } finally {
        hideLoading();
    }
}

// Generate image
async function generateImage() {
    const input = document.getElementById('image-input').value.trim();
    
    if (!input) {
        showToast('Please describe the image you want to generate');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description: input })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate image');
        }
        
        const data = await response.json();
        
        // Display image
        const img = document.getElementById('generated-image');
        img.src = data.image_url;
        img.alt = input;
        document.getElementById('image-result').style.display = 'block';
        
        showToast('Image generated successfully!');
    } catch (error) {
        showToast('Error: ' + error.message);
        console.error('Image generation error:', error);
    } finally {
        hideLoading();
    }
}

// Download image
function downloadImage() {
    const img = document.getElementById('generated-image');
    const link = document.createElement('a');
    link.href = img.src;
    link.download = 'generated-image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Image downloaded!');
}

// Enter key support for textareas
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        const activeTab = document.querySelector('.tab.active').dataset.tab;
        
        switch(activeTab) {
            case 'summarize':
                summarizeText();
                break;
            case 'polish':
                polishText();
                break;
            case 'image':
                generateImage();
                break;
        }
    }
});
