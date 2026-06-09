#!/usr/bin/env node
import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({viewport:{width:1600,height:1200}})).newPage();
await page.goto('http://localhost:4321/');
await page.waitForSelector('#family-chart svg g.card_cont');
await page.waitForFunction(() => window.__familytree?.focusOn);
await page.waitForTimeout(800);

await page.screenshot({ path: '/tmp/main-default.png' });
const counts = await page.evaluate(() => {
  const conts = document.querySelectorAll('#family-chart svg g.card_cont');
  const byId = new Map();
  const byName = new Map();
  conts.forEach(c => {
    if (c.style.display === 'none') return;
    const td = c.__data__;
    if (td?.data?.to_add) return;
    const id = td?.data?.id;
    const name = (c.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 50);
    if (id) byId.set(id, (byId.get(id) || 0) + 1);
    byName.set(name, (byName.get(name) || []).concat([id]));
  });
  return {
    total: conts.length,
    idDups: Array.from(byId.entries()).filter(([,n]) => n>1).sort((a,b)=>b[1]-a[1]),
    nameOnlyDups: Array.from(byName.entries()).filter(([,ids]) => ids.length>1 && new Set(ids).size === ids.length),
  };
});
console.log('Total visible cards:', counts.total);
console.log('TRUE duplicates (same id rendered N times):');
if (!counts.idDups.length) console.log('  none');
counts.idDups.forEach(([id,c]) => console.log(`  ${c}× id=${id}`));
console.log('Name collisions (different people, same name):');
counts.nameOnlyDups.forEach(([n,ids]) => console.log(`  ${n}  → ${ids.join(', ')}`));
await browser.close();
