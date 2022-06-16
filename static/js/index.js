const form = document.getElementById('form-input')
const inputField = document.getElementById('input-field')
const checkButton = document.getElementById('check-button')
const result = document.getElementById('result')

form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const userMessage = inputField.value

    const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: userMessage
        })
    })

    const data = await response.json()
    if (data.prediction_result === 'spam') {
        result.classList.add('spam-result')
        result.innerHTML = data.prediction_result
    }
    else {
        result.classList.remove('spam-result')
        result.innerHTML = data.prediction_result
    }
})