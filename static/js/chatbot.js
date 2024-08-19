document.getElementById('sendBtn').addEventListener('click', sendMessage);

document.getElementById('chatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chatInput');
    const originalValue = input.value.trim();
    if (originalValue === '') return;

    const chatMessages = document.getElementById('chatMessages');

    // Append User Message
    const userMessage = document.createElement('div');
    userMessage.className = 'bg-blue-500 text-white p-3 rounded-lg self-end';
    userMessage.textContent = originalValue;
    chatMessages.appendChild(userMessage);

    // Scroll to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Show "Searching..." and disable the input
    input.value = 'Searching...';
    input.classList.add('text-gray-400');
    input.disabled = true;

    // Make a POST request to the server
    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: originalValue })
    })
    .then(response => response.json())
    .then(data => {
        // Append Bot Message
        const botMessage = document.createElement('div');
        botMessage.className = 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300 p-3 rounded-lg self-start';
        botMessage.textContent = data.answer;
        chatMessages.appendChild(botMessage);

        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Clear the input and re-enable it
        input.value = '';
        input.classList.remove('text-gray-400');
        input.disabled = false;
        input.focus();
    })
    .catch(error => {
        console.error('Error:', error);
        // Re-enable input on error
        input.value = originalValue;
        input.classList.remove('text-gray-400');
        input.disabled = false;
        input.focus();
    });
}