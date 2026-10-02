# PM-Bench score report

## Summary

Hit: 61 | Late: 6 | Miss: 14 | False alarms: 5 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 52 | check_time calls: 30 | Actions: 72
Exact-set: matches 53 | mismatches 27 | reward 26
Set micro: TP 61 | FP 11 | FN 20
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 75.3% | late 7.4% | miss 17.3% | false alarm/step 6.2% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 11.2% | cross-day miss 0.0% | update miss 0.0% | precision_hit 84.7% | precision_any 93.1% | exact-set match rate 66.2% | exact-set avg reward 0.325 | set_precision 84.7% | set_recall 75.3% | set_f1 79.7%
Hit rates (by modality): event 73.7% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:28.232Z |
| Finished (UTC) | 2026-09-14T01:15:41.307Z |
| Duration | 14m 13.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 6 |
| Miss | 14 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 52 |
| Check_time calls | 30 |
| Actions | 72 |
| Exact-set matches | 53 |
| Exact-set mismatches | 27 |
| Exact-set reward | 26 |
| Set TP | 61 |
| Set FP | 11 |
| Set FN | 20 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 4 |
| calendar | 2 |
| clock | 30 |
| course_portal | 2 |
| email | 7 |
| library_hold | 2 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 75.3% |
| Late rate | 7.4% |
| Miss rate | 17.3% |
| False alarm/step | 6.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 11.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 84.7% |
| Precision any | 93.1% |
| Exact-set match rate | 66.2% |
| Exact-set avg reward | 0.325 |
| Set precision | 84.7% |
| Set recall | 75.3% |
| Set F1 | 79.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 57 | 73.7% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 42 | 0 | 0 | 42 | 100.0% | 100.0% |
| proactive_monitoring_required | 19 | 6 | 14 | 39 | 48.7% | 64.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 19 | 2 | 3 | 24 | 79.2% | 87.5% |
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
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 9.1% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 8.3% | 8.3% | 75.0% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 81.8% | 75.0% | 78.3% |
| Saturday | 12 | 0 | 2 | 85.7% | 0.0% | 14.3% | 10.0% | 10.0% | 80.0% | 100.0% | 100.0% | 66.7% | 70.0% | 0.400 | 92.3% | 85.7% | 88.9% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 9.1% | 80.0% | 75.0% | 100.0% | 60.0% | 72.7% | 0.455 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | email | 3 |
| Tuesday | calendar | 2 |
| Tuesday | clock | 6 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 2 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 6 |
