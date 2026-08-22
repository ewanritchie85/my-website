// Turbo Death Warrior - Frontend Controller
// Follows the same pattern as spotify-now-playing.js

const TDW_API_BASE = "/tdw-api";

let tdwGameId = null;
let tdwTyping = false;
let tdwSkip = false;
let tdwControlsReady = false;
let tdwCurrentLines = [];
let tdwCurrentLineIndex = 0;
let tdwCurrentLineEl = null;
let tdwPendingChoice = null;

function tdwBar(cur, max, width = 20) {
    const n = Math.max(0, Math.min(width, Math.round((cur / max) * width)));
    return "█".repeat(n) + "░".repeat(width - n);
}

function tdwHpClass(pct) {
    if (pct > 50) return "hpbar ok";
    if (pct > 25) return "hpbar warn";
    return "hpbar crit";
}

function tdwPad(s, len) {
    return (s || "").toUpperCase().padEnd(len, " ");
}

async function tdwApi(path, body) {
    const res = await fetch(TDW_API_BASE + path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body || {}),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || res.statusText);
    return data;
}

function tdwSetState(st) {
    const p = st.player;
    const hpPct = Math.max(0, (p.hp / p.max_hp) * 100);
    const hpCls = tdwHpClass(hpPct);
    const name = tdwPad(p.name || "-", 10);
    const weapon = tdwPad(p.weapon, 14);
    const potions = String(p.potions).padStart(2, " ");
    const crystal = p.has_turbo_crystal ? "YES" : "NO";

    const statusEl = document.getElementById("tdw-statusline");
    if (statusEl) {
        statusEl.innerHTML =
            `${name} ` +
            `<span class="tdw-dim">HP</span> ` +
            `<span class="${hpCls}">[${tdwBar(p.hp, p.max_hp)}]</span> ` +
            `<span class="tdw-dim">${p.hp}/${p.max_hp}</span> ` +
            `<span class="tdw-dim">WEAPON:</span>${weapon} ` +
            `<span class="tdw-dim">POT:</span><span class="tdw-amber">${potions}</span> ` +
            `<span class="tdw-dim">CRYSTAL:</span><span class="${p.has_turbo_crystal ? "tdw-amber" : "tdw-dim"}">${crystal}</span>`;
    }

    const enemyEl = document.getElementById("tdw-enemy");
    const enemylineEl = document.getElementById("tdw-enemyline");
    if (st.enemy) {
        enemyEl.classList.add("visible");
        const e = st.enemy;
        const ename = tdwPad(e.name, 14);
        enemylineEl.innerHTML =
            `${ename} ` +
            `<span class="tdw-dim">HP</span> ` +
            `<span class="hpbar">[${tdwBar(e.hp, e.max_hp)}]</span> ` +
            `<span class="tdw-dim">${e.hp}/${e.max_hp}</span>`;
    } else {
        enemyEl.classList.remove("visible");
    }
}

function tdwStartTyping(lines) {
    tdwCurrentLines = lines;
    tdwCurrentLineIndex = 0;
    const contentEl = document.getElementById("tdw-content");
    if (contentEl) contentEl.innerHTML = "";
    tdwTyping = true;
    tdwControlsReady = false;
    tdwTypeNextLine();
}

function tdwTypeNextLine() {
    const contentEl = document.getElementById("tdw-content");
    if (!contentEl) return;

    if (tdwCurrentLineIndex >= tdwCurrentLines.length) {
        tdwTyping = false;
        tdwSkip = false;
        tdwControlsReady = true;
        tdwRenderControls();
        return;
    }
    const text = tdwCurrentLines[tdwCurrentLineIndex];
    if (text === "") {
        const sp = document.createElement("div");
        sp.className = "tdw-spacer";
        contentEl.appendChild(sp);
        tdwCurrentLineIndex++;
        tdwTypeNextLine();
        return;
    }
    tdwCurrentLineEl = document.createElement("div");
    tdwCurrentLineEl.className = "tdw-line";
    contentEl.appendChild(tdwCurrentLineEl);
    let i = 0;
    const iv = setInterval(() => {
        i = tdwSkip ? text.length : i + 1;
        tdwCurrentLineEl.textContent = text.slice(0, i);
        if (i >= text.length) {
            clearInterval(iv);
            tdwCurrentLineIndex++;
            setTimeout(tdwTypeNextLine, tdwSkip ? 0 : 80);
        }
    }, 28);
}

function tdwRenderControls() {
    const choicesEl = document.getElementById("tdw-choices");
    const nameForm = document.getElementById("tdw-nameform");
    const nameInput = document.getElementById("tdw-nameinput");
    if (!choicesEl || !nameForm || !nameInput) return;

    choicesEl.innerHTML = "";
    const p = tdwLastPayload;
    if (!p) return;
    if (p.text_input) {
        nameForm.classList.add("visible");
        nameInput.placeholder = p.text_input;
        nameInput.value = "";
        nameInput.focus();
    } else {
        nameForm.classList.remove("visible");
        p.options.forEach((opt, idx) => {
            const div = document.createElement("div");
            div.className = "tdw-choice";
            div.dataset.actionId = opt.id;
            div.innerHTML = `<span class="tdw-num">${idx + 1}</span> ${opt.label}`;
            choicesEl.appendChild(div);
        });
    }
}

