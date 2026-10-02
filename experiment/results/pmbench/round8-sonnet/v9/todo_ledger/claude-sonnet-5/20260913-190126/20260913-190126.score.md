# PM-Bench score report

## Summary

Hit: 56 | Late: 2 | Miss: 23 | False alarms: 6 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 24 | check_time calls: 21 | Actions: 64
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 56 | FP 8 | FN 25
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 5 | late 0 | miss 4 | canceled 2 | total 11 | violations 3
Rates: hit 69.1% | late 2.5% | miss 28.4% | false alarm/step 7.5% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 5.0% | cross-day miss 0.0% | update miss 44.4% | precision_hit 87.5% | precision_any 90.6% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 87.5% | set_recall 69.1% | set_f1 77.2%
Hit rates (by modality): event 73.7% | time 58.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:26.420Z |
| Finished (UTC) | 2026-09-14T01:11:40.292Z |
| Duration | 10m 13.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 2 |
| Miss | 23 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 24 |
| Check_time calls | 21 |
| Actions | 64 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 56 |
| Set FP | 8 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 21 |
| email | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 2.5% |
| Miss rate | 28.4% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 5.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 44.4% |
| Precision hit | 87.5% |
| Precision any | 90.6% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 87.5% |
| Set recall | 69.1% |
| Set F1 | 77.2% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 57 | 73.7% |
| Time (time + time_check) | 14 | 24 | 58.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 14 | 2 | 23 | 39 | 35.9% | 41.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 14 | 1 | 9 | 24 | 58.3% | 62.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 0.0% | 0.0% | 57.1% | 50.0% | 100.0% | 28.6% | 69.2% | 0.385 | 100.0% | 54.5% | 70.6% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 20.0% | 20.0% | 66.7% | 50.0% | 100.0% | 20.0% | 50.0% | 0.000 | 77.8% | 63.6% | 70.0% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 88.9% | 33.3% | 100.0% | 25.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 9 | 0 | 5 | 64.3% | 0.0% | 35.7% | 30.0% | 10.0% | 80.0% | 25.0% | 100.0% | 16.7% | 60.0% | 0.200 | 75.0% | 64.3% | 69.2% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 2 |
| Tuesday | clock | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 3 |
| Friday | clock | 5 |
| Friday | email | 1 |
| Saturday | clock | 2 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |
