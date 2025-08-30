// Pdf upload and submit functions
const loadingModal = document.getElementById('loadingModal');

function showLoading() {
    loadingModal.style.display = 'block';
}

function hideLoading() {
    loadingModal.style.display = 'none';
}

let result_vs = null;


document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent default form submission

    const pdfFile = document.getElementById('pdf_file').files[0];
    if (!pdfFile) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append('pdf', pdfFile);

    showLoading()
    try {
        const response = await fetch('http://127.0.0.1:2000/upload', {
            method: 'POST',
            body: formData
        });
        
        console.log('Raw response:', response);
        result_vs = await response.json();
        console.log('Parsed JSON:', result_vs);

        if (response.ok) {
            document.getElementById('response').innerHTML = `
                <p style="color: green;">${result_vs.message}</p>
            `;
        } else {
            document.getElementById('response').innerHTML = `
                <p style="color: red;">Error: ${result_vs.error}</p>
            `;
        }
    } catch (error) {
        console.error('Upload failed:', error);
        document.getElementById('response').innerHTML = `
            <p style="color: red;">Something went wrong. Check console.</p>
        `;
    } finally {
        hideLoading()
    }
});


// Chat bot interface dynamic interaction functions
document.getElementById('uploadQuery').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevent default form submission

    const userInput = document.getElementById('messagePrompt').value;
    if (userInput.trim() !== '') {
        // Append user message at the top of the chat window
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user');
        userMessage.textContent = userInput;

        // Insert the user message at the top
        document.getElementById('chatMessages').append(userMessage);
        
        // Clear input field
        document.getElementById('messagePrompt').value = '';

        // Simulate bot reply (you can change this to be dynamic later)
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');
        result_vs['query'] = userInput

        console.log(result_vs)

        try {
            const response = await fetch('http://127.0.0.1:2001/llmcall', {
                method: 'POST',
                body: JSON.stringify(result_vs)
            });
            
            console.log('Raw response:', response);
            result_llm = await response.json();
            console.log('Parsed JSON:', result_vs);

            if (response.ok) {
                document.getElementById('response').innerHTML = `
                    <p style="color: green;">${result_vs.message}</p>
                `;
            } else {
                document.getElementById('response').innerHTML = `
                    <p style="color: red;">Error: ${result_llm.error}</p>
                `;
            }
        } catch (error) {
            console.error('Upload failed:', error);
            document.getElementById('response').innerHTML = `
                <p style="color: red;">Something went wrong. Check console.</p>
            `;
        }

        botMessage.textContent = result_llm['answer'];
        
        
        // Insert the bot message at the top
        chatMessages.append(botMessage);

        // Ensure the chat window scrolls to the top to show the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});