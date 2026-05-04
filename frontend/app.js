let questions = [];
let answers = [];
let index = 0;
let chartInstance = null;

document.addEventListener("DOMContentLoaded", init);

async function init() {
    const res = await fetch("http://127.0.0.1:8000/questions");
    const data = await res.json();

    questions = data.questions;
    showQuestion();
}

function showQuestion() {
    document.getElementById("questionBox").innerText = questions[index];

    document.getElementById("progressText").innerText =
        `Question ${index + 1} / ${questions.length}`;

    document.getElementById("progressFill").style.width =
        ((index + 1) / questions.length) * 100 + "%";
}

function answer(val) {
    answers.push(val);
    index++;

    if (index < questions.length) {
        showQuestion();
    } else {
        submit();
    }
}

async function submit() {
    document.getElementById("questionCard").style.display = "none";

    const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers })
    });

    const data = await res.json();

    document.getElementById("result").classList.remove("hidden");

    document.getElementById("type").innerText = data.type;

    document.getElementById("title").innerText =
        `You are: ${data.percentages["E/I"].side} • ${data.percentages["S/N"].side} • ${data.percentages["T/F"].side} • ${data.percentages["J/P"].side}`;

    document.getElementById("description").innerText = data.description;

    document.getElementById("confidence").innerText =
        `Confidence: ${data.confidence}%`;

    showPercentages(data.percentages);
    fillList("strengths", data.strengths);
    fillList("careers", data.careers);

    drawChart(data.traits);
}

function showPercentages(p) {
    const el = document.getElementById("percentages");
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

function fillList(id, arr) {
    const el = document.getElementById(id);
    el.innerHTML = "";

    arr.forEach(item => {
        el.innerHTML += `<li>${item}</li>`;
    });
}

function drawChart(traits) {
    const ctx = document.getElementById("chart");

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: "radar",
        data: {
            labels: Object.keys(traits),
            datasets: [{
                label: "Trait Strength",
                data: Object.values(traits),
                borderColor: "#3b82f6",
                backgroundColor: "rgba(59,130,246,.18)",
                borderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1400
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.raw}%`;
                        }
                    }
                }
            },
            scales: {
                r: {
                    min: 50,
                    max: 100,
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });
}