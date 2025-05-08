document.addEventListener("DOMContentLoaded", () => {
    // Configurar marked.js para segurança
    marked.setOptions({
        sanitize: true,  // Sanitizar o HTML de entrada
        breaks: true,    // Converter quebras de linha em <br>
        gfm: true        // Usar GitHub Flavored Markdown
    });

    const chatBox = document.getElementById("chatBox");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");

    const addMessage = (text, sender) => {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "assistant-message");

        const p = document.createElement("p");
        // Use marked.js to parse Markdown to HTML
        if (sender === "assistant") {
            // Processar Markdown apenas para mensagens do assistente
            p.innerHTML = marked.parse(text);
        } else {
            // Para mensagens do usuário, apenas substituir quebras de linha
            p.innerHTML = text.replace(/\n/g, "<br>");
        }
        messageDiv.appendChild(p);

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
    };

    const sendMessage = async () => {
        const question = userInput.value.trim();
        if (question === "") return;

        addMessage(question, "user");
        userInput.value = ""; // Clear input field
        sendButton.disabled = true;
        addMessage("Digitando...", "assistant"); // Show typing indicator

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question: question }),
            });

            // Remove typing indicator
            const typingIndicator = chatBox.querySelector(".assistant-message:last-child");
            if (typingIndicator && typingIndicator.textContent.includes("Digitando...")) {
                chatBox.removeChild(typingIndicator);
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            addMessage(data.answer, "assistant");

        } catch (error) {
            console.error("Erro ao enviar mensagem:", error);
            // Remove typing indicator if it's still there on error
            const typingIndicatorOnError = chatBox.querySelector(".assistant-message:last-child");
            if (typingIndicatorOnError && typingIndicatorOnError.textContent.includes("Digitando...")) {
                chatBox.removeChild(typingIndicatorOnError);
            }
            addMessage(`Desculpe, ocorreu um erro: ${error.message}. Tente novamente.`, "assistant");
        }
        sendButton.disabled = false;
        userInput.focus();
    };

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    userInput.focus(); // Focus on input field on load
});

