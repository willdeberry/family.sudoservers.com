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

// `server-serialization`: minimize what the client actually needs to render
// the chart. The card only displays full name + lifespan; everything else
// (birthday, deathday raw, lineageCode, verified flag) is used only when the
// user opens the modal, which fetches people-index.json on demand.
const treeData = people.map(p => {
  const spouseIds = (p.marriages || [])
    .map(m => m.spouseId)
    .filter(Boolean);

  // Ship both biological parents. family-chart needs both ids on the child
  // so its hierarchyGetterParents pulls them BOTH up as ancestors (couples
  // render adjacent only when both walked up the ancestry tree). If we ship
  // only one, ancestors render solo because the chart's setupSpouses skips
  // ancestry-side nodes. Pedigree collapse (cousin marriages → same ancestor
  // reached via multiple paths) is handled by setDuplicateBranchToggle(true)
  // on the chart, which collapses converging hierarchy branches.
  const parents = (p.parentIds || []).filter(id => byId.has(id));
  const children = (p.childIds || []).filter(id => byId.has(id));

  const birthYear = isoYear(p.birth);
  const deathYear = isoYear(p.death);
  const lifespan = birthYear || deathYear
    ? `${birthYear || '?'} – ${deathYear || ''}`.trim().replace(/\s+–\s+$/, '')
    : '';

  // Per-spouse marriage metadata. The shape is the DatumJson.rel_data
  // pattern from FCP: keyed by the OTHER party's id, with any per-rel
  // fields we want to ship to the client. SpouseLinkTextPlugin reads
  // `marriage_date` to label the connector between spouses.
  const relData = {};
  for (const m of p.marriages || []) {
    if (!m.spouseId) continue;
    const label = m.dateRaw || (m.date ? m.date.slice(0, 4) : null);
    if (!label) continue;
    relData[m.spouseId] = { marriage_date: label };
  }

  return {
    id: p.id,
    data: {
      gender: inferGender(p),
      'full name': displayName(p.name),
      lifespan,
    },
    rel_data: relData,
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
    nameMiddle: p.name?.middle,
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

// Counts are computed once at build time and shipped with the tree so the
// client doesn't have to re-iterate 4.9k rows just to know totals.
const totalPeople = treeData.length;
const verifiedCount = people.filter(p => p.verification?.status === 'verified').length;

// Initial-slice for fast first paint. We BFS the founder's neighborhood up to
// `INITIAL_DEPTH` hops and emit a self-contained subset: each node's rels are
// rewritten to drop any pointer outside the slice, so family-chart can render
// it without dangling-ref crashes. The full dataset still ships separately
// (tree-full.json) and is fetched lazily when the user navigates outside.
const INITIAL_DEPTH = 4;
const treeById = new Map(treeData.map(d => [d.id, d]));
const visited = new Set(['p_000001']);
let frontier = ['p_000001'];
for (let depth = 0; depth < INITIAL_DEPTH; depth++) {
  const next = [];
  for (const id of frontier) {
    const node = treeById.get(id);
    if (!node) continue;
    for (const nb of [...node.rels.parents, ...node.rels.spouses, ...node.rels.children]) {
      if (visited.has(nb)) continue;
      visited.add(nb);
      next.push(nb);
    }
  }
  frontier = next;
  if (!frontier.length) break;
}
const initialSlice = treeData
  .filter(d => visited.has(d.id))
  .map(d => ({
    id: d.id,
    data: d.data,
    rels: {
      parents: d.rels.parents.filter(x => visited.has(x)),
      spouses: d.rels.spouses.filter(x => visited.has(x)),
      children: d.rels.children.filter(x => visited.has(x)),
    },
  }));

writeFileSync(resolve(outDir, 'tree.json'), JSON.stringify({
  meta: { totalPeople, verifiedCount, sliceSize: initialSlice.length },
  people: initialSlice,
}));
writeFileSync(resolve(outDir, 'tree-full.json'), JSON.stringify({
  meta: { totalPeople, verifiedCount },
  people: treeData,
}));
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
