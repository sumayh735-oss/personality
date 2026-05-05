const API_URL = "https://personality-1-57jo.onrender.com";

let questions = [];
let answers = [];
let index = 0;
let chartInstance = null;

document.addEventListener("DOMContentLoaded", init);

/* =========================
   INIT
========================= */
async function init() {
    try {
        const res = await fetch(`${API_URL}/questions`);
        const data = await res.json();

        questions = data.questions || [];
        showQuestion();
    } catch (error) {
        console.error("Failed to load questions:", error);
    }
}

/* =========================
   SHOW QUESTION
========================= */
function showQuestion() {
    document.getElementById("questionBox").innerText = questions[index];

    document.getElementById("progressText").innerText =
        `Question ${index + 1} / ${questions.length}`;

    const percent = ((index + 1) / questions.length) * 100;
    document.getElementById("progressFill").style.width = percent + "%";
}

/* =========================
   ANSWER
========================= */
function answer(val) {
    answers.push(val);
    index++;

    if (index < questions.length) {
        showQuestion();
    } else {
        submit();
    }
}

/* =========================
   SUBMIT TO BACKEND
========================= */
async function submit() {
    document.getElementById("questionCard").style.display = "none";

    try {
        const res = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers })
        });

        const data = await res.json();

        document.getElementById("result").classList.remove("hidden");

        // =========================
        // TYPE
        // =========================
        document.getElementById("type").innerText = data.type;

        // =========================
        // PERSONALITY BREAKDOWN TEXT
        // =========================
        const p = data.percentages;

        document.getElementById("title").innerText =
            `You are: ${p["E/I"].side} • ${p["S/N"].side} • ${p["T/F"].side} • ${p["J/P"].side}`;

        // =========================
        // DESCRIPTION (AI STYLE)
        // =========================
        document.getElementById("description").innerText =
            data.description || "Your personality analysis is ready.";

        // =========================
        // CONFIDENCE
        // =========================
        document.getElementById("confidence").innerText =
            `Confidence: ${data.confidence}%`;

        // =========================
        // PERCENTAGE BARS
        // =========================
        showPercentages(data.percentages);

        // =========================
        // LISTS
        // =========================
        fillList("strengths", data.strengths);
        fillList("careers", data.careers);

        // =========================
        // CHART
        // =========================
        drawChart(data.traits);

    } catch (error) {
        console.error("Prediction failed:", error);
    }
}

/* =========================
   PERCENTAGE UI
========================= */
function showPercentages(p) {
    const el = document.getElementById("percentages");
    if (!el) return;

    el.innerHTML = "";

    for (let key in p) {
        el.innerHTML += `
            <div class="percent-item">
                <div class="percent-label">
                    ${p[key].percent}% ${p[key].side}
                </div>
                <div class="percent-bar">
                    <div class="percent-fill" style="width:${p[key].percent}%"></div>
                </div>
            </div>
        `;
    }
}

/* =========================
   LIST RENDER
========================= */
function fillList(id, arr) {
    const el = document.getElementById(id);
    if (!el) return;

    el.innerHTML = "";

    if (!arr || arr.length === 0) {
        el.innerHTML = "<li>No data available</li>";
        return;
    }

    arr.forEach(item => {
        el.innerHTML += `<li>✔ ${item}</li>`;
    });
}

/* =========================
   RADAR CHART (PROFESSIONAL)
========================= */
function drawChart(traits) {
    const ctx = document.getElementById("chart");

    if (!ctx) return;

    if (chartInstance) {
        chartInstance.destroy();
    }

    const labels = Object.keys(traits);
    const values = Object.values(traits);

    chartInstance = new Chart(ctx, {
        type: "radar",
        data: {
            labels: labels,
            datasets: [{
                label: "Personality Strength",
                data: values,
                borderColor: "#3b82f6",
                borderWidth: 2,
                backgroundColor: "rgba(59,130,246,0.15)",
                pointBackgroundColor: "#3b82f6",
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1600,
                easing: "easeOutQuart"
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: {
                        display: false
                    },
                    grid: {
                        color: "#e5e7eb"
                    },
                    angleLines: {
                        color: "#e5e7eb"
                    },
                    pointLabels: {
                        font: {
                            size: 13,
                            weight: "bold"
                        },
                        color: "#1f2937"
                    }
                }
            }
        }
    });
}
