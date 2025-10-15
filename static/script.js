// ---------------- Typing Animation ----------------
const tagline = document.querySelector(".tagline");
const text = "Build. Code. Innovate.";
let index = 0;

function typeEffect() {
  tagline.innerHTML = text.slice(0, index) + '<span class="cursor">|</span>';
  index++;
  if (index > text.length) index = 0;
}
setInterval(typeEffect, 150);

// ---------------- Quiz Functionality ----------------
// quizData is passed from Flask via Jinja
const quizData = window.quizData || [
  {
    question: "Which language is primarily used for web development?",
    options: ["Python", "JavaScript", "C++", "Java"],
    answer: "JavaScript"
  },
  {
    question: "HTML stands for?",
    options: ["Hyper Text Markup Language", "High Text Machine Language", "Hyperlink Text Management", "Home Tool Markup Language"],
    answer: "Hyper Text Markup Language"
  },
  {
    question: "CSS is used for?",
    options: ["Content Structure", "Styling Web Pages", "Database Management", "Server-side scripting"],
    answer: "Styling Web Pages"
  },
  {
    question: "Which of these is a frontend framework?",
    options: ["Django", "React", "Flask", "Laravel"],
    answer: "React"
  }
];

let currentQuestion = 0;
let score = 0;

const questionEl = document.getElementById('question');
const optionsEl = document.getElementById('options');
const nextBtn = document.getElementById('nextBtn');
const resultEl = document.getElementById('result');

function loadQuestion() {
  const currentQuiz = quizData[currentQuestion];
  questionEl.textContent = currentQuiz.question;
  optionsEl.innerHTML = "";
  currentQuiz.options.forEach(option => {
    const button = document.createElement("button");
    button.textContent = option;
    button.onclick = () => checkAnswer(option, button);
    optionsEl.appendChild(button);
  });
  nextBtn.disabled = true; // disable next until an answer is selected
}

function checkAnswer(selected, button) {
  if(selected === quizData[currentQuestion].answer){
    score++;
    button.style.backgroundColor = "#00e0b0"; // green
  } else {
    button.style.backgroundColor = "#ff3864"; // red
  }

  // Disable all buttons after selection
  Array.from(optionsEl.children).forEach(btn => btn.disabled = true);
  nextBtn.disabled = false;
}

nextBtn.addEventListener("click", () => {
  currentQuestion++;
  if(currentQuestion < quizData.length){
    loadQuestion();
  } else {
    showResult();
  }
});

function showResult(){
  document.getElementById('quiz-content').classList.add('hide');
  resultEl.classList.remove('hide');
  resultEl.innerHTML = `<h3>You scored ${score} out of ${quizData.length}!</h3>
                        <button onclick="restartQuiz()">Try Again</button>`;
}

function restartQuiz(){
  currentQuestion = 0;
  score = 0;
  resultEl.classList.add('hide');
  document.getElementById('quiz-content').classList.remove('hide');
  loadQuestion();
}

// Initialize quiz
loadQuestion();
