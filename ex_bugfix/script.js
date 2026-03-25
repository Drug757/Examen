/*
  ╔══════════════════════════════════════════════════════════╗
  ║  ГЕНЕРАТОР КОМАНД — в этом файле спрятано 10 ошибок!   ║
  ║  Найди и исправь все баги, чтобы приложение работало.   ║
  ║                                                          ║
  ║  Что должно работать:                                    ║
  ║  1. Добавление участников (без дублей, не пустое)        ║
  ║  2. Удаление участника по кнопке ✕                       ║
  ║  3. Счётчик участников обновляется                       ║
  ║  4. Таймер: старт, стоп, сброс на 30 сек                ║
  ║  5. Генерация случайных команд заданного размера         ║
  ╚══════════════════════════════════════════════════════════╝
*/

// ── Список участников ────────────────────────────────────────
let players = [];

const nameInput   = document.getElementById("name-input");
const addForm     = document.getElementById("add-form");
const playersList = document.getElementById("players-list");
const countSpan   = document.getElementById("count");

// addEventListener изменил с click на submit
addForm.addEventListener("submit", (e) => {
  e.preventDefault();
  
  // добавлил trim для удаления пробелов
  const name = nameInput.value.trim();  

  if (name === "") return;       

  // сравнение должно быть регистронезависимым
  if (players.some(player => player.toLowerCase() === name.toLowerCase())) {
    alert("Такой участник уже есть!");
    return;
  }

  players.push(name);
  nameInput.value = "";
  renderPlayers();
});

function renderPlayers() {
  playersList.innerHTML = "";

  players.forEach((name, i) => {
    const li = document.createElement("li");
    li.textContent = name;

    const btn = document.createElement("button");
    btn.textContent = "✕";

    btn.addEventListener("click", () => {
      // splice должен удалять 1 элемент
      players.splice(i, 1);
      renderPlayers();
    });

    li.append(btn);
    playersList.append(li);
  });

  // добавил обновление счётчика участников
  countSpan.textContent = players.length;
}

// ── Таймер ───────────────────────────────────────────────────
let seconds = 30;
let timerInterval = null;

const timerDisplay = document.getElementById("timer-display");
const startBtn     = document.getElementById("start-btn");
const stopBtn      = document.getElementById("stop-btn");
const resetBtn     = document.getElementById("reset-btn");

function updateTimerDisplay() {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  
  // добавил toString() перед padStart
  timerDisplay.textContent = `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

startBtn.addEventListener("click", () => {
  if (timerInterval) return;
  timerInterval = setInterval(() => {
    // добавил проверку, чтобы таймер не уходил в отрицательные значения
    if (seconds > 0) {
      seconds--;
      updateTimerDisplay();
    } else {
      clearInterval(timerInterval);
      timerInterval = null;
      alert("Время вышло!");
    }
  }, 1000);
});

stopBtn.addEventListener("click", () => {
  clearInterval(timerInterval);
  timerInterval = null;
});

resetBtn.addEventListener("click", () => {
  clearInterval(timerInterval);
  timerInterval = null;
  seconds = 30;
  updateTimerDisplay();
});

// ── Генерация команд ─────────────────────────────────────────
const teamSizeInput = document.getElementById("team-size");
const generateBtn   = document.getElementById("generate-btn");
const teamsOutput   = document.getElementById("teams-output");

generateBtn.addEventListener("click", () => {
  //преобразовал значения в число
  const size = parseInt(teamSizeInput.value);

  if (players.length === 0) {
    alert("Добавьте хотя бы одного участника!");
    return;
  }

  if (players.length < size) {
    alert(`Нужно больше участников! Текущее количество: ${players.length}, требуется: ${size}`);
    return;
  }

  const shuffled = players.sort(() => Math.random() - 0.5);

  const teams = [];
  for (let i = 0; i < shuffled.length; i += size) {
    teams.push(shuffled.slice(i, i + size));
  }

  teamsOutput.innerHTML = "";
  teams.forEach((team, idx) => {
    const card = document.createElement("div");
    card.className = "team-card";
    card.innerHTML = `
      <h3>Команда ${idx + 1}</h3>
      <p>${team.join(", ")}</p>
    `;
    teamsOutput.append(card);
  });
});

function initialize() {
  countSpan.textContent = players.length;
  updateTimerDisplay();
}

// ── Инициализация ────────────────────────────────────────────
initialize();