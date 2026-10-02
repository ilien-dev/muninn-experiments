# PM-Bench score report

## Summary

Hit: 57 | Late: 2 | Miss: 22 | False alarms: 5 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 5 | state query calls: 30 | check_time calls: 27 | Actions: 64
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 57 | FP 7 | FN 24
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 0
Rates: hit 70.4% | late 2.5% | miss 27.2% | false alarm/step 6.2% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 6.2% | cross-day miss 0.0% | update miss 22.2% | precision_hit 89.1% | precision_any 92.2% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 89.1% | set_recall 70.4% | set_f1 78.6%
Hit rates (by modality): event 68.4% | time 75.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:22.468Z |
| Finished (UTC) | 2026-09-14T01:08:21.454Z |
| Duration | 6m 59.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 57 |
| Late | 2 |
| Miss | 22 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 5 |
| State query calls | 30 |
| Check_time calls | 27 |
| Actions | 64 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 57 |
| Set FP | 7 |
| Set FN | 24 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 27 |
| email | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 70.4% |
| Late rate | 2.5% |
| Miss rate | 27.2% |
| False alarm/step | 6.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 6.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 89.1% |
| Precision any | 92.2% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 89.1% |
| Set recall | 70.4% |
| Set F1 | 78.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 18 | 24 | 75.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 18 | 2 | 19 | 39 | 46.2% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 18 | 1 | 5 | 24 | 75.0% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 7.7% | 7.7% | 57.1% | 75.0% | 100.0% | 42.9% | 61.5% | 0.231 | 87.5% | 63.6% | 73.7% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 66.7% | 50.0% | 100.0% | 20.0% | 70.0% | 0.400 | 100.0% | 63.6% | 77.8% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 77.8% | 66.7% | 87.5% | 50.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 0.0% | 0.0% | 80.0% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 100.0% | 78.6% | 88.0% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 18.2% | 18.2% | 60.0% | 50.0% | 75.0% | 40.0% | 45.5% | -0.091 | 62.5% | 55.6% | 58.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 4 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 5 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |
