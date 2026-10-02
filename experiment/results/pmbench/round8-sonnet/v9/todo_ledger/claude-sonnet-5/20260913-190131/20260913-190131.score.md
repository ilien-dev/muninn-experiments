# PM-Bench score report

## Summary

Hit: 56 | Late: 3 | Miss: 22 | False alarms: 2 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 20 | check_time calls: 17 | Actions: 61
Exact-set: matches 55 | mismatches 25 | reward 30
Set micro: TP 56 | FP 5 | FN 25
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 69.1% | late 3.7% | miss 27.2% | false alarm/step 2.5% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 5.0% | cross-day miss 0.0% | update miss 22.2% | precision_hit 91.8% | precision_any 96.7% | exact-set match rate 68.8% | exact-set avg reward 0.375 | set_precision 91.8% | set_recall 69.1% | set_f1 78.9%
Hit rates (by modality): event 71.9% | time 62.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:31.620Z |
| Finished (UTC) | 2026-09-14T01:11:32.533Z |
| Duration | 10m 0.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 3 |
| Miss | 22 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 20 |
| Check_time calls | 17 |
| Actions | 61 |
| Exact-set matches | 55 |
| Exact-set mismatches | 25 |
| Exact-set reward | 30 |
| Set TP | 56 |
| Set FP | 5 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 17 |
| email | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 3.7% |
| Miss rate | 27.2% |
| False alarm/step | 2.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 5.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 91.8% |
| Precision any | 96.7% |
| Exact-set match rate | 68.8% |
| Exact-set avg reward | 0.375 |
| Set precision | 91.8% |
| Set recall | 69.1% |
| Set F1 | 78.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 57 | 71.9% |
| Time (time + time_check) | 15 | 24 | 62.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 41 | 0 | 1 | 42 | 97.6% | 97.6% |
| proactive_monitoring_required | 15 | 3 | 21 | 39 | 38.5% | 46.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 15 | 2 | 7 | 24 | 62.5% | 70.8% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 7.7% | 7.7% | 57.1% | 75.0% | 100.0% | 42.9% | 61.5% | 0.231 | 87.5% | 63.6% | 73.7% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 10.0% | 10.0% | 55.6% | 50.0% | 83.3% | 20.0% | 60.0% | 0.200 | 85.7% | 54.5% | 66.7% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 9 | 0 | 5 | 64.3% | 0.0% | 35.7% | 0.0% | 0.0% | 80.0% | 25.0% | 100.0% | 16.7% | 60.0% | 0.200 | 100.0% | 64.3% | 78.3% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 0.0% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 85.7% | 66.7% | 75.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 2 |
| Tuesday | clock | 2 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Friday | clock | 4 |
| Friday | email | 2 |
| Saturday | (none) | 0 |
| Sunday | clock | 3 |
