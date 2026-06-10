/**
 * POST /api/submit
 *
 * Accepts a genealogy suggestion from a signed-in visitor and opens a
 * GitHub issue on the dataset repo so we can review it before merging.
 *
 * Request body (JSON):
 *   {
 *     idToken:   string,          // Google ID token (JWT) from GIS
 *     personId?: string,          // p_XXXXXX the suggestion relates to (optional)
 *     subject:   string,          // short title
 *     body:      string,          // free-form description
 *     sourceUrl?: string,         // optional citation
 *   }
 *
 * Response:
 *   200 { ok: true, issueUrl: string }
 *   4xx { ok: false, error: string }
 *
 * Token verification: we call Google's tokeninfo endpoint instead of
 * pulling in a JWT library. One network call per submission is fine at
 * this volume and saves an entire dependency tree.
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

export const POST: APIRoute = async ({ request }) => {
  const audience = import.meta.env.GOOGLE_CLIENT_ID;
  const ghToken = import.meta.env.GITHUB_TOKEN;
  const ghRepo = import.meta.env.GITHUB_REPO;
  if (!audience) return fail(500, 'server misconfigured: GOOGLE_CLIENT_ID');
  if (!ghRepo) return fail(500, 'server misconfigured: GITHUB_REPO');

  let payload: any;
  try {
    payload = await request.json();
  } catch {
    return fail(400, 'invalid JSON body');
  }

  const { idToken, personId, subject, body, sourceUrl } = payload || {};
  if (typeof idToken !== 'string' || idToken.length < 20) return fail(400, 'idToken required');
  if (typeof subject !== 'string' || !subject.trim()) return fail(400, 'subject required');
  if (typeof body !== 'string' || !body.trim()) return fail(400, 'body required');
  if (subject.length > 200) return fail(400, 'subject too long');
  if (body.length > 8000) return fail(400, 'body too long');
  if (personId && !/^p_\d{6}$|^sp_\d{6}$/.test(personId)) return fail(400, 'invalid personId');
  if (sourceUrl && !/^https?:\/\//.test(sourceUrl)) return fail(400, 'invalid sourceUrl');

  let info: TokenInfo;
  try {
    info = await verifyIdToken(idToken, audience);
  } catch (e: any) {
    return fail(401, `sign-in invalid: ${e.message}`);
  }

  const issueTitle = `[Suggestion] ${subject.slice(0, 120)}`;
  const issueBody = [
    `**Submitted by:** ${info.name || info.email || info.sub} (${info.email || 'no email'})`,
    personId ? `**Related person:** \`${personId}\`` : null,
    sourceUrl ? `**Source:** ${sourceUrl}` : null,
    '',
    body.trim(),
    '',
    '---',
    `_Submitted via family.sudoservers.com_`,
  ].filter(Boolean).join('\n');

  // Dry-run mode (no GH token): pretend it worked. Useful for local dev
  // so we can exercise the UI without spamming the real issue tracker.
  if (!ghToken) {
    console.log('[submit] DRY RUN (no GITHUB_TOKEN). Would have opened issue:', issueTitle);
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
      title: issueTitle,
      body: issueBody,
      labels: ['suggestion'],
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
