/**
 * All backend access goes through this module.
 * Talks to the FastAPI app defined in openapi.yaml.
 */

const CACHE_KEY = "pl_scoreboard.v1";
const CACHE_TTL_MS = 5 * 60 * 1000;
const DEFAULT_API = "http://127.0.0.1:8000";

function apiBase() {
  const meta = document.querySelector('meta[name="api-base"]');
  if (meta?.content) return meta.content.replace(/\/$/, "");
  if (location.protocol === "http:" && (location.port === "8000" || location.port === "")) {
    return "";
  }
  return DEFAULT_API;
}

function apiUrl(path) {
  return `${apiBase()}${path}`;
}

async function readJson(path) {
  const response = await fetch(apiUrl(path));
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (body?.detail) detail = body.detail;
    } catch {
      /* ignore non-JSON errors */
    }
    throw new Error(detail);
  }
  return response.json();
}

function readCache() {
  try {
    const raw = sessionStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const entry = JSON.parse(raw);
    if (!entry?.fetchedAt || !entry?.payload) return null;
    if (Date.now() - entry.fetchedAt > CACHE_TTL_MS) return null;
    return entry;
  } catch {
    return null;
  }
}

function writeCache(payload) {
  const entry = { fetchedAt: Date.now(), payload };
  sessionStorage.setItem(CACHE_KEY, JSON.stringify(entry));
  return entry;
}

async function fetchScoreboard() {
  return readJson("/api/scoreboard");
}

export async function getMatch(matchId) {
  return readJson(`/api/matches/${encodeURIComponent(matchId)}`);
}

/**
 * Load standings and this week's matches.
 * Uses a short session cache so reloads skip the API while fresh.
 */
export async function getScoreboard({ force = false } = {}) {
  if (!force) {
    const cached = readCache();
    if (cached) {
      return {
        ...cached.payload,
        source: "cache",
        fetchedAt: cached.fetchedAt,
      };
    }
  }

  const payload = await fetchScoreboard();
  const entry = writeCache(payload);
  return {
    ...payload,
    source: "network",
    fetchedAt: entry.fetchedAt,
  };
}
