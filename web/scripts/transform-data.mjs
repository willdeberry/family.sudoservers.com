#!/usr/bin/env node
/**
 * Transform ../data/people.json into the shape family-chart expects.
 *
 * family-chart Datum shape:
 *   { id, data: { gender, ... }, rels: { parents, spouses, children } }
 *
 * Our schema:
 *   { id, name, sex, birth, death, parentIds, childIds, marriages: [{spouseId}], ... }
 *
 * Output:
 *   web/public/data/tree.json       — array shaped for family-chart
 *   web/public/data/people-index.json — id → richer detail used by the modal
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repo = resolve(__dirname, '..', '..');
const peoplePath = resolve(repo, 'data', 'people.json');
const outDir = resolve(__dirname, '..', 'public', 'data');

mkdirSync(outDir, { recursive: true });

const dataset = JSON.parse(readFileSync(peoplePath, 'utf-8'));
const people = dataset.people;
const byId = new Map(people.map(p => [p.id, p]));

/**
 * Sex inference for people whose sex field is missing.
 * Strategy:
 *   1. Use explicit sex if present
 *   2. Else if they appear as a spouse to someone with known sex, take opposite
 *   3. Else default to 'M' (family-chart requires one of M/F)
 */
function inferGender(person) {
  if (person.sex === 'M') return 'M';
  if (person.sex === 'F') return 'F';

  // Walk all marriages globally to see if anyone marked them as a spouse
  for (const other of people) {
    for (const m of other.marriages || []) {
      if (m.spouseId === person.id && other.sex) {
        return other.sex === 'M' ? 'F' : 'M';
      }
    }
  }
  return 'M';
}

function displayName(name) {
  if (!name) return 'Unknown';
  return name.full || [name.first, name.middle, name.last].filter(Boolean).join(' ') || 'Unknown';
}

function isoYear(event) {
  if (!event) return null;
  if (event.date) return event.date.slice(0, 4);
  if (event.dateRaw) {
    const m = event.dateRaw.match(/\b(1[6-9]\d{2}|20\d{2})\b/);
    return m ? m[1] : null;
  }
  return null;
}

const treeData = people.map(p => {
  // Spouses: collect spouseIds from marriages (skip unlinked)
  const spouseIds = (p.marriages || [])
    .map(m => m.spouseId)
    .filter(Boolean);

  // Parents/children: use stored relationship arrays
  const parents = (p.parentIds || []).filter(id => byId.has(id));
  const children = (p.childIds || []).filter(id => byId.has(id));

  const birthYear = isoYear(p.birth);
  const deathYear = isoYear(p.death);

  return {
    id: p.id,
    data: {
      gender: inferGender(p),
      'first name': p.name?.first || '',
      'last name': p.name?.last || '',
      'full name': displayName(p.name),
      birthday: p.birth?.date || p.birth?.dateRaw || '',
      deathday: p.death?.date || p.death?.dateRaw || '',
      birthYear: birthYear || '',
      deathYear: deathYear || '',
      lifespan: birthYear || deathYear
        ? `${birthYear || '?'} – ${deathYear || ''}`.trim().replace(/\s+–\s+$/, '')
        : '',
      lineageCode: (p.lineageCodes || [])[0] || '',
      verified: p.verification?.status === 'verified',
      avatar: '', // could be added later
    },
    rels: {
      parents,
      spouses: spouseIds,
      children,
    },
  };
});

// Also build a richer index keyed by id for the detail modal
const peopleIndex = {};
for (const p of people) {
  peopleIndex[p.id] = {
    id: p.id,
    lineageCodes: p.lineageCodes || [],
    name: displayName(p.name),
    nameFirst: p.name?.first,
    nameLast: p.name?.last,
    nameMaiden: p.name?.maidenName,
    sex: p.sex,
    birth: p.birth,
    death: p.death,
    burial: p.burial,
    parentIds: p.parentIds || [],
    childIds: p.childIds || [],
    marriages: (p.marriages || []).map(m => ({
      spouseId: m.spouseId,
      spouseName: m.spouseName,
      date: m.date,
      dateRaw: m.dateRaw,
      place: m.place,
      order: m.marriageOrder,
      notes: m.notes,
    })),
    residences: p.residences || [],
    occupation: p.occupation,
    notes: p.notes,
    sources: p.sources || [],
    verification: p.verification || { status: 'draft', source: 'unknown' },
  };
}

writeFileSync(resolve(outDir, 'tree.json'), JSON.stringify(treeData));
writeFileSync(resolve(outDir, 'people-index.json'), JSON.stringify(peopleIndex));

// Build a tiny search index (id, name, lineage codes, lifespan)
const searchIndex = people.map(p => ({
  id: p.id,
  n: displayName(p.name),
  c: (p.lineageCodes || []).join(','),
  l: isoYear(p.birth) || '',
}));
writeFileSync(resolve(outDir, 'search.json'), JSON.stringify(searchIndex));

console.log(`Wrote tree.json (${treeData.length} nodes), people-index.json, search.json`);
console.log(`Verified: ${people.filter(p => p.verification?.status === 'verified').length}`);
console.log(`Drafts:   ${people.filter(p => p.verification?.status !== 'verified').length}`);
