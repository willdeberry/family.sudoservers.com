#!/usr/bin/env node
// Verify focus-history back nav: button enable/disable, click, keyboard.
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await (await browser.newContext({viewport:{width:1600,height:1200}})).newPage();
page.on('pageerror', e => console.log('  [pageerror]', e.message));

await page.goto('http://localhost:4321/');
await page.waitForSelector('#family-chart svg g.card_cont');
await page.waitForFunction(() => window.__familytree?.focusOn);

const mainName = async () => page.evaluate(() => {
  const main = document.querySelector('#family-chart .card-main-outline');
  return main?.closest('.card_cont')?.textContent?.replace(/\s+/g,' ').trim().slice(0,60) || null;
});
const canBack = async () => page.evaluate(() => window.__familytree?.canGoBack());
const btnDisabled = async () => page.evaluate(() => !!document.getElementById('nav-back')?.disabled);

console.log('Start:', await mainName(), '| canBack:', await canBack(), '| btnDisabled:', await btnDisabled());

// Navigate via search to William Dale DeBerry
await page.click('#search-trigger');
await page.fill('#search-input', 'William Dale DeBerry');
await page.waitForSelector('.hit-row');
await page.locator('.hit-row').first().click();
await page.waitForSelector('#person-modal', { state: 'visible' });
await page.click('#focus-tree-on');
await page.waitForTimeout(800);
console.log('After focus William:', await mainName(), '| canBack:', await canBack(), '| btnDisabled:', await btnDisabled());

// Click back button
await page.click('#nav-back');
await page.waitForTimeout(800);
console.log('After back click:', await mainName(), '| canBack:', await canBack(), '| btnDisabled:', await btnDisabled());

// Navigate forward, then test Backspace key
await page.click('#search-trigger');
await page.fill('#search-input', 'Nancy Guthrie');
await page.waitForSelector('.hit-row');
await page.locator('.hit-row').first().click();
await page.waitForSelector('#person-modal', { state: 'visible' });
await page.click('#focus-tree-on');
await page.waitForTimeout(800);
console.log('After focus Nancy:', await mainName(), '| canBack:', await canBack());

await page.keyboard.press('Backspace');
await page.waitForTimeout(800);
console.log('After Backspace:', await mainName(), '| canBack:', await canBack(), '| btnDisabled:', await btnDisabled());

await browser.close();
