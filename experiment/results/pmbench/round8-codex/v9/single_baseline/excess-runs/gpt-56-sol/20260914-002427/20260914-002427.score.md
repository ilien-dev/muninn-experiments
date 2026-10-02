# PM-Bench score report

## Summary

Hit: 65 | Late: 3 | Miss: 13 | False alarms: 7 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 53 | check_time calls: 28 | Actions: 75
Exact-set: matches 58 | mismatches 22 | reward 36
Set micro: TP 65 | FP 10 | FN 16
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 80.2% | late 3.7% | miss 16.0% | false alarm/step 8.8% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 8.8% | cross-day miss 0.0% | update miss 11.1% | precision_hit 86.7% | precision_any 90.7% | exact-set match rate 72.5% | exact-set avg reward 0.450 | set_precision 86.7% | set_recall 80.2% | set_f1 83.3%
Hit rates (by modality): event 78.9% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:24:27.019Z |
| Finished (UTC) | 2026-09-14T06:34:49.490Z |
| Duration | 10m 22.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 65 |
| Late | 3 |
| Miss | 13 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 53 |
| Check_time calls | 28 |
| Actions | 75 |
| Exact-set matches | 58 |
| Exact-set mismatches | 22 |
| Exact-set reward | 36 |
| Set TP | 65 |
| Set FP | 10 |
| Set FN | 16 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 4 |
| calendar | 4 |
| clock | 28 |
| course_portal | 2 |
| email | 7 |
| library_hold | 2 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 80.2% |
| Late rate | 3.7% |
| Miss rate | 16.0% |
| False alarm/step | 8.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 8.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 86.7% |
| Precision any | 90.7% |
| Exact-set match rate | 72.5% |
| Exact-set avg reward | 0.450 |
| Set precision | 86.7% |
| Set recall | 80.2% |
| Set F1 | 83.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 45 | 57 | 78.9% |
| Time (time + time_check) | 20 | 24 | 83.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 23 | 3 | 13 | 39 | 59.0% | 66.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 20 | 1 | 3 | 24 | 83.3% | 87.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 7.7% | 15.4% | 71.4% | 100.0% | 100.0% | 71.4% | 69.2% | 0.385 | 81.8% | 81.8% | 81.8% |
| Wednesday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 20.0% | 10.0% | 77.8% | 50.0% | 100.0% | 40.0% | 60.0% | 0.200 | 80.0% | 72.7% | 76.2% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 9.1% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 30.0% | 20.0% | 80.0% | 75.0% | 100.0% | 50.0% | 50.0% | 0.000 | 78.6% | 78.6% | 78.6% |
| Sunday | 9 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | email | 2 |
| Tuesday | calendar | 2 |
| Tuesday | clock | 6 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 3 |
| Thursday | shipment_status | 4 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 5 |
