# PM-Bench score report

## Summary

Hit: 54 | Late: 1 | Miss: 26 | False alarms: 2 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 24 | check_time calls: 21 | Actions: 57
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 54 | FP 3 | FN 27
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 0
Rates: hit 66.7% | late 1.2% | miss 32.1% | false alarm/step 2.5% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 14.3% | update miss 33.3% | precision_hit 94.7% | precision_any 96.5% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 94.7% | set_recall 66.7% | set_f1 78.3%
Hit rates (by modality): event 68.4% | time 62.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | n/a |
| Finished (UTC) | n/a |
| Duration | n/a |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 54 |
| Late | 1 |
| Miss | 26 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 24 |
| Check_time calls | 21 |
| Actions | 57 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 54 |
| Set FP | 3 |
| Set FN | 27 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 21 |
| email | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 66.7% |
| Late rate | 1.2% |
| Miss rate | 32.1% |
| False alarm/step | 2.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 94.7% |
| Precision any | 96.5% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 94.7% |
| Set recall | 66.7% |
| Set F1 | 78.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 15 | 24 | 62.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 15 | 1 | 23 | 39 | 38.5% | 41.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 15 | 0 | 9 | 24 | 62.5% | 62.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 10.0% | 10.0% | 44.4% | 50.0% | 66.7% | 20.0% | 50.0% | 0.000 | 83.3% | 45.5% | 58.8% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 9.1% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 0.0% | 75.0% | 75.0% | 100.0% | 50.0% | 75.0% | 0.500 | 90.0% | 75.0% | 81.8% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 0.0% | 0.0% | 70.0% | 25.0% | 87.5% | 16.7% | 60.0% | 0.200 | 100.0% | 57.1% | 72.7% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 81.8% | 0.636 | 100.0% | 77.8% | 87.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 2 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 3 |
| Friday | clock | 4 |
| Friday | email | 2 |
| Saturday | clock | 2 |
| Sunday | clock | 5 |
