# PM-Bench score report

## Summary

Hit: 64 | Late: 5 | Miss: 12 | False alarms: 7 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 55 | check_time calls: 28 | Actions: 76
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 64 | FP 12 | FN 17
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 79.0% | late 6.2% | miss 14.8% | false alarm/step 8.8% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 11.2% | cross-day miss 0.0% | update miss 11.1% | precision_hit 84.2% | precision_any 90.8% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 84.2% | set_recall 79.0% | set_f1 81.5%
Hit rates (by modality): event 77.2% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:24:29.614Z |
| Finished (UTC) | 2026-09-14T06:35:05.421Z |
| Duration | 10m 35.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 64 |
| Late | 5 |
| Miss | 12 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 55 |
| Check_time calls | 28 |
| Actions | 76 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 64 |
| Set FP | 12 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 4 |
| calendar | 5 |
| clock | 28 |
| course_portal | 2 |
| email | 6 |
| library_hold | 2 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.0% |
| Late rate | 6.2% |
| Miss rate | 14.8% |
| False alarm/step | 8.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 11.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 84.2% |
| Precision any | 90.8% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 84.2% |
| Set recall | 79.0% |
| Set F1 | 81.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 44 | 57 | 77.2% |
| Time (time + time_check) | 20 | 24 | 83.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 41 | 0 | 1 | 42 | 97.6% | 97.6% |
| proactive_monitoring_required | 23 | 5 | 11 | 39 | 59.0% | 71.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 1 | 1 | 3 | 33.3% | 66.7% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 20 | 1 | 3 | 24 | 83.3% | 87.5% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 7.7% | 7.7% | 66.7% | 100.0% | 100.0% | 50.0% | 69.2% | 0.385 | 81.8% | 75.0% | 78.3% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 7.7% | 15.4% | 71.4% | 100.0% | 100.0% | 71.4% | 69.2% | 0.385 | 81.8% | 81.8% | 81.8% |
| Wednesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 0.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 77.8% | 63.6% | 70.0% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 77.8% | 66.7% | 87.5% | 50.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 8.3% | 8.3% | 75.0% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 81.8% | 75.0% | 78.3% |
| Saturday | 12 | 0 | 2 | 85.7% | 0.0% | 14.3% | 20.0% | 20.0% | 90.0% | 75.0% | 100.0% | 66.7% | 60.0% | 0.200 | 85.7% | 85.7% | 85.7% |
| Sunday | 9 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 4 |
| Monday | email | 2 |
| Tuesday | calendar | 3 |
| Tuesday | clock | 5 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 3 |
| Thursday | shipment_status | 5 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 5 |
