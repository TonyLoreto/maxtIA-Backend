document.getElementById("submit-query").addEventListener("click", async () => {
    const query = document.getElementById("query-input").value;
    const responseTextarea = document.getElementById("response-textarea");

    if (query.trim() === "") {
        responseTextarea.value = "Por favor, ingresa una consulta.";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),  
        });

        if (!response.ok) {
            throw new Error("Error en la consulta. Inténtalo de nuevo.");
        }

        const data = await response.json();
        responseTextarea.value = `Respuesta: ${data.answer}`;
    } catch (error) {
        responseTextarea.value = `Error: ${error.message}`;
    }
});

document.getElementById("clear-screen").addEventListener("click", () => {
    document.getElementById("query-input").value = "";  
    document.getElementById("response-textarea").value = "";  
});
