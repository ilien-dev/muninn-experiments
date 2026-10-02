# PM-Bench score report

## Summary

Hit: 63 | Late: 8 | Miss: 10 | False alarms: 3 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 60 | check_time calls: 31 | Actions: 74
Exact-set: matches 55 | mismatches 25 | reward 30
Set micro: TP 63 | FP 11 | FN 18
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 77.8% | late 9.9% | miss 12.3% | false alarm/step 3.8% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 11.2% | cross-day miss 0.0% | update miss 0.0% | precision_hit 85.1% | precision_any 95.9% | exact-set match rate 68.8% | exact-set avg reward 0.375 | set_precision 85.1% | set_recall 77.8% | set_f1 81.3%
Hit rates (by modality): event 75.4% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:24:30.916Z |
| Finished (UTC) | 2026-09-14T06:38:40.264Z |
| Duration | 14m 9.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 63 |
| Late | 8 |
| Miss | 10 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 60 |
| Check_time calls | 31 |
| Actions | 74 |
| Exact-set matches | 55 |
| Exact-set mismatches | 25 |
| Exact-set reward | 30 |
| Set TP | 63 |
| Set FP | 11 |
| Set FN | 18 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 4 |
| bank_balance | 5 |
| calendar | 4 |
| clock | 31 |
| course_portal | 2 |
| email | 8 |
| library_hold | 2 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 77.8% |
| Late rate | 9.9% |
| Miss rate | 12.3% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 11.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 85.1% |
| Precision any | 95.9% |
| Exact-set match rate | 68.8% |
| Exact-set avg reward | 0.375 |
| Set precision | 85.1% |
| Set recall | 77.8% |
| Set F1 | 81.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 43 | 57 | 75.4% |
| Time (time + time_check) | 20 | 24 | 83.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 21 | 8 | 10 | 39 | 53.8% | 74.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 1 | 1 | 1 | 3 | 33.3% | 66.7% |
| clock | 20 | 3 | 1 | 24 | 83.3% | 95.8% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 7.7% | 66.7% | 100.0% | 100.0% | 50.0% | 69.2% | 0.385 | 90.0% | 75.0% | 81.8% |
| Tuesday | 8 | 2 | 1 | 72.7% | 18.2% | 9.1% | 7.7% | 23.1% | 57.1% | 100.0% | 100.0% | 57.1% | 53.8% | 0.077 | 72.7% | 72.7% | 72.7% |
| Wednesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 0.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 77.8% | 63.6% | 70.0% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 9.1% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 13 | 0 | 1 | 92.9% | 0.0% | 7.1% | 10.0% | 10.0% | 90.0% | 100.0% | 100.0% | 83.3% | 80.0% | 0.600 | 92.9% | 92.9% | 92.9% |
| Sunday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 0.0% | 9.1% | 80.0% | 75.0% | 100.0% | 60.0% | 72.7% | 0.455 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 4 |
| Monday | email | 3 |
| Tuesday | calendar | 3 |
| Tuesday | clock | 6 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 3 |
| Thursday | shipment_status | 4 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | calendar | 1 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 3 |
| Sunday | clock | 6 |
