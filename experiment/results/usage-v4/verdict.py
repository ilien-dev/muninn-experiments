#!/usr/bin/env python3
"""Read two builds' counts and print, per usage-v4 rule, the base figure, the candidate figure and
pass/fail under the binding reading (pre-registration and its three amendments).

  python -I verdict.py <base sha16> <candidate sha16> [--split heldout|design|all] [--json]

Held-out rules (A1-A3, C1) read --split (default heldout). A1 and A2 are read on counts: the
noise and durable records each build emits; a per-item reading needs the private per-item files
in the work directory. C2 needs the candidate's c_delivery run with `--against <base>`; its
`init --check-budget` half is not in the counts and is printed as "run separately". E must come
from one interleaved `e_perf.py --bin <base> --against <candidate>` run. A section with no counts
file for a build prints "missing".
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('base')
ap.add_argument('cand')
ap.add_argument('--split', default='heldout', choices=['design', 'heldout', 'all'])
ap.add_argument('--json', action='store_true')
ap.add_argument('--counts-dir', help='read counts from this directory instead of counts/ (for checks on doctored copies)')
a = ap.parse_args()


def load(sec, b):
    p = os.path.join(a.counts_dir or os.path.join(HERE, 'counts'), '%s_%s.json' % (sec, b))
    return json.load(open(p)) if os.path.isfile(p) else None


rows = []


EMPTY = (None, '', {}, [])


def out(rule, base, cand, ok, note='', verdict=None):
    """An absent or empty input is `missing`, never `pass`."""
    if verdict is None:
        if ok is None or base in EMPTY or cand in EMPTY:
            verdict = 'missing'
        else:
            verdict = 'pass' if ok else 'fail'
    rows.append({'rule': rule, 'base': base, 'candidate': cand, 'verdict': verdict, 'note': note})


def frac(x):
    n, d = x.split('/')
    return int(n), int(d)


sp = a.split
# ---------------------------------------------------------------------------------------------- A
A0, A1 = load('a_extract', a.base), load('a_extract', a.cand)
a_inputs_ok = all((X or {}).get('inputs', {}).get('status', 'ok') == 'ok' for X in (A0, A1))
if A0 and A1 and not a_inputs_ok:
    for r in ('A1', 'A2', 'A3'):
        out(r, None, None, None, 'missing input: a staged extraction transcript is gone or changed (tenth amendment)')
elif A0 and A1 and sp in A0['splits'] and sp in A1['splits']:
    p0, p1 = A0['splits'][sp]['precision_set'], A1['splits'][sp]['precision_set']
    r0, r1 = A0['splits'][sp]['recall_set'], A1['splits'][sp]['recall_set']
    n0 = p0['noise_emitted'] + r0['noise_candidates']
    n1 = p1['noise_emitted'] + r1['noise_candidates']
    d0 = p0['durable_emitted'] + r0['candidates_by_class'].get('durable', 0)
    d1 = p1['durable_emitted'] + r1['candidates_by_class'].get('durable', 0)
    removed = (n0 - n1) / n0 if n0 else 0
    lost = (d0 - d1) / d0 if d0 else 0
    out('A1 filters: noise removed >= 30 %, durable lost <= 5 %', 'noise %d, durable %d' % (n0, d0), 'noise %d, durable %d' % (n1, d1),
        removed >= 0.30 and lost <= 0.05, 'count-based, both sets; removed %.3f, lost %.3f' % (removed, lost))
    add_d = r1['durable_emitted'] - r0['durable_emitted']
    add_n = r1['noise_candidates'] - r0['noise_candidates']
    out('A2 recall rules: added durable >= added noise', 'durable %d, noise %d' % (r0['durable_emitted'], r0['noise_candidates']),
        'durable %d, noise %d' % (r1['durable_emitted'], r1['noise_candidates']), add_d >= max(add_n, 0) and add_d > 0, 'recall set')
    mp0, mp1 = r0['message_precision'] or 0, r1['message_precision'] or 0
    out('A3 new extractor: precision >= 2x base, recall >= base', 'precision %s, recall %s' % (r0['message_precision'], r0['recall']),
        'precision %s, recall %s' % (r1['message_precision'], r1['recall']), mp1 >= 2 * mp0 and (r1['recall'] or 0) >= (r0['recall'] or 0), 'recall set')
else:
    out('A', None, None, None)
# ---------------------------------------------------------------------------------------------- B
B0, B1 = load('b_retire', a.base), load('b_retire', a.cand)
if B0 and B1:
    s0, s1 = B0['splits']['all'], B1['splits']['all']
    if 'b1' in s0 and 'b1' in s1 and (s0['b1'].get('status', 'ok') != 'ok' or s1['b1'].get('status', 'ok') != 'ok'):
        for r in ('B1 loss retired: candidate <= base (score.py rule)', 'B1 both valid retirements happen (earliest row)'):
            out(r, None, None, None, 'missing input: a staged B1 transcript is gone or changed (tenth amendment)')
    elif 'b1' in s0 and 'b1' in s1:
        v = s1['b1']['valid_states_earliest_row']
        out('B1 loss retired: candidate <= base (score.py rule)', s0['b1']['loss_retired_total'], s1['b1']['loss_retired_total'],
            s1['b1']['loss_retired_total'] <= s0['b1']['loss_retired_total'], 'earliest-row reading: %d -> %d (secondary)' % (s0['b1']['loss_retired_total_earliest_row'], s1['b1']['loss_retired_total_earliest_row']))
        out('B1 both valid retirements happen (earliest row)', s0['b1'].get('valid_states_earliest_row'), v, bool(v) and all(x == 'retired' for x in v.values()))
        k0, k1 = s0['b1'].get('kind_free'), s1['b1'].get('kind_free')
        if k0 and k1:
            # twelfth amendment: where the kind-bound reading is absent, the kind-free one binds
            out('B1 (12th) loss retired, binding reading: <= base and <= 5', k0['loss_retired_total'], k1['loss_retired_total'],
                k1['loss_retired_total'] <= k0['loss_retired_total'] and k1['loss_retired_total'] <= 5,
                'kind-free split %s -> %s; binding split %s -> %s' % (k0['split'], k1['split'], k0['binding_split'], k1['binding_split']))
            fv = k1['valid_states_earliest_row']
            out('B1 (12th) both valid retirements happen (binding, earliest row)', k0['valid_states_earliest_row'], fv,
                bool(fv) and all(x == 'retired' for x in fv.values()))
        else:
            out('B1 (12th) kind-free reading', None, None, None, 'missing: rerun b_retire.py --parts b1 --score-only')
    if 'b2' in s0 and 'b2' in s1:
        w0, w1 = s0['b2'], s1['b2']
        out('B2 reword retires nothing (any kind)', w0['reword']['retired'], w1['reword']['retired'], w1['reword']['retired'] == 0,
            'typed only: %d -> %d (secondary)' % (w0['reword']['retired_typed'], w1['reword']['retired_typed']))
        out('B2 A-B-A serves A and not B (typed blocks)', '%s/%s' % (w0['aba']['served_A_typed'], w0['aba']['served_B_typed']),
            '%s/%s' % (w1['aba']['served_A_typed'], w1['aba']['served_B_typed']), w1['aba']['served_A_typed'] and not w1['aba']['served_B_typed'], 'A/B')
        r0, r1 = w0['revert_one_maintain'], w1['revert_one_maintain']
        out('B2 revert retires every record of the reverted commit (one maintain)', '%d/%d' % (r0['reverted_commit_retired'], r0['reverted_commit_records']),
            '%d/%d' % (r1['reverted_commit_retired'], r1['reverted_commit_records']),
            r1['reverted_commit_records'] > 0 and r1['reverted_commit_retired'] == r1['reverted_commit_records'] if r1['reverted_commit_records'] else None)
    if 'b3' in s0 and 'b3' in s1:
        ok = True
        notes, bsum, csum = [], [], []
        for k in sorted(s0['b3']):
            if not k.startswith('registered/'):
                continue
            arm = k.split('/')[1]
            b, c = s0['b3'][k], s1['b3'].get(k)
            if not c:
                ok = False
                continue
            if arm == 'both':
                ok &= frac(c['retired_a'])[0] >= frac(b['retired_a'])[0] and frac(c['kept_b'])[0] >= frac(b['kept_b'])[0]
            else:
                ok &= frac(c['retired_a'])[0] <= frac(b['retired_a'])[0]
            notes.append('%s kb %s->%s' % (k.split('/', 1)[1], b['kept_b'], c['kept_b']))
            bsum.append('%s %s' % (k.split('/', 1)[1], b['retired_a']))
            csum.append('%s %s' % (k.split('/', 1)[1], c['retired_a']))
        dated = ['%s ra %s->%s' % (k.split('/', 1)[1], s0['b3'][k]['retired_a'], s1['b3'].get(k, {}).get('retired_a')) for k in sorted(s0['b3']) if k.startswith('dated/')]
        out('B3 registered loop8: both arms retired_a, kept_b >= base; noise retired_a <= base', 'retired_a ' + ', '.join(bsum), 'retired_a ' + ', '.join(csum),
            ok if bsum else None, '; '.join(notes) + ' | dated (secondary): ' + '; '.join(dated))
else:
    out('B', None, None, None)
# ---------------------------------------------------------------------------------------------- C
C0, C1 = load('c_delivery', a.base), load('c_delivery', a.cand)
if C0 and C1:
    # C1 reads the counts scored with frozen + pool labels when both builds have them (fourth amendment)
    P0, P1 = load('c_delivery', a.base + '-pool'), load('c_delivery', a.cand + '-pool')
    use_pool = bool(P0 and P1 and P0['splits'].get(sp, {}).get('c12') and P1['splits'].get(sp, {}).get('c12'))
    Q0, Q1 = (P0, P1) if use_pool else (C0, C1)
    c0, c1 = Q0['splits'].get(sp, {}).get('c12'), Q1['splits'].get(sp, {}).get('c12')  # a split a build has no prompt counts for reads missing
    if c0 and c1:
        out('C1 unrelated returned falls >= 30 %, useful falls <= 1', 'unrelated %d, useful %d (unscored %d)' % (c0['unrelated_returned'], c0['useful_returned'], c0['unlabelled_returned']),
            'unrelated %d, useful %d (unscored %d)' % (c1['unrelated_returned'], c1['useful_returned'], c1['unlabelled_returned']),
            c1['unrelated_returned'] <= 0.7 * c0['unrelated_returned'] and c1['useful_returned'] >= c0['useful_returned'] - 1,
            'split %s; labels %s; returned pairs still unscored: base %d of %d, candidate %d of %d' % (
                sp, 'frozen + pool extension' if use_pool else 'frozen only', c0['unlabelled_returned'], c0['returned'], c1['unlabelled_returned'], c1['returned']))
    # C2 is not a held-out rule: it reads every prompt (split all)
    ca0, ca1 = C0['splits']['all'].get('c12'), C1['splits']['all'].get('c12')
    same = (ca1 or {}).get('c2_same_ids')
    if same and same.get('against') == a.base and same['prompts']:
        out('C2 mean tokens on prompts with the same ids falls', same['mean_tokens_against'], same['mean_tokens_this'],
            same['mean_tokens_this'] < same['mean_tokens_against'], 'n=%d prompts, split all; all-prompt mean %s -> %s (secondary)' % (same['prompts'], ca0['mean_tokens'], ca1['mean_tokens']))
    else:
        out('C2 mean tokens on prompts with the same ids falls', (ca0 or {}).get('mean_tokens'), (ca1 or {}).get('mean_tokens'), None, 'run the candidate with --against %s' % a.base)
    out('C2 init --check-budget passes on the candidate', '', '', None, 'not in the counts: run `muninn init --check-budget` built with --features exact-tokens', verdict='manual')
    t0, t1 = C0['splits']['all'].get('c3'), C1['splits']['all'].get('c3')
    if t0 and t1:
        x0, x1 = t0['t1_cut_for_budget'], t1['t1_cut_for_budget']
        out('C3 cut record offered again in the same session (all of them)', '%d/%d' % (x0['same_session'], x0['tried']), '%d/%d' % (x1['same_session'], x1['tried']),
            x1['tried'] > 0 and x1['same_session'] == x1['tried'])
        y0, y1 = t0.get('t1_listed_in_catalogue'), t1.get('t1_listed_in_catalogue')
        # eighth amendment: the denominator is the listed records the build's own fresh-session
        # control returns; the others are counted and printed, not scored
        if y0 and y1 and 'returned_by_fresh_control' in y0 and 'returned_by_fresh_control' in y1:
            out('C3 catalogue-only record offered again in the same session (of those its fresh control returns)',
                '%d/%d' % (y0['same_session_of_those'], y0['returned_by_fresh_control']),
                '%d/%d' % (y1['same_session_of_those'], y1['returned_by_fresh_control']),
                y1['same_session_of_those'] == y1['returned_by_fresh_control'] if y1['returned_by_fresh_control'] else None,
                'excluded, not returned by the fresh control: base %d, candidate %d (ids %s); tried base %d, candidate %d' % (
                    y0['excluded_not_returned_fresh'], y1['excluded_not_returned_fresh'], y1['excluded_ids'], y0['tried'], y1['tried']))
        else:
            out('C3 catalogue-only record offered again in the same session (of those its fresh control returns)', None, None, None,
                'counts predate the eighth amendment: rerun c_delivery --parts c3')
        out('C3 offered again after compaction and Stop', t0['t2_after_compaction']['offered_again_after_stop'], t1['t2_after_compaction']['offered_again_after_stop'],
            t1['t2_after_compaction']['offered_again_after_stop'] == 1)
        z0, z1 = t0['t3_stale_twin'], t1['t3_stale_twin']
        out('C3 no retired statement served through its episode twin', 'W02 %d, L01 %d' % (z0['W02:prompts_with_stale_twin'], z0['L01:prompts_with_stale_twin']),
            'W02 %d, L01 %d' % (z1['W02:prompts_with_stale_twin'], z1['L01:prompts_with_stale_twin']),
            z1['W02:prompts_with_stale_twin'] == 0 and z1['L01:prompts_with_stale_twin'] == 0)
    # C4 shares are read on --split, with the pool's session-start labels when both builds' -pool
    # counts carry them; coverage is read on today's copies (split all), seventh amendment
    # the pool's slot labels count only when they passed their gate and were merged (pool_units_used > 0)
    pool4 = bool(P0 and P1 and all((X['splits'].get(sp, {}).get('c4') or {}).get('all_slots') and (X['splits'].get(sp, {}).get('c4') or {}).get('pool_units_used', 0) > 0 for X in (P0, P1)))
    # without usable pool slot labels, a final+pool run's C4 is scored on the frozen labels only:
    # read it when both builds have it for this split, else the frozen run's counts
    has4 = lambda X: bool(X and (X['splits'].get(sp, {}).get('c4') or {}).get('all_slots'))
    if pool4:
        S0, S1 = P0, P1
    elif has4(P0) and has4(P1):
        S0, S1 = P0, P1
    else:
        S0, S1 = C0, C1
    g0, g1 = S0['splits'].get(sp, {}).get('c4'), S1['splits'].get(sp, {}).get('c4')
    if g0 and g1 and 'all_slots' in g0 and 'all_slots' in g1:
        l0, l1 = g0['all_slots'], g1['all_slots']
        un0 = g0['blocks']['unlabelled'] + g0['catalogue']['unlabelled']
        un1 = g1['blocks']['unlabelled'] + g1['catalogue']['unlabelled']
        out('C4 share worth the slot does not fall (lenient and strict)', '%s / %s (unscored %d)' % (l0['share_lenient_of_labelled'], l0['share_strict_of_labelled'], un0),
            '%s / %s (unscored %d)' % (l1['share_lenient_of_labelled'], l1['share_strict_of_labelled'], un1),
            l1['share_lenient_of_labelled'] >= l0['share_lenient_of_labelled'] and l1['share_strict_of_labelled'] >= l0['share_strict_of_labelled'],
            'split %s; labels %s; unlabelled slots not scored: base %d, candidate %d' % (sp, 'frozen + pool slots' if pool4 else 'frozen only', un0, un1))
    else:
        out('C4 share worth the slot does not fall (lenient and strict)', None, None, None, 'no C4 counts for split %s' % sp)
    # coverage does not depend on labels: the newest of the two counts files that carry it
    pick = lambda Cx, Px: (Px if Px and Px['splits'].get('all', {}).get('c4', {}).get('whole_list_today') else Cx)['splits']['all'].get('c4', {})
    v0, v1 = pick(C0, P0), pick(C1, P1)
    if v0.get('coverage_today') and v1.get('coverage_today'):
        cov0 = sum(v[k]['neither'] for v in v0['coverage_today'].values() for k in v)
        cov1 = sum(v[k]['neither'] for v in v1['coverage_today'].values() for k in v)
        wl1 = v1.get('whole_list_today') or {}
        truthful = all(x.get('truthful') is True for x in wl1.values()) if wl1 else None
        out('C4 (amended) corrections and invariants neither shown nor listed do not rise', 'neither %d' % cov0, 'neither %d' % cov1, cov1 <= cov0,
            'literal clause (every one shown or listed): %s' % ('met' if cov1 == 0 else 'not met, %d neither' % cov1))
        out('C4 (amended) the catalogue says truthfully whether its list is whole', '%d stores' % len(v0.get('whole_list_today') or {}),
            '%s of %d stores truthful' % (sum(1 for x in wl1.values() if x.get('truthful') is True), len(wl1)) if wl1 else None,
            truthful, 'stores with no closing line read missing' if wl1 and any(x.get('truthful') is None for x in wl1.values()) else '')
    w0, w1 = C0['splits']['all'].get('c5'), C1['splits']['all'].get('c5')
    if w0 and w1:
        out('C5 Spanish recall does not fall', w0['usage_v2']['spanish_reached'], w1['usage_v2']['spanish_reached'], w1['usage_v2']['spanish_reached'] >= w0['usage_v2']['spanish_reached'],
            'English %d -> %d' % (w0['usage_v2']['english_reached'], w1['usage_v2']['english_reached']))
        out('C5 gender pairs: more than base match', w0['gender_flip_W02']['found_top8'], w1['gender_flip_W02']['found_top8'], w1['gender_flip_W02']['found_top8'] > w0['gender_flip_W02']['found_top8'],
            'of %d' % w1['gender_flip_W02']['asked'])
        out('C5 every kind returned by the route that names it', '%d/%d' % (w0['routed_away']['returned'], w0['routed_away']['records']),
            '%d/%d' % (w1['routed_away']['returned'], w1['routed_away']['records']), w1['routed_away']['returned'] == w1['routed_away']['records'],
            'controls %d/%d' % (w1['routed_away']['control_returned'], w1['routed_away']['control_records']))
        f0, f1 = w0['all_flag'], w1['all_flag']
        out('C5 --all uses every word: "what about w" finds more than base, one word not below base', 'what about %d, one word %d' % (f0['what_about_found'], f0['one_word_found']),
            'what about %d, one word %d' % (f1['what_about_found'], f1['one_word_found']),
            f1['what_about_found'] > f0['what_about_found'] and f1['one_word_found'] >= f0['one_word_found'] if f1['asked'] else None, 'of %d asked' % f1['asked'])
else:
    out('C', None, None, None)
# ---------------------------------------------------------------------------------------------- D
D0 = load('d_removals', a.base)
if D0:
    x = D0['splits']['all']
    out('D graph and cues: no ledger row from a dir/symbol/file/tool cue', x['ledger_rows_naming_dir_symbol_file_or_tool_cue'], 'store reading', x['ledger_rows_naming_dir_symbol_file_or_tool_cue'] == 0, 'second half: B3 and delivery ids unchanged (d_removals --against)')
    out('D sidecar: no store holds a vector', x['record_vec_rows'], 'store reading', x['record_vec_rows'] == 0, 'second half: usage-v2 recall unchanged (C5)')
    out('D commit subjects: no hook delivery names one', x['commit_linked_delivered_by_hook'], 'store reading', not any(k.endswith(':commit') for k in x['commit_linked_delivered_by_hook']),
        'said: swap records are delivered and are not commit subjects')
    D1 = load('d_removals', a.cand)
    if D1 and 'against' in D1:
        ag = D1['against']
        ids = ag['delivery_ids'].get('all', {})
        out('D removal leaves B3 and delivery ids unchanged', 'comparison with %s' % ag['build'], '%s/%s same, b3 equal %s' % (ids.get('same_ids'), ids.get('prompts_compared'), ag['b3_equal']),
            ag['b3_equal'] and ids.get('same_ids') == ids.get('prompts_compared'))
# ---------------------------------------------------------------------------------------------- E
E0, E1 = load('e_perf', a.base), load('e_perf', a.cand)
if E0 and E1 and 'perf' in E0['splits']['all'] and 'perf' in E1['splits']['all']:
    h0, h1 = E0['splits']['all']['perf']['hooks'], E1['splits']['all']['perf']['hooks']
    p0, p1 = E0['splits']['all']['perf'], E1['splits']['all']['perf']
    inter = p1.get('interleaved_with') == [E0['binary_sha256']] or p0.get('interleaved_with') == [E1['binary_sha256']]
    # harness rev 2: each build timed by a bench of its own source, every run checked; rev-1 counts
    # timed the base on a store it refused and are never a reading
    # revision 3: equal workloads by seed count and fingerprint, a must-deliver case on both builds.
    # Revision-2 counts called a row count equal and did not gate delivery: they read missing.
    rev = E0.get('harness_rev', 1) >= 3 and E1.get('harness_rev', 1) >= 3
    checked = all(p.get('store_checks', {}).get('all_hooks_ok') for p in (p0, p1))
    valid = inter and rev and checked
    why = [] if valid else [w for w, c in (('not from one interleaved run', inter), ('counts from before harness rev 3', rev), ('bench stores not checked', checked)) if not c]
    wl = E1.get('workload') or {}
    if valid and wl.get('equal') is not True:
        valid, why = False, ['workloads not equal: ' + wl.get('caveat', 'not recorded')]
    if valid and (wl.get('must_deliver') or {}).get('verdict') != 'both':
        valid, why = False, ['must-deliver case: %s' % (wl.get('must_deliver') or {}).get('verdict', 'not recorded')]
    note = ('missing: ' + ', '.join(why)) if why else 'workloads equal, must-deliver on both'
    for h in h0:
        out('E %s p95 <= 1.10 x base' % h, h0[h]['p95_median'], h1[h]['p95_median'], h1[h]['p95_median'] <= 1.10 * h0[h]['p95_median'] if valid else None, note)
    s0, s1 = E0['splits']['all'].get('stop_ingest_W02'), E1['splits']['all'].get('stop_ingest_W02')
    if s0 and s1:
        md_ok = (wl.get('must_deliver') or {}).get('verdict') == 'both'
        sv = rev and md_ok and s0.get('stop_hooks_ok') is True and s1.get('stop_hooks_ok') is True and s1.get('schema_after') == s1.get('schema_expected') and s0.get('schema_after') == s0.get('schema_before') and (s1.get('interleaved_with') == [E0['binary_sha256']] or s0.get('interleaved_with') == [E1['binary_sha256']])
        out('E Stop with ingest, W02: candidate median lower', s0['median_ms'], s1['median_ms'], s1['median_ms'] < s0['median_ms'] if sv else None,
            ('migration (first write open) %s ms, not counted' % s1.get('first_write_open_ms')) if sv else 'missing: counts from before harness rev 3, must-deliver not on both, a Stop error, schema not as expected, or not interleaved')
else:
    out('E', None, None, None)

EXPECTED = ['A1', 'A2', 'A3', 'B1 loss', 'B1 both valid', 'B2 reword', 'B2 A-B-A', 'B2 revert', 'B3', 'C1', 'C2 mean', 'C2 init', 'C3 cut', 'C3 catalogue',
            'C3 offered again after', 'C3 no retired', 'C4 share', 'C4 (amended) corrections', 'C4 (amended) the catalogue', 'C5 Spanish', 'C5 gender', 'C5 every kind', 'C5 --all', 'D graph', 'D sidecar',
            'D commit', 'D removal', 'E SessionStart', 'E SubagentStart', 'E UserPromptSubmit_full', 'E UserPromptSubmit_gated', 'E Stop']
for e in EXPECTED:
    if not any(r['rule'].startswith(e) for r in rows):
        rows.append({'rule': e, 'base': None, 'candidate': None, 'verdict': 'missing', 'note': 'no input'})
rows = [r for r in rows if r['rule'] not in ('A', 'B', 'C', 'E') or r['verdict'] != 'missing' or False]

if a.json:
    print(json.dumps(rows, indent=1))
else:
    for r in rows:
        print('%-8s %-70s base=%s cand=%s %s' % (r['verdict'], r['rule'][:70], r['base'], r['candidate'], ('| ' + r['note']) if r['note'] else ''))
