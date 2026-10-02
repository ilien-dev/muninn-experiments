# PM-Bench score report

## Summary

Hit: 58 | Late: 1 | Miss: 22 | False alarms: 3 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 27 | check_time calls: 24 | Actions: 62
Exact-set: matches 59 | mismatches 21 | reward 38
Set micro: TP 58 | FP 4 | FN 23
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 2
Rates: hit 71.6% | late 1.2% | miss 27.2% | false alarm/step 3.8% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 0.0% | update miss 33.3% | precision_hit 93.5% | precision_any 95.2% | exact-set match rate 73.8% | exact-set avg reward 0.475 | set_precision 93.5% | set_recall 71.6% | set_f1 81.1%
Hit rates (by modality): event 73.7% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T12:05:08.923Z |
| Finished (UTC) | 2026-09-13T12:45:47.850Z |
| Duration | 40m 38.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 58 |
| Late | 1 |
| Miss | 22 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 27 |
| Check_time calls | 24 |
| Actions | 62 |
| Exact-set matches | 59 |
| Exact-set mismatches | 21 |
| Exact-set reward | 38 |
| Set TP | 58 |
| Set FP | 4 |
| Set FN | 23 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 24 |
| email | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 71.6% |
| Late rate | 1.2% |
| Miss rate | 27.2% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 33.3% |
| Precision hit | 93.5% |
| Precision any | 95.2% |
| Exact-set match rate | 73.8% |
| Exact-set avg reward | 0.475 |
| Set precision | 93.5% |
| Set recall | 71.6% |
| Set F1 | 81.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 57 | 73.7% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 16 | 1 | 22 | 39 | 41.0% | 43.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 16 | 0 | 8 | 24 | 66.7% | 66.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 10.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 87.5% | 63.6% | 73.7% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 88.9% | 33.3% | 100.0% | 25.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 9 | 0 | 5 | 64.3% | 0.0% | 35.7% | 20.0% | 10.0% | 80.0% | 25.0% | 100.0% | 16.7% | 60.0% | 0.200 | 81.8% | 64.3% | 72.0% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 81.8% | 0.636 | 100.0% | 77.8% | 87.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Saturday | clock | 2 |
| Sunday | clock | 5 |
