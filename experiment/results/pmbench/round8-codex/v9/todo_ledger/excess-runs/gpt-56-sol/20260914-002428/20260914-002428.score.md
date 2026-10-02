# PM-Bench score report

## Summary

Hit: 62 | Late: 6 | Miss: 13 | False alarms: 5 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 50 | check_time calls: 31 | Actions: 73
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 62 | FP 11 | FN 19
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 76.5% | late 7.4% | miss 16.0% | false alarm/step 6.2% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 0.0% | update miss 11.1% | precision_hit 84.9% | precision_any 93.2% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 84.9% | set_recall 76.5% | set_f1 80.5%
Hit rates (by modality): event 75.4% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:24:28.319Z |
| Finished (UTC) | 2026-09-14T06:37:38.004Z |
| Duration | 13m 9.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 62 |
| Late | 6 |
| Miss | 13 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 50 |
| Check_time calls | 31 |
| Actions | 73 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 62 |
| Set FP | 11 |
| Set FN | 19 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 4 |
| calendar | 3 |
| clock | 31 |
| course_portal | 3 |
| email | 2 |
| library_hold | 1 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 76.5% |
| Late rate | 7.4% |
| Miss rate | 16.0% |
| False alarm/step | 6.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 84.9% |
| Precision any | 93.2% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 84.9% |
| Set recall | 76.5% |
| Set F1 | 80.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 43 | 57 | 75.4% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 20 | 6 | 13 | 39 | 51.3% | 66.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 19 | 3 | 2 | 24 | 79.2% | 91.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 8 | 2 | 1 | 72.7% | 18.2% | 9.1% | 7.7% | 23.1% | 57.1% | 100.0% | 100.0% | 57.1% | 53.8% | 0.077 | 72.7% | 72.7% | 72.7% |
| Wednesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 10.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 77.8% | 63.6% | 70.0% |
| Thursday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 9.1% | 88.9% | 66.7% | 100.0% | 50.0% | 72.7% | 0.455 | 90.9% | 83.3% | 87.0% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 20.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 84.6% | 78.6% | 81.5% |
| Sunday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 9.1% | 18.2% | 100.0% | 50.0% | 100.0% | 60.0% | 63.6% | 0.273 | 77.8% | 77.8% | 77.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | course_portal | 1 |
| Tuesday | calendar | 2 |
| Tuesday | clock | 6 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 2 |
| Thursday | clock | 3 |
| Thursday | shipment_status | 5 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Friday | library_hold | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 5 |
