const cityInput = document.getElementById("cityInput");
const autocompleteList = document.getElementById("autocompleteList");
const weatherForm = document.getElementById("weatherForm");
const unitSelect = document.getElementById("unitSelect");
const weatherResult = document.getElementById("weatherResult");
const forecastDiv = document.getElementById("forecast");
const recentList = document.getElementById("recentList");

// Autocomplete
cityInput.addEventListener("input", async () => {
    const query = cityInput.value;
    if (!query) {
        autocompleteList.innerHTML = "";
        return;
    }
    const res = await fetch(`/autocomplete?q=${query}`);
    const suggestions = await res.json();
    autocompleteList.innerHTML = "";
    suggestions.forEach(city => {
        const li = document.createElement("li");
        li.textContent = city;
        li.addEventListener("click", () => {
            cityInput.value = city;
            autocompleteList.innerHTML = "";
        });
        autocompleteList.appendChild(li);
    });
});

// Function to fetch weather
async function fetchWeather(city, units) {
    try {
        const res = await fetch(`/weather_json?city=${city}&units=${units}`);
        const data = await res.json();

        // Handle errors
        if (data.weather.error) {
            weatherResult.innerHTML = `<p class="error">${data.weather.error}</p>`;
            forecastDiv.innerHTML = "";
        } else {
            // Current weather
            weatherResult.innerHTML = `
                <h2>${data.weather.city}</h2>
                <img src="http://openweathermap.org/img/wn/${data.weather.icon}@2x.png" alt="icon">
                <p>Temperature: ${data.weather.temp}°</p>
                <p>Description: ${data.weather.description}</p>
                <p>Humidity: ${data.weather.humidity}%</p>
                <p>Wind: ${data.weather.wind} m/s</p>
            `;

            // Forecast
            if (data.forecast) {
                let forecastHTML = `<h3>7-Day Forecast:</h3><div class="forecast-cards">`;
                data.forecast.forEach(day => {
                    const date = new Date(day.date * 1000); // Convert Unix timestamp
                    const dayName = date.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });

                    forecastHTML += `
                        <div class="card">
                            <p>${dayName}</p>
                            <img src="http://openweathermap.org/img/wn/${day.icon}@2x.png" alt="icon">
                            <p>${day.description}</p>
                            <p>${day.temp_min}° - ${day.temp_max}°</p>
                        </div>
                    `;
                });
                forecastHTML += `</div>`;
                forecastDiv.innerHTML = forecastHTML;
            }

            // Recent searches
            recentList.innerHTML = "";
            data.recent.forEach(c => {
                const li = document.createElement("li");
                li.textContent = c;
                li.style.cursor = "pointer"; // indicate clickable
                li.addEventListener("click", () => {
                    cityInput.value = c;
                    fetchWeather(c, unitSelect.value);
                });
                recentList.appendChild(li);
            });
        }

    } catch (err) {
        weatherResult.innerHTML = `<p class="error">Unable to fetch weather. Try again.</p>`;
        forecastDiv.innerHTML = "";
    }
}

// Weather form submission
weatherForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const city = cityInput.value;
    const units = unitSelect.value;
    fetchWeather(city, units);
});
