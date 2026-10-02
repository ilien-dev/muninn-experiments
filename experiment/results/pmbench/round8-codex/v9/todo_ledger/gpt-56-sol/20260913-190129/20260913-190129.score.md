# PM-Bench score report

## Summary

Hit: 61 | Late: 8 | Miss: 12 | False alarms: 4 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 51 | check_time calls: 33 | Actions: 73
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 61 | FP 12 | FN 20
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 75.3% | late 9.9% | miss 14.8% | false alarm/step 5.0% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 11.2% | cross-day miss 0.0% | update miss 0.0% | precision_hit 83.6% | precision_any 94.5% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 83.6% | set_recall 75.3% | set_f1 79.2%
Hit rates (by modality): event 75.4% | time 75.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:29.531Z |
| Finished (UTC) | 2026-09-14T01:19:22.201Z |
| Duration | 17m 52.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 8 |
| Miss | 12 |
| False alarms | 4 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 51 |
| Check_time calls | 33 |
| Actions | 73 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 61 |
| Set FP | 12 |
| Set FN | 20 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 3 |
| calendar | 4 |
| clock | 33 |
| course_portal | 3 |
| email | 3 |
| library_hold | 2 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 75.3% |
| Late rate | 9.9% |
| Miss rate | 14.8% |
| False alarm/step | 5.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 11.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 83.6% |
| Precision any | 94.5% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 83.6% |
| Set recall | 75.3% |
| Set F1 | 79.2% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 43 | 57 | 75.4% |
| Time (time + time_check) | 18 | 24 | 75.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 19 | 8 | 12 | 39 | 48.7% | 69.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 18 | 4 | 2 | 24 | 75.0% | 91.7% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 8 | 2 | 1 | 72.7% | 18.2% | 9.1% | 7.7% | 23.1% | 57.1% | 100.0% | 100.0% | 57.1% | 53.8% | 0.077 | 72.7% | 72.7% | 72.7% |
| Wednesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 0.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 77.8% | 63.6% | 70.0% |
| Thursday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 9.1% | 9.1% | 88.9% | 66.7% | 100.0% | 50.0% | 81.8% | 0.636 | 90.9% | 83.3% | 87.0% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 10 | 2 | 2 | 71.4% | 14.3% | 14.3% | 10.0% | 20.0% | 80.0% | 50.0% | 100.0% | 33.3% | 50.0% | 0.000 | 76.9% | 71.4% | 74.1% |
| Sunday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 9.1% | 18.2% | 100.0% | 50.0% | 100.0% | 60.0% | 63.6% | 0.273 | 77.8% | 77.8% | 77.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | course_portal | 1 |
| Monday | email | 1 |
| Tuesday | calendar | 3 |
| Tuesday | clock | 6 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 5 |
| Thursday | shipment_status | 2 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Friday | library_hold | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 6 |
