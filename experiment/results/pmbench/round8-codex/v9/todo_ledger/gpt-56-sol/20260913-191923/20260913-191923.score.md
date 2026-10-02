# PM-Bench score report

## Summary

Hit: 65 | Late: 7 | Miss: 9 | False alarms: 3 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 48 | check_time calls: 32 | Actions: 75
Exact-set: matches 59 | mismatches 21 | reward 38
Set micro: TP 65 | FP 10 | FN 16
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 80.2% | late 8.6% | miss 11.1% | false alarm/step 3.8% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 8.8% | cross-day miss 0.0% | update miss 0.0% | precision_hit 86.7% | precision_any 96.0% | exact-set match rate 73.8% | exact-set avg reward 0.475 | set_precision 86.7% | set_recall 80.2% | set_f1 83.3%
Hit rates (by modality): event 77.2% | time 87.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:19:23.742Z |
| Finished (UTC) | 2026-09-14T01:33:33.358Z |
| Duration | 14m 9.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 65 |
| Late | 7 |
| Miss | 9 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 48 |
| Check_time calls | 32 |
| Actions | 75 |
| Exact-set matches | 59 |
| Exact-set mismatches | 21 |
| Exact-set reward | 38 |
| Set TP | 65 |
| Set FP | 10 |
| Set FN | 16 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 4 |
| calendar | 2 |
| clock | 32 |
| course_portal | 1 |
| email | 2 |
| library_hold | 2 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 80.2% |
| Late rate | 8.6% |
| Miss rate | 11.1% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 8.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 86.7% |
| Precision any | 96.0% |
| Exact-set match rate | 73.8% |
| Exact-set avg reward | 0.475 |
| Set precision | 86.7% |
| Set recall | 80.2% |
| Set F1 | 83.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 44 | 57 | 77.2% |
| Time (time + time_check) | 21 | 24 | 87.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 23 | 7 | 9 | 39 | 59.0% | 76.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 21 | 3 | 0 | 24 | 87.5% | 100.0% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 7.7% | 77.8% | 100.0% | 100.0% | 66.7% | 76.9% | 0.538 | 90.9% | 83.3% | 87.0% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 15.4% | 15.4% | 57.1% | 100.0% | 100.0% | 57.1% | 61.5% | 0.231 | 72.7% | 72.7% | 72.7% |
| Wednesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 0.0% | 10.0% | 66.7% | 100.0% | 100.0% | 40.0% | 70.0% | 0.400 | 88.9% | 72.7% | 80.0% |
| Thursday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 88.9% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 91.7% | 95.7% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 10 | 2 | 2 | 71.4% | 14.3% | 14.3% | 10.0% | 20.0% | 80.0% | 50.0% | 100.0% | 33.3% | 50.0% | 0.000 | 76.9% | 71.4% | 74.1% |
| Sunday | 8 | 1 | 0 | 88.9% | 11.1% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | library_hold | 1 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 6 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 4 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Friday | library_hold | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 6 |
