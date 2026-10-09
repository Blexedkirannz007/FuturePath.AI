// Detect if we are on the quiz page before assigning listeners
const predictionForm = document.getElementById('predictionForm');

if (predictionForm) {
    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            submitBtn.innerText = 'Running Decision Model...';
            submitBtn.disabled = true;
        }

        const studentData = {
            math_score: parseInt(document.getElementById('math_score').value, 10),
            coding_score: parseInt(document.getElementById('coding_score').value, 10),
            creativity_score: parseInt(document.getElementById('creativity_score').value, 10),
            communication_score: parseInt(document.getElementById('communication_score').value, 10)
        };

        try {
            // Post payload to the Flask API running locally
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'API server returned an error.');
            }

            const result = await response.json();

            // Store decision tree leaves information locally to share across windows
            localStorage.setItem('predicted_career', result.career);
            localStorage.setItem('predicted_explanation', result.explanation);

            // Re-route browser window seamlessly to the results web page
            window.location.href = 'result.html';

        } catch (error) {
            alert('Cannot process prediction. Ensure your app.py Python backend server is running!');
            console.error(error);
            if (submitBtn) {
                submitBtn.innerText = 'Analyze Profile';
                submitBtn.disabled = false;
            }
        }
    });
}