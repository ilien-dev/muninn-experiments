# PM-Bench score report

## Summary

Hit: 64 | Late: 8 | Miss: 9 | False alarms: 7 | Commission: 0 | Wrong-content: 10 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 61 | check_time calls: 33 | Actions: 79
Exact-set: matches 52 | mismatches 28 | reward 24
Set micro: TP 64 | FP 15 | FN 17
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 79.0% | late 9.9% | miss 11.1% | false alarm/step 8.8% | commission 0.0% | wrong-content 12.3% | dependency/step 0.0% | overkill/step 15.0% | cross-day miss 0.0% | update miss 0.0% | precision_hit 81.0% | precision_any 91.1% | exact-set match rate 65.0% | exact-set avg reward 0.300 | set_precision 81.0% | set_recall 79.0% | set_f1 80.0%
Hit rates (by modality): event 77.2% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:18:17.624Z |
| Finished (UTC) | 2026-09-14T01:30:41.657Z |
| Duration | 12m 24.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 64 |
| Late | 8 |
| Miss | 9 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 10 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 61 |
| Check_time calls | 33 |
| Actions | 79 |
| Exact-set matches | 52 |
| Exact-set mismatches | 28 |
| Exact-set reward | 24 |
| Set TP | 64 |
| Set FP | 15 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 4 |
| calendar | 5 |
| clock | 33 |
| course_portal | 2 |
| email | 6 |
| library_hold | 3 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.0% |
| Late rate | 9.9% |
| Miss rate | 11.1% |
| False alarm/step | 8.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 12.3% |
| Dependency/step | 0.0% |
| Overkill/step | 15.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 81.0% |
| Precision any | 91.1% |
| Exact-set match rate | 65.0% |
| Exact-set avg reward | 0.300 |
| Set precision | 81.0% |
| Set recall | 79.0% |
| Set F1 | 80.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 44 | 57 | 77.2% |
| Time (time + time_check) | 20 | 24 | 83.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 22 | 8 | 9 | 39 | 56.4% | 76.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 20 | 3 | 1 | 24 | 83.3% | 95.8% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 1 | 2 | 0 | 3 | 33.3% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 15.4% | 15.4% | 66.7% | 100.0% | 100.0% | 50.0% | 61.5% | 0.231 | 75.0% | 75.0% | 75.0% |
| Tuesday | 8 | 2 | 1 | 72.7% | 18.2% | 9.1% | 7.7% | 23.1% | 57.1% | 100.0% | 100.0% | 57.1% | 53.8% | 0.077 | 72.7% | 72.7% | 72.7% |
| Wednesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 10.0% | 10.0% | 77.8% | 50.0% | 100.0% | 40.0% | 60.0% | 0.200 | 80.0% | 72.7% | 76.2% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 9.1% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 10 | 2 | 0 | 83.3% | 16.7% | 0.0% | 0.0% | 8.3% | 75.0% | 100.0% | 100.0% | 66.7% | 75.0% | 0.500 | 83.3% | 83.3% | 83.3% |
| Saturday | 12 | 0 | 2 | 85.7% | 0.0% | 14.3% | 20.0% | 20.0% | 80.0% | 100.0% | 100.0% | 66.7% | 60.0% | 0.200 | 85.7% | 85.7% | 85.7% |
| Sunday | 8 | 1 | 0 | 88.9% | 11.1% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 5 |
| Monday | email | 1 |
| Monday | library_hold | 1 |
| Tuesday | calendar | 3 |
| Tuesday | clock | 6 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 3 |
| Thursday | shipment_status | 5 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 7 |
