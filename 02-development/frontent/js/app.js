import { getScoreboard } from "./api.js";

const tableBody = document.querySelector("#standings-body");
const resultsList = document.querySelector("#results-list");
const fixturesList = document.querySelector("#fixtures-list");
const statusEl = document.querySelector("#load-status");
const seasonEl = document.querySelector("#season-label");
const matchweekEl = document.querySelector("#matchweek-label");
const errorEl = document.querySelector("#error-banner");
const refreshBtn = document.querySelector("#refresh-btn");
const matchDialog = document.querySelector("#match-dialog");
const matchDialogBody = document.querySelector("#match-dialog-body");

function signed(n) {
  if (n > 0) return `+${n}`;
  return String(n);
}

function formatKickoff(iso) {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(iso));
}

function formatMatchDay(iso) {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "long",
    month: "short",
    day: "numeric",
  }).format(new Date(iso));
}

function formatMatchTime(iso) {
  return new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(iso));
}

function formatFetchedAt(ms) {
  return new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(ms));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function setStatus(board) {
  const from = board.source === "cache" ? "cache" : "live fetch";
  statusEl.textContent = `Loaded from ${from} at ${formatFetchedAt(board.fetchedAt)}`;
}

function renderStandings(rows) {
  tableBody.replaceChildren();
  for (const row of rows) {
    const tr = document.createElement("tr");
    if (row.position <= 4) tr.classList.add("zone-cl");
    else if (row.position >= 18) tr.classList.add("zone-rel");
    tr.innerHTML = `
      <td class="num">${row.position}</td>
      <th scope="row">${escapeHtml(row.club)}</th>
      <td class="num">${row.played}</td>
      <td class="num">${row.won}</td>
      <td class="num">${row.drawn}</td>
      <td class="num">${row.lost}</td>
      <td class="num">${row.goalsFor}</td>
      <td class="num">${row.goalsAgainst}</td>
      <td class="num">${signed(row.goalDifference)}</td>
      <td class="num pts">${row.points}</td>
    `;
    tableBody.append(tr);
  }
}

function matchCard(match) {
  const finished = match.status === "FINISHED";
  const button = document.createElement("button");
  button.type = "button";
  button.className = `match-card ${finished ? "is-result" : "is-fixture"}`;
  button.dataset.matchId = match.id;

  const homeScore = finished ? escapeHtml(match.homeScore) : "";
  const awayScore = finished ? escapeHtml(match.awayScore) : "";
  const state = finished
    ? `<span class="match-state">FT</span>`
    : `<time class="match-time" datetime="${escapeHtml(match.utcKickoff)}">${escapeHtml(formatMatchTime(match.utcKickoff))}</time>`;

  button.innerHTML = `
    <span class="match-meta">${state}</span>
    <span class="match-row">
      <span class="club">${escapeHtml(match.home)}</span>
      <span class="score">${homeScore}</span>
    </span>
    <span class="match-row">
      <span class="club">${escapeHtml(match.away)}</span>
      <span class="score">${awayScore}</span>
    </span>
  `;
  button.addEventListener("click", () => openMatch(match));
  return button;
}

function groupByDay(matches) {
  const groups = [];
  const index = new Map();
  for (const match of matches) {
    const label = formatMatchDay(match.utcKickoff);
    if (!index.has(label)) {
      const group = { label, matches: [] };
      index.set(label, group);
      groups.push(group);
    }
    index.get(label).matches.push(match);
  }
  return groups;
}

function renderMatchGroups(container, matches, emptyText) {
  container.replaceChildren();
  if (!matches.length) {
    container.innerHTML = `<p class="empty">${emptyText}</p>`;
    return;
  }
  for (const group of groupByDay(matches)) {
    const block = document.createElement("div");
    block.className = "match-day";
    const heading = document.createElement("h3");
    heading.className = "match-day-label";
    heading.textContent = group.label;
    block.append(heading);
    for (const match of group.matches) block.append(matchCard(match));
    container.append(block);
  }
}

function renderMatches(matches) {
  const finished = matches.filter((m) => m.status === "FINISHED");
  const upcoming = matches.filter((m) => m.status !== "FINISHED");
  renderMatchGroups(resultsList, finished, "No results this week yet.");
  renderMatchGroups(fixturesList, upcoming, "No upcoming fixtures this week.");
}

function openMatch(match) {
  const finished = match.status === "FINISHED";
  matchDialogBody.innerHTML = `
    <p class="eyebrow">${finished ? "Full time" : "Upcoming"}</p>
    <div class="dialog-score">
      <p class="dialog-club">${escapeHtml(match.home)}</p>
      <p class="dialog-nums">${finished ? `${escapeHtml(match.homeScore)}–${escapeHtml(match.awayScore)}` : "vs"}</p>
      <p class="dialog-club">${escapeHtml(match.away)}</p>
    </div>
    <p class="muted">${escapeHtml(formatKickoff(match.utcKickoff))}</p>
  `;
  matchDialog.showModal();
}

async function loadScoreboard({ force = false } = {}) {
  errorEl.hidden = true;
  refreshBtn.disabled = true;
  statusEl.textContent = force ? "Fetching scoreboard…" : "Loading scoreboard…";
  try {
    const board = await getScoreboard({ force });
    seasonEl.textContent = board.season;
    matchweekEl.textContent = `Matchweek ${board.matchweek}`;
    renderStandings(board.standings);
    renderMatches(board.matches);
    setStatus(board);
  } catch (err) {
    errorEl.hidden = false;
    errorEl.textContent = err instanceof Error ? err.message : "Could not load the scoreboard.";
    statusEl.textContent = "Load failed.";
  } finally {
    refreshBtn.disabled = false;
  }
}

refreshBtn.addEventListener("click", () => loadScoreboard({ force: true }));
document.querySelector("#close-dialog").addEventListener("click", () => matchDialog.close());
matchDialog.addEventListener("click", (event) => {
  if (event.target === matchDialog) matchDialog.close();
});

loadScoreboard();
