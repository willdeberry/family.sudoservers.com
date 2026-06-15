/**
 * POST /api/submit
 *
 * Accepts a structured genealogy suggestion (either "add a new person"
 * or "edit an existing one") from a signed-in visitor and opens a
 * GitHub issue on the dataset repo so a human can review before
 * merging.
 *
 * Request body (JSON):
 *   {
 *     idToken: string,             // Google ID token (JWT)
 *     mode: 'add' | 'edit',
 *     personId?: string,           // p_XXXXXX, required when mode='edit'
 *     person: PersonInput,         // structured form payload (see types below)
 *   }
 *
 * Response:
 *   200 { ok: true, issueUrl: string }
 *   4xx { ok: false, error: string }
 *
 * Important: we don't allocate p_XXXXXX lineage codes here — those are
 * derived from confirmed parentage on merge, not at submit time. The
 * issue carries the proposed parent ids (existing) and inline names
 * (new) and the human reviewer does the assignment.
 */
import type { APIRoute } from 'astro';

export const prerender = false;

const TOKENINFO = 'https://oauth2.googleapis.com/tokeninfo?id_token=';
const ISSUER_HOSTS = new Set(['accounts.google.com', 'https://accounts.google.com']);

type TokenInfo = {
  aud: string;
  iss: string;
  email?: string;
  email_verified?: string | boolean;
  name?: string;
  sub: string;
  exp: string;
};

type PickerValue =
  | { kind: 'none' }
  | { kind: 'existing'; id: string; displayName?: string }
  | { kind: 'new'; name: string; birthYear?: string; deathYear?: string };

type LifeEventInput = { dateRaw?: string; place?: string };

type PersonInput = {
  name?: { first?: string; middle?: string; last?: string; maidenName?: string };
  sex?: 'M' | 'F';
  birth?: LifeEventInput;
  death?: LifeEventInput;
  burial?: { place?: string };
  parents?: PickerValue[];
  marriages?: Array<{
    spouse: PickerValue;
    dateRaw?: string;
    place?: string;
    marriageOrder?: number;
    notes?: string;
  }>;
  residences?: string[];
  occupation?: string;
  notes?: string;
  sourceNotes?: string;
};

async function verifyIdToken(idToken: string, expectedAud: string): Promise<TokenInfo> {
  const res = await fetch(TOKENINFO + encodeURIComponent(idToken));
  if (!res.ok) throw new Error('token verification failed');
  const info = (await res.json()) as TokenInfo;
  if (info.aud !== expectedAud) throw new Error('audience mismatch');
  if (!ISSUER_HOSTS.has(info.iss)) throw new Error('issuer mismatch');
  if (Number(info.exp) * 1000 < Date.now()) throw new Error('token expired');
  if (info.email_verified !== true && info.email_verified !== 'true') {
    throw new Error('email not verified');
  }
  return info;
}

