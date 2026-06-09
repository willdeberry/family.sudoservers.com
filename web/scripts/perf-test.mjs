#!/usr/bin/env node
/**
 * Drive the dev server with Playwright and measure how the page actually
 * feels. Captures:
 *   - time-to-search-button-responsive
 *   - search keystroke latency for "William Dale DeBerry"
 *   - time to result render
 *   - click + modal open latency
 *   - the chart timing log we emit from Tree.astro
 */
import { chromium } from 'playwright';

const URL = 'http://localhost:4321/';

async function runOnce(label) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();

  const chartTimings = [];
  page.on('console', msg => {
    const text = msg.text();
    if (text.startsWith('[chart') || text.startsWith('Failed') || msg.type() === 'error') {
      chartTimings.push(`[${msg.type()}] ${text}`);
    }
  });
  page.on('pageerror', err => chartTimings.push(`[pageerror] ${err.message}`));

  const t0 = Date.now();
  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  const tDOM = Date.now() - t0;

  // Time until the search trigger is clickable.
  await page.waitForSelector('#search-trigger', { state: 'visible' });
  const tSearchVisible = Date.now() - t0;

  // Time until the chart has rendered (loading spinner is removed).
  let tChartVisible;
  try {
    await page.waitForSelector('#family-chart svg g.card_cont', { timeout: 5000 });
    tChartVisible = Date.now() - t0;
  } catch {
    tChartVisible = -1;
    for (const t of chartTimings) console.log(`  msg: ${t}`);
  }

  // Open the palette.
  const tBeforeOpen = Date.now();
  await page.click('#search-trigger');
  await page.waitForSelector('#search-input', { state: 'visible' });
  const tPaletteOpen = Date.now() - tBeforeOpen;

  // Type the query and measure search-render latency.
  const tBeforeType = Date.now();
  await page.fill('#search-input', 'William Dale DeBerry');
  // Wait until at least one .hit-row appears.
  await page.waitForSelector('.hit-row', { timeout: 5000 });
  const tFirstResult = Date.now() - tBeforeType;

  // Count results, click the first one.
  const resultCount = await page.locator('.hit-row').count();
  const firstResultName = await page.locator('.hit-row').first().innerText();

  const tBeforeClick = Date.now();
  await page.locator('.hit-row').first().click();
  await page.waitForSelector('#person-modal', { state: 'visible' });
  const tModalOpen = Date.now() - tBeforeClick;

  // Click "Focus tree on this person" and measure how long until the chart
  // recenters on the new person. We detect by checking the main card's text.
  const tBeforeFocus = Date.now();
  await page.click('#focus-tree-on');
  // Modal closes; the chart re-centers. Wait for William's card to be the main.
  await page.waitForFunction(() => {
    const main = document.querySelector('#family-chart .card-main-outline');
    if (!main) return false;
    const txt = main.closest('.card_cont')?.textContent || '';
    return txt.includes('William Dale DeBerry');
  }, { timeout: 10000 });
  const tFocus = Date.now() - tBeforeFocus;

  // Wait for chart timings to land.
  await page.waitForTimeout(800);
  await browser.close();

  console.log(`\n=== ${label} ===`);
  console.log(`  DOM ready:            ${tDOM}ms`);
  console.log(`  Search btn visible:   ${tSearchVisible}ms`);
  console.log(`  Chart rendered:       ${tChartVisible}ms`);
  console.log(`  Palette open:         ${tPaletteOpen}ms`);
  console.log(`  First result render:  ${tFirstResult}ms (typed full query)`);
  console.log(`  Result count:         ${resultCount}`);
  console.log(`  Top result:           ${firstResultName.replace(/\n/g, ' ')}`);
  console.log(`  Modal open:           ${tModalOpen}ms`);
  console.log(`  Focus tree on person: ${tFocus}ms`);
  for (const t of chartTimings) console.log(`  ${t}`);
}

await runOnce('run 1');
await runOnce('run 2');