let tdwLastPayload = null;

function tdwHandle(payload) {
    if (!tdwGameId && payload.game_id) tdwGameId = payload.game_id;
    tdwLastPayload = payload;
    const choicesEl = document.getElementById("tdw-choices");
    const nameForm = document.getElementById("tdw-nameform");
    if (choicesEl) choicesEl.innerHTML = "";
    if (nameForm) nameForm.classList.remove("visible");
    tdwControlsReady = false;
    tdwSkip = false;
    tdwSetState(payload.state);
    tdwStartTyping(payload.messages);
}

function tdwFatal(err) {
    const contentEl = document.getElementById("tdw-content");
    if (!contentEl) return;
    contentEl.innerHTML = "";
    const el = document.createElement("div");
    el.className = "tdw-line tdw-err";
    el.textContent = "SYSTEM ERROR: " + err.message;
    contentEl.appendChild(el);
}

function tdwShowPendingChoice(choice) {
    const contentEl = document.getElementById("tdw-content");
    if (!contentEl) return;
    const num = choice.querySelector(".tdw-num").textContent;
    const label = choice.textContent.replace(/^\[\d+\]\s*/, "").trim();
    const line = document.createElement("div");
    line.className = "tdw-line";
    line.style.color = "var(--tdw-amber)";
    line.textContent = `> ${num} ${label}`;
    contentEl.appendChild(line);
}

async function tdwChoose(id) {
    try {
        tdwHandle(await tdwApi("/game/" + tdwGameId + "/action", { id }));
    } catch (err) {
        tdwFatal(err);
    }
}

async function tdwInit() {
    const container = document.getElementById("tdw-game");
    if (!container) return;

    // Inject the game HTML
    container.innerHTML = `
        <div id="tdw-crt">
            <div class="tdw-scanlines"></div>
            <div class="tdw-vignette"></div>
            <div class="tdw-sweep"></div>
            <div id="tdw-app">
                <header class="tdw-header">
                    <div class="tdw-titlebox">TURBO DEATH WARRIOR</div>
                    <div class="tdw-subtitle">A QUEST FOR THE REALM'S WI-FI ROUTER · TDW-DOS v1.0</div>
                </header>
                <section id="tdw-status" class="tdw-panel">
                    <pre id="tdw-statusline"></pre>
                </section>
                <section id="tdw-enemy" class="tdw-panel">
                    <pre id="tdw-enemyline"></pre>
                </section>
                <main id="tdw-content" class="tdw-panel"></main>
                <footer id="tdw-controls">
                    <div id="tdw-choices"></div>
                    <form id="tdw-nameform">
                        <span class="tdw-prompt">> </span>
                        <input id="tdw-nameinput" autocomplete="off" maxlength="30" placeholder="ENTER YOUR NAME, WARRIOR" />
                        <button type="submit" hidden>OK</button>
                    </form>
                    <div class="tdw-hint">PRESS 1-9 TO SELECT · CLICK TEXT TO SKIP TYPE-OUT</div>
                </footer>
            </div>
        </div>
    `;

    // Event listeners
    document.addEventListener("click", () => { tdwSkip = true; });

    document.addEventListener("keydown", (e) => {
        const nameInput = document.getElementById("tdw-nameinput");
        const nameForm = document.getElementById("tdw-nameform");
        if (e.target === nameInput) return;
        if (nameForm && nameForm.classList.contains("visible")) {
            nameInput.focus();
            return;
        }
        if (!tdwControlsReady) return;

        if (e.key === "Enter") {
            if (tdwPendingChoice !== null) {
                const choiceId = tdwPendingChoice.dataset.actionId;
                tdwPendingChoice = null;
                tdwChoose(choiceId);
            }
            return;
        }

        const n = parseInt(e.key, 10);
        if (n >= 1 && n <= 9) {
            const choicesEl = document.getElementById("tdw-choices");
            if (!choicesEl) return;
            const choices = choicesEl.querySelectorAll(".tdw-choice");
            const choice = choices[n - 1];
            if (choice) {
                choices.forEach(c => c.classList.remove("active"));
                choice.classList.add("active");
                tdwPendingChoice = choice;
                tdwShowPendingChoice(choice);
            }
        }
    });

    const nameForm = document.getElementById("tdw-nameform");
    if (nameForm) {
        nameForm.addEventListener("submit", async (ev) => {
            ev.preventDefault();
            const nameInput = document.getElementById("tdw-nameinput");
            if (!nameInput) return;
            const name = nameInput.value.trim();
            if (!name || !tdwGameId) return;
            nameInput.value = "";
            nameForm.classList.remove("visible");
            try {
                tdwHandle(await tdwApi("/game/" + tdwGameId + "/name", { name }));
            } catch (err) {
                tdwFatal(err);
            }
        });
    }

    // Start the game
    try {
        tdwHandle(await tdwApi("/game", {}));
    } catch (err) {
        tdwFatal(err);
    }
}

// Auto-init when the project section becomes visible
function initTurboDeathWarrior() {
    const tdwProject = document.getElementById("turbo-death-warrior");
    if (tdwProject && tdwProject.classList.contains("active")) {
        tdwInit();
    }
}

// Export for functions.js to call when project is activated
window.initTurboDeathWarrior = initTurboDeathWarrior;