function fail(status: number, error: string) {
  return new Response(JSON.stringify({ ok: false, error }), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
function ok(payload: Record<string, unknown>) {
  return new Response(JSON.stringify({ ok: true, ...payload }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

// ── Validation ───────────────────────────────────────────────────────
const PID_RE = /^(p|sp)_\d{6}$/;
function isPersonId(s: unknown): s is string {
  return typeof s === 'string' && PID_RE.test(s);
}
function trim(s: unknown, max = 200): string | undefined {
  if (typeof s !== 'string') return undefined;
  const t = s.trim();
  if (!t) return undefined;
  if (t.length > max) throw new Error(`field too long (max ${max})`);
  return t;
}
function validatePicker(p: any, label: string): PickerValue {
  if (!p || typeof p !== 'object') throw new Error(`${label}: missing`);
  if (p.kind === 'none') return { kind: 'none' };
  if (p.kind === 'existing') {
    if (!isPersonId(p.id)) throw new Error(`${label}: invalid id`);
    return { kind: 'existing', id: p.id, displayName: trim(p.displayName, 200) };
  }
  if (p.kind === 'new') {
    const name = trim(p.name, 200);
    if (!name) throw new Error(`${label}: new person needs a name`);
    return {
      kind: 'new',
      name,
      birthYear: trim(p.birthYear, 4),
      deathYear: trim(p.deathYear, 4),
    };
  }
  throw new Error(`${label}: unknown picker kind`);
}
function validatePerson(raw: any): PersonInput {
  if (!raw || typeof raw !== 'object') throw new Error('person: missing');
  const name = raw.name || {};
  const first = trim(name.first, 100);
  const last = trim(name.last, 100);
  if (!first || !last) throw new Error('first + last name required');

  const sex = raw.sex === 'M' || raw.sex === 'F' ? raw.sex : undefined;

  const ev = (e: any): LifeEventInput | undefined => {
    if (!e || typeof e !== 'object') return undefined;
    const dateRaw = trim(e.dateRaw, 100);
    const place = trim(e.place, 300);
    if (!dateRaw && !place) return undefined;
    return { dateRaw, place };
  };

  const parents = Array.isArray(raw.parents)
    ? raw.parents.slice(0, 2).map((p: any, i: number) => validatePicker(p, `parent[${i}]`))
    : [];

  const marriages = Array.isArray(raw.marriages)
    ? raw.marriages.slice(0, 12).map((m: any, i: number) => ({
        spouse: validatePicker(m?.spouse || { kind: 'none' }, `marriage[${i}].spouse`),
        dateRaw: trim(m?.dateRaw, 100),
        place: trim(m?.place, 300),
        marriageOrder:
          m?.marriageOrder != null && Number.isFinite(Number(m.marriageOrder))
            ? Math.max(1, Math.min(9, Number(m.marriageOrder)))
            : undefined,
        notes: trim(m?.notes, 500),
      }))
    : [];

  const residences = Array.isArray(raw.residences)
    ? raw.residences.map((s: any) => trim(s, 200)).filter(Boolean) as string[]
    : undefined;

  return {
    name: {
      first,
      middle: trim(name.middle, 100),
      last,
      maidenName: trim(name.maidenName, 100),
    },
    sex,
    birth: ev(raw.birth),
    death: ev(raw.death),
    burial: ev(raw.burial) ? { place: ev(raw.burial)!.place } : undefined,
    parents,
    marriages,
    residences,
    occupation: trim(raw.occupation, 200),
    notes: trim(raw.notes, 4000),
    sourceNotes: trim(raw.sourceNotes, 4000),
  };
}

// ── Issue body formatting ────────────────────────────────────────────
function fullName(n?: PersonInput['name']) {
  return [n?.first, n?.middle, n?.last].filter(Boolean).join(' ').trim() || 'Unnamed';
}
function pickerLabel(p?: PickerValue) {
  if (!p || p.kind === 'none') return null;
  if (p.kind === 'existing') return `\`${p.id}\` ${p.displayName ? `— ${p.displayName}` : ''}`.trim();
  const lifespan = p.birthYear || p.deathYear
    ? ` (${p.birthYear || '?'}–${p.deathYear || ''})`
    : '';
  return `**New:** ${p.name}${lifespan}`;
}
function evLine(ev?: LifeEventInput) {
  if (!ev) return '_(none)_';
  return [ev.dateRaw, ev.place].filter(Boolean).join(' · ') || '_(none)_';
}
function bulleted(lines: Array<string | null | undefined>) {
  const kept = lines.filter(Boolean) as string[];
  if (!kept.length) return '_(none)_';
  return kept.map(l => `- ${l}`).join('\n');
}

function renderPersonBlock(p: PersonInput): string {
  const sections: string[] = [];
  sections.push(`**Name:** ${fullName(p.name)}${p.name?.maidenName ? ` (born ${p.name.maidenName})` : ''}`);
  if (p.sex) sections.push(`**Sex:** ${p.sex === 'M' ? 'Male' : 'Female'}`);
  sections.push(`**Birth:** ${evLine(p.birth)}`);
  sections.push(`**Death:** ${evLine(p.death)}`);
  if (p.burial?.place) sections.push(`**Burial:** ${p.burial.place}`);
  if (p.occupation) sections.push(`**Occupation:** ${p.occupation}`);
  if (p.residences?.length) {
    sections.push(`**Residences:**\n${bulleted(p.residences)}`);
  }
  if (p.parents?.length) {
    sections.push(`**Parents:**\n${bulleted(p.parents.map(pickerLabel))}`);
  }
  if (p.marriages?.length) {
    const lines = p.marriages.map((m, i) => {
      const head = `Marriage ${m.marriageOrder ?? i + 1}: ${pickerLabel(m.spouse) || '_(spouse not specified)_'}`;
      const sub = [
        m.dateRaw ? `date: ${m.dateRaw}` : null,
        m.place ? `place: ${m.place}` : null,
        m.notes ? `notes: ${m.notes}` : null,
      ].filter(Boolean).join(' · ');
      return sub ? `${head}\n  - ${sub}` : head;
    });
    sections.push(`**Marriages:**\n${lines.map(l => `- ${l}`).join('\n')}`);
  }
  if (p.notes) sections.push(`**Notes:**\n\n${p.notes}`);
  return sections.join('\n\n');
}

// ── Diff helpers (edit mode) ─────────────────────────────────────────
function diffField(label: string, before: string | undefined, after: string | undefined): string | null {
  const b = before?.trim() || '';
  const a = after?.trim() || '';
  if (b === a) return null;
  return `- **${label}:** ${b || '_(empty)_'} → ${a || '_(empty)_'}`;
}
function evFlat(ev?: { date?: string | null; dateRaw?: string | null; place?: string | null } | null) {
  if (!ev) return { date: '', place: '' };
  return {
    date: ev.dateRaw || ev.date || '',
    place: ev.place || '',
  };
}
function renderEditDiff(originalRaw: any, proposed: PersonInput): string {
  // The PersonModal pre-fill data is the people-index.json record. Its
  // shape is: { name: 'Full Name', nameFirst, nameLast, nameMaiden,
  // sex, birth: {date,dateRaw,place}, death: {...}, parentIds: [...],
  // marriages: [...], residences, occupation, notes }
  const before = originalRaw || {};
  const lines: Array<string | null> = [];

  lines.push(diffField('First name', before.nameFirst, proposed.name?.first));
  lines.push(diffField('Middle name', before.nameMiddle, proposed.name?.middle));
  lines.push(diffField('Last name', before.nameLast, proposed.name?.last));
  lines.push(diffField('Maiden name', before.nameMaiden, proposed.name?.maidenName));
  lines.push(diffField('Sex', before.sex, proposed.sex));

  const beforeBirth = evFlat(before.birth);
  lines.push(diffField('Birth date', beforeBirth.date, proposed.birth?.dateRaw));
  lines.push(diffField('Birth place', beforeBirth.place, proposed.birth?.place));

  const beforeDeath = evFlat(before.death);
  lines.push(diffField('Death date', beforeDeath.date, proposed.death?.dateRaw));
  lines.push(diffField('Death place', beforeDeath.place, proposed.death?.place));

  lines.push(diffField('Burial place', before.burial?.place, proposed.burial?.place));
  lines.push(diffField('Occupation', before.occupation, proposed.occupation));
  lines.push(diffField('Notes', before.notes, proposed.notes));

  const beforeParents = (before.parentIds || []).join(', ');
  const afterParents = (proposed.parents || [])
    .map(p => p.kind === 'existing' ? p.id : p.kind === 'new' ? `(new) ${p.name}` : '')
    .filter(Boolean)
    .join(', ');
  lines.push(diffField('Parents', beforeParents, afterParents));

  const beforeRes = (before.residences || []).join(' | ');
  const afterRes = (proposed.residences || []).join(' | ');
  lines.push(diffField('Residences', beforeRes, afterRes));

  // Marriages: list any change as a single field rather than per-row
  // diff — easier for the reviewer to read in one go.
  const beforeMar = (before.marriages || []).map((m: any) => {
    const sp = m.spouseId || m.spouseName || '?';
    return `${sp} ${m.dateRaw || m.date || ''}`.trim();
  }).join(' | ');
  const afterMar = (proposed.marriages || []).map(m => {
    const sp = m.spouse.kind === 'existing' ? m.spouse.id
            : m.spouse.kind === 'new' ? `(new) ${m.spouse.name}`
            : '?';
    return `${sp} ${m.dateRaw || ''}`.trim();
  }).join(' | ');
  lines.push(diffField('Marriages', beforeMar, afterMar));

  const kept = lines.filter(Boolean) as string[];
  if (!kept.length) return '_No field-level changes detected._';
  return kept.join('\n');
}

// ── Handler ──────────────────────────────────────────────────────────
export const POST: APIRoute = async ({ request }) => {
  const audience = import.meta.env.GOOGLE_CLIENT_ID;
  const ghToken = import.meta.env.GITHUB_TOKEN;
  const ghRepo = import.meta.env.GITHUB_REPO;
  if (!audience) return fail(500, 'server misconfigured: GOOGLE_CLIENT_ID');
  if (!ghRepo) return fail(500, 'server misconfigured: GITHUB_REPO');

  let raw: any;
  try {
    raw = await request.json();
  } catch {
    return fail(400, 'invalid JSON body');
  }

  // Auth
  const idToken = raw?.idToken;
  if (typeof idToken !== 'string' || idToken.length < 20) return fail(400, 'idToken required');

  // Mode
  const mode = raw?.mode === 'edit' ? 'edit' : raw?.mode === 'add' ? 'add' : null;
  if (!mode) return fail(400, 'mode must be "add" or "edit"');
  if (mode === 'edit' && !isPersonId(raw.personId)) {
    return fail(400, 'edit mode requires a valid personId');
  }

  // Person payload
  let person: PersonInput;
  try {
    person = validatePerson(raw.person);
  } catch (e: any) {
    return fail(400, e.message);
  }

  let info: TokenInfo;
  try {
    info = await verifyIdToken(idToken, audience);
  } catch (e: any) {
    return fail(401, `sign-in invalid: ${e.message}`);
  }

  // Issue construction
  const submitter = `${info.name || info.email || info.sub} (${info.email || 'no email'})`;
  const personDisplay = fullName(person.name);
  const title = mode === 'edit'
    ? `[Edit] ${raw.editLabel || raw.personId}: ${personDisplay}`
    : `[Add] ${personDisplay}`;

  const sections: string[] = [
    `**Submitted by:** ${submitter}`,
    mode === 'edit' ? `**Editing:** \`${raw.personId}\`` : null,
  ].filter(Boolean) as string[];

  if (mode === 'edit') {
    sections.push(`### Proposed changes\n\n${renderEditDiff(raw.editOriginal, person)}`);
    sections.push(`### Full proposed record\n\n${renderPersonBlock(person)}`);
  } else {
    sections.push(`### Proposed person\n\n${renderPersonBlock(person)}`);
  }

  if (person.sourceNotes) {
    sections.push(`### Source notes\n\n${person.sourceNotes}`);
  }
  sections.push('---\n_Submitted via family.sudoservers.com_');

  const issueBody = sections.join('\n\n');

  if (!ghToken) {
    console.log('[submit] DRY RUN (no GITHUB_TOKEN). Would have opened issue:', title);
    return ok({ issueUrl: `https://github.com/${ghRepo}/issues/dry-run`, dryRun: true });
  }

  const ghRes = await fetch(`https://api.github.com/repos/${ghRepo}/issues`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${ghToken}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title,
      body: issueBody,
      labels: [mode === 'edit' ? 'suggestion:edit' : 'suggestion:add'],
    }),
  });
  if (!ghRes.ok) {
    const err = await ghRes.text();
    console.error('[submit] GitHub API failed:', ghRes.status, err);
    return fail(502, 'failed to open issue');
  }
  const issue = (await ghRes.json()) as { html_url: string };
  return ok({ issueUrl: issue.html_url });
};
