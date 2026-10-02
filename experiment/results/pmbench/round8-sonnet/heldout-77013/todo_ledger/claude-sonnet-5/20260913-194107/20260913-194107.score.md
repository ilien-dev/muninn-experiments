# PM-Bench score report

## Summary

Hit: 52 | Late: 0 | Miss: 29 | False alarms: 2 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 22 | check_time calls: 18 | Actions: 54
Exact-set: matches 58 | mismatches 26 | reward 32
Set micro: TP 52 | FP 2 | FN 29
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 0
Rates: hit 64.2% | late 0.0% | miss 35.8% | false alarm/step 2.4% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 2.4% | cross-day miss 14.3% | update miss 33.3% | precision_hit 96.3% | precision_any 96.3% | exact-set match rate 69.0% | exact-set avg reward 0.381 | set_precision 96.3% | set_recall 64.2% | set_f1 77.0%
Hit rates (by modality): event 67.9% | time 56.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:41:07.686Z |
| Finished (UTC) | 2026-09-14T01:49:53.013Z |
| Duration | 8m 45.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 52 |
| Late | 0 |
| Miss | 29 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 22 |
| Check_time calls | 18 |
| Actions | 54 |
| Exact-set matches | 58 |
| Exact-set mismatches | 26 |
| Exact-set reward | 32 |
| Set TP | 52 |
| Set FP | 2 |
| Set FN | 29 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| clock | 18 |
| course_portal | 1 |
| email | 1 |
| price_tracker | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 64.2% |
| Late rate | 0.0% |
| Miss rate | 35.8% |
| False alarm/step | 2.4% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 2.4% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 96.3% |
| Precision any | 96.3% |
| Exact-set match rate | 69.0% |
| Exact-set avg reward | 0.381 |
| Set precision | 96.3% |
| Set recall | 64.2% |
| Set F1 | 77.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 56 | 67.9% |
| Time (time + time_check) | 14 | 25 | 56.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 14 | 0 | 27 | 41 | 34.1% | 34.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 14 | 0 | 11 | 25 | 56.0% | 56.0% |
| course_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 7.7% | 7.7% | 80.0% | 50.0% | 100.0% | 40.0% | 76.9% | 0.538 | 85.7% | 66.7% | 75.0% |
| Tuesday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 75.0% | 50.0% | 100.0% | 33.3% | 72.7% | 0.455 | 100.0% | 66.7% | 80.0% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 7.1% | 7.1% | 60.0% | 100.0% | 75.0% | 80.0% | 78.6% | 0.571 | 87.5% | 77.8% | 82.4% |
| Thursday | 9 | 0 | 7 | 56.2% | 0.0% | 43.8% | 0.0% | 0.0% | 69.2% | 0.0% | 90.0% | 0.0% | 50.0% | 0.000 | 100.0% | 56.2% | 72.0% |
| Friday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 0.0% | 0.0% | 62.5% | 33.3% | 100.0% | 16.7% | 66.7% | 0.333 | 100.0% | 54.5% | 70.6% |
| Saturday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 62.5% | 75.0% | 100.0% | 42.9% | 66.7% | 0.333 | 100.0% | 66.7% | 80.0% |
| Sunday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 66.7% | 66.7% | 100.0% | 33.3% | 66.7% | 0.333 | 100.0% | 66.7% | 80.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 2 |
| Tuesday | clock | 2 |
| Wednesday | appointment_portal | 1 |
| Wednesday | clock | 5 |
| Wednesday | email | 1 |
| Thursday | clock | 1 |
| Thursday | price_tracker | 1 |
| Friday | clock | 2 |
| Friday | course_portal | 1 |
| Saturday | clock | 4 |
| Sunday | clock | 2 |
