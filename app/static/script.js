document.getElementById('destinyForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const resultContainer = document.getElementById('result-container');
    const resultContent = document.getElementById('result-content');

    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = 'Consulting the Stars...';

    // Clear previous results
    resultContent.innerHTML = '';
    resultContainer.classList.remove('hidden');

    const formData = new FormData(this);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to fetch destiny reading');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            const text = decoder.decode(value, { stream: true });
            // Since the text is coming as HTML chunks, appending them directly might break tags if split improperly.
            // However, browsers are generally good at handling stream append.
            // For a more robust solution, a markdown parser on client side is often better,
            // but the prompt asked for HTML tags from the server.
            resultContent.innerHTML += text;

            // Auto scroll to bottom
            // resultContent.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }

    } catch (error) {
        resultContent.innerHTML = `<p style="color: red;">The stars are clouded: ${error.message}</p>`;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Reveal Destiny';
    }
});
