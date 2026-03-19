const form = document.getElementById("contact-form");
const resultBox = document.getElementById("result");
const resultText = document.getElementById("result-text");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = document.getElementById("query").value.trim();
    if (!query) {
      alert("Please enter a query.");
      return;
    }

    resultBox.hidden = false;
    resultText.textContent = "Running demo...";

    try {
      const response = await fetch("/api/demo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Request failed");
      }

      resultText.textContent = data.results
        .map((item) => `- ${item.source}: ${item.data}`)
        .join("\\n\\n");
    } catch (error) {
      resultText.textContent = `Error: ${error.message}`;
    }
  });
}
