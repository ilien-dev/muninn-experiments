# PM-Bench score report

## Summary

Hit: 56 | Late: 2 | Miss: 23 | False alarms: 1 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 24 | check_time calls: 23 | Actions: 59
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 56 | FP 3 | FN 25
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 0
Rates: hit 69.1% | late 2.5% | miss 28.4% | false alarm/step 1.2% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 14.3% | update miss 33.3% | precision_hit 94.9% | precision_any 98.3% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 94.9% | set_recall 69.1% | set_f1 80.0%
Hit rates (by modality): event 71.9% | time 62.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | n/a |
| Finished (UTC) | n/a |
| Duration | n/a |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 2 |
| Miss | 23 |
| False alarms | 1 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 24 |
| Check_time calls | 23 |
| Actions | 59 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 56 |
| Set FP | 3 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 23 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 2.5% |
| Miss rate | 28.4% |
| False alarm/step | 1.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 94.9% |
| Precision any | 98.3% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 94.9% |
| Set recall | 69.1% |
| Set F1 | 80.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 57 | 71.9% |
| Time (time + time_check) | 15 | 24 | 62.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 41 | 0 | 1 | 42 | 97.6% | 97.6% |
| proactive_monitoring_required | 15 | 2 | 22 | 39 | 38.5% | 43.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 15 | 1 | 8 | 24 | 62.5% | 66.7% |
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
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 0.0% | 62.5% | 100.0% | 83.3% | 66.7% | 75.0% | 0.500 | 90.0% | 75.0% | 81.8% |
| Saturday | 9 | 0 | 5 | 64.3% | 0.0% | 35.7% | 0.0% | 0.0% | 80.0% | 25.0% | 100.0% | 16.7% | 60.0% | 0.200 | 100.0% | 64.3% | 78.3% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 0.0% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 85.7% | 66.7% | 75.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Saturday | clock | 2 |
| Sunday | clock | 4 |
