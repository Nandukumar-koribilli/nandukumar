let isListening = false;
let recognition = null;
let currentTranscript = '';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeSpeechRecognition();
    setupToastStyles();
});

// Create toast notification styles
function setupToastStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .toast.show {
            opacity: 1;
        }
    `;
    document.head.appendChild(style);
}

// Show toast notification
function showToast(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US'; // Default to English, backend will detect the actual language
        
        recognition.onresult = function(event) {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            currentTranscript = finalTranscript || interimTranscript;
            updateTranscript(currentTranscript);
            
            if (finalTranscript) {
                setTimeout(() => {
                    if (!isListening) {
                        translateText();
                    }
                }, 1000);
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            stopRecording();
            showToast('Speech recognition error: ' + event.error);
        };
        
        recognition.onend = function() {
            stopRecording();
        };
    } else {
        showUnsupportedMessage();
    }
}

function toggleRecording() {
    if (isListening) {
        stopRecording();
    } else {
        startRecording();
    }
}

function startRecording() {
    if (!recognition) {
        showUnsupportedMessage();
        return;
    }
    
    isListening = true;
    currentTranscript = '';
    
    const micButton = document.getElementById('mic-button');
    const listeningIndicator = document.getElementById('listening-indicator');
    
    micButton.classList.add('recording');
    micButton.innerHTML = '<span class="mic-icon">⏹️</span><div class="pulse-ring"></div>';
    listeningIndicator.classList.remove('hidden');
    
    hideElement('translation-result');
    hideElement('action-buttons');
    hideElement('transcript-container');
    
    try {
        recognition.start();
        showToast('Recording started');
    } catch (error) {
        showToast('Failed to start recording');
        stopRecording();
    }
}

function stopRecording() {
    if (!recognition) return;
    
    isListening = false;
    
    const micButton = document.getElementById('mic-button');
    const listeningIndicator = document.getElementById('listening-indicator');
    
    micButton.classList.remove('recording');
    micButton.innerHTML = '<span class="mic-icon">🎤</span><div class="pulse-ring"></div>';
    listeningIndicator.classList.add('hidden');
    
    recognition.stop();
    
    if (currentTranscript.trim()) {
        showElement('action-buttons');
        showToast('Recording stopped');
    }
}

function updateTranscript(transcript) {
    const transcriptContainer = document.getElementById('transcript-container');
    const transcriptElement = document.getElementById('transcript');
    
    transcriptElement.textContent = transcript;
    transcriptContainer.classList.remove('hidden');
}

function translateText() {
    if (!currentTranscript.trim()) {
        showToast('No text to translate');
        return;
    }

    showElement('loading-section');
    hideElement('action-buttons');
    hideElement('translation-result');

    console.log(`Sending translation request: text='${currentTranscript}'`);

    fetch('http://localhost:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: currentTranscript
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        const translatedText = data.translated_text;
        const detectedLang = data.detected_lang;
        const targetLang = data.target_lang;
        showTranslationResult(currentTranscript, translatedText, detectedLang, targetLang);
        hideElement('loading-section');
        showElement('translation-result');
        showToast('Translation completed');
    })
    .catch(error => {
        console.error('Translation error:', error);
        hideElement('loading-section');
        showToast('Translation failed: ' + error.message);
    });
}

function showTranslationResult(original, translated, detectedLang, targetLang) {
    const originalElement = document.getElementById('original-text');
    const translatedElement = document.getElementById('translated-text');
    const timestampElement = document.getElementById('timestamp');
    const detectedLangElement = document.getElementById('detected-lang');
    const originalLangElement = document.getElementById('original-lang');
    const translatedLangElement = document.getElementById('translated-lang');
    
    originalElement.textContent = original;
    translatedElement.textContent = translated;
    timestampElement.textContent = `Translated at ${new Date().toLocaleTimeString()}`;
    
    // Display the detected and target languages
    detectedLangElement.textContent = `Detected Language: ${detectedLang === 'en' ? 'English' : 'Telugu'}`;
    originalLangElement.textContent = `Language: ${detectedLang === 'en' ? 'English' : 'Telugu'}`;
    translatedLangElement.textContent = `Language: ${targetLang === 'en' ? 'English' : 'Telugu'}`;
}

function speakText(type) {
    if ('speechSynthesis' in window) {
        const text = type === 'original' 
            ? document.getElementById('original-text').textContent
            : document.getElementById('translated-text').textContent;
        
        const detectedLang = document.getElementById('detected-lang').textContent.includes('English') ? 'en' : 'te';
        const targetLang = document.getElementById('translated-lang').textContent.includes('English') ? 'en' : 'te';
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = type === 'original' ? detectedLang : targetLang;
        speechSynthesis.speak(utterance);
        showToast('Playing audio');
    } else {
        showToast('Text-to-speech not supported');
    }
}

function copyText(type) {
    const text = type === 'original' 
        ? document.getElementById('original-text').textContent
        : document.getElementById('translated-text').textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showCopyFeedback();
        showToast('Text copied to clipboard');
    }).catch(() => {
        showToast('Failed to copy text');
    });
}

function showCopyFeedback() {
    const buttons = document.querySelectorAll('.icon-button');
    buttons.forEach(button => {
        if (button.textContent.includes('📋')) {
            const originalText = button.textContent;
            button.textContent = '✅';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        }
    });
}

function resetAll() {
    currentTranscript = '';
    hideElement('transcript-container');
    hideElement('action-buttons');
    hideElement('translation-result');
    hideElement('loading-section');
    document.getElementById('transcript').textContent = 'Your spoken words will appear here...';
    document.getElementById('detected-lang').textContent = '';
    if (recognition && isListening) {
        stopRecording();
    }
    showToast('Reset complete');
}

function showUnsupportedMessage() {
    const recorderSection = document.querySelector('.recorder-section .card');
    recorderSection.innerHTML = `
        <div style="text-align: center; padding: 40px;">
            <div style="font-size: 3rem; margin-bottom: 20px;">🚫</div>
            <h3 style="color: #e53e3e; margin-bottom: 15px;">Speech Recognition Not Supported</h3>
            <p style="color: #718096;">Your browser doesn't support speech recognition. Please use Chrome, Edge, or Safari.</p>
        </div>
    `;
    showToast('Browser not supported');
}

function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}