document.addEventListener('DOMContentLoaded', () => {
    // Get references to DOM elements
    const registerBtn = document.getElementById('registerBtn');
    const loginBtn = document.getElementById('loginBtn');
    const fetchNewsBtn = document.getElementById('fetchNewsBtn');
    const authMessage = document.getElementById('auth-message');
    const newsSection = document.getElementById('news-section');
    const newsResults = document.getElementById('news-results');

    let accessToken = '';

    // Add event listener for the register button
    registerBtn.addEventListener('click', () => {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Send a POST request to the /register endpoint
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            // Display the response message
            authMessage.textContent = data.message;
        });
    });

    // Add event listener for the login button
    loginBtn.addEventListener('click', () => {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Send a POST request to the /login endpoint
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                // Store the access token and display success message
                accessToken = data.access_token;
                authMessage.textContent = "Login successful";
                newsSection.style.display = 'block';
            } else {
                // Display error message
                authMessage.textContent = data.message;
            }
        });
    });

    // Add event listener for the fetch news button
    fetchNewsBtn.addEventListener('click', () => {
        const category = document.getElementById('category').value;

        // Send a GET request to the /news/<category> endpoint
        fetch(`/news/${category}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        })
        .then(response => response.json())
        .then(data => {
            // Clear previous news results
            newsResults.innerHTML = '';

            if (data.message) {
                // Display error message if present
                newsResults.textContent = data.message;
            } else {
                // Display fetched news articles
                data.forEach(news => {
                    // Create a news item div
                    const newsItem = document.createElement('div');
                    newsItem.classList.add('news-item');

                    // Construct the news item content
                    const newsContent = `
                        <h3>${news.heading || 'No title available'}</h3>
                        ${news.image ? `<img src="${news.image}" alt="News Image" style="  width: 100px; max width: None; margin: 10px 0;">` : ''}
                        <p>${news.summary ? news.summary : 'No summary available'}</p>
                        <p><strong>Sentiment Score:</strong> ${news.sentiment_score !== undefined ? news.sentiment_score : 'No score available'}</p>
                        <a href="${news.link || '#'}" target="_blank">Read more</a>
                    `;

                    // Set the inner HTML of the news item
                    newsItem.innerHTML = newsContent;

                    // Append the news item to the results container
                    newsResults.appendChild(newsItem);
                });
            }
        });
    });
});
