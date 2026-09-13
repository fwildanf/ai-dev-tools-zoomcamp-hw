/**
 * All backend access goes through this module.
 * Swap fetchScoreboard() for a real HTTP call when Django exists.
 */

import { MOCK_SCOREBOARD } from "./mock-data.js";

const CACHE_KEY = "pl_scoreboard.v1";
const CACHE_TTL_MS = 5 * 60 * 1000;

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
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

/** Replace this with GET /api/scoreboard/ later. */
async function fetchScoreboard() {
  await delay(450);
  return structuredClone(MOCK_SCOREBOARD);
}

/**
 * Load standings and this week's matches.
 * Uses a short session cache so reloads skip the mock "network" while fresh.
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
