#!/usr/bin/env node
// Drive trace mode for William Dale DeBerry and dump the resulting card layout
// + take a screenshot we can compare against expectations.
import { chromium } from 'playwright';

const URL = 'http://localhost:4321/';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1600, height: 1200 } });
const page = await ctx.newPage();

page.on('console', msg => {
  const text = msg.text();
  if (text.startsWith('[chart')) console.log('  console:', text);
});

await page.goto(URL);
// Wait for the chart and full data merge.
await page.waitForSelector('#family-chart svg g.card_cont');
await page.waitForFunction(() => window.__familytree?.focusOn);

// Open search, find William Dale DeBerry (the senior, 1963).
await page.click('#search-trigger');
await page.fill('#search-input', 'William Dale DeBerry');
await page.waitForSelector('.hit-row');

// Click the result; opens modal. Then click "Trace ancestry to founder".
await page.locator('.hit-row').first().click();
await page.waitForSelector('#person-modal', { state: 'visible' });
await page.click('#trace-to-founder');
await page.waitForTimeout(1200);

// Take a screenshot.
await page.screenshot({ path: '/tmp/trace.png', fullPage: false });
console.log('screenshot → /tmp/trace.png');

// Dump every visible card's name + position.
const cards = await page.evaluate(() => {
  const conts = document.querySelectorAll('#family-chart svg g.card_cont');
  const out = [];
  conts.forEach(c => {
    const transform = c.getAttribute('transform') || '';
    const m = transform.match(/translate\(([-\d.]+),\s*([-\d.]+)/);
    const x = m ? parseFloat(m[1]) : 0;
    const y = m ? parseFloat(m[2]) : 0;
    const text = (c.textContent || '').replace(/\s+/g, ' ').trim();
    const td = c.__data__;
    const hidden = c.style.display === 'none';
    out.push({
      name: text.slice(0, 60),
      x, y,
      id: td?.data?.id,
      isMain: !!td?.data?.main,
      isAncestry: !!td?.is_ancestry,
      hasSpouse: !!td?.spouse,
      hidden,
    });
  });
  return out.sort((a, b) => a.y - b.y || a.x - b.x);
});

console.log('\nAll cards (H = hidden / placeholder):');
for (const c of cards) {
  console.log(
    `  y=${String(Math.round(c.y)).padStart(6)} x=${String(Math.round(c.x)).padStart(6)} ` +
    `${c.isMain ? '★' : ' '} ${c.isAncestry ? 'a' : ' '} ${c.hasSpouse ? 's' : ' '} ${c.hidden ? 'H' : ' '} ` +
    `${c.name.slice(0, 50)}`
  );
}

await browser.close();
