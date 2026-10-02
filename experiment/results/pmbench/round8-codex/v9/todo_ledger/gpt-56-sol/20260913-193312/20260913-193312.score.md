# PM-Bench score report

## Summary

Hit: 62 | Late: 6 | Miss: 13 | False alarms: 3 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 48 | check_time calls: 32 | Actions: 71
Exact-set: matches 55 | mismatches 25 | reward 30
Set micro: TP 62 | FP 9 | FN 19
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 76.5% | late 7.4% | miss 16.0% | false alarm/step 3.8% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 8.8% | cross-day miss 0.0% | update miss 11.1% | precision_hit 87.3% | precision_any 95.8% | exact-set match rate 68.8% | exact-set avg reward 0.375 | set_precision 87.3% | set_recall 76.5% | set_f1 81.6%
Hit rates (by modality): event 73.7% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:33:12.051Z |
| Finished (UTC) | 2026-09-14T01:48:01.105Z |
| Duration | 14m 49.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 62 |
| Late | 6 |
| Miss | 13 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 48 |
| Check_time calls | 32 |
| Actions | 71 |
| Exact-set matches | 55 |
| Exact-set mismatches | 25 |
| Exact-set reward | 30 |
| Set TP | 62 |
| Set FP | 9 |
| Set FN | 19 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 3 |
| calendar | 1 |
| clock | 32 |
| course_portal | 1 |
| email | 6 |
| library_hold | 1 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 76.5% |
| Late rate | 7.4% |
| Miss rate | 16.0% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 8.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 87.3% |
| Precision any | 95.8% |
| Exact-set match rate | 68.8% |
| Exact-set avg reward | 0.375 |
| Set precision | 87.3% |
| Set recall | 76.5% |
| Set F1 | 81.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 57 | 73.7% |
| Time (time + time_check) | 20 | 24 | 83.3% |

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
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 20 | 2 | 2 | 24 | 83.3% | 91.7% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 8 | 2 | 1 | 72.7% | 18.2% | 9.1% | 0.0% | 15.4% | 57.1% | 100.0% | 100.0% | 57.1% | 61.5% | 0.231 | 80.0% | 72.7% | 76.2% |
| Wednesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 0.0% | 10.0% | 66.7% | 100.0% | 100.0% | 40.0% | 70.0% | 0.400 | 88.9% | 72.7% | 80.0% |
| Thursday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 9.1% | 88.9% | 66.7% | 100.0% | 50.0% | 72.7% | 0.455 | 90.9% | 83.3% | 87.0% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 20.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 84.6% | 78.6% | 81.5% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 18.2% | 80.0% | 50.0% | 100.0% | 40.0% | 54.5% | 0.091 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | email | 2 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 6 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 2 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 6 |
