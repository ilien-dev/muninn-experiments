# PM-Bench score report

## Summary

Hit: 59 | Late: 0 | Miss: 22 | False alarms: 12 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 55 | check_time calls: 32 | Actions: 71
Exact-set: matches 57 | mismatches 27 | reward 30
Set micro: TP 59 | FP 12 | FN 22
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 72.8% | late 0.0% | miss 27.2% | false alarm/step 14.3% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 8.3% | cross-day miss 0.0% | update miss 11.1% | precision_hit 83.1% | precision_any 83.1% | exact-set match rate 67.9% | exact-set avg reward 0.357 | set_precision 83.1% | set_recall 72.8% | set_f1 77.6%
Hit rates (by modality): event 71.4% | time 76.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T07:15:19.526Z |
| Finished (UTC) | 2026-09-14T07:28:33.636Z |
| Duration | 13m 14.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 0 |
| Miss | 22 |
| False alarms | 12 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 55 |
| Check_time calls | 32 |
| Actions | 71 |
| Exact-set matches | 57 |
| Exact-set mismatches | 27 |
| Exact-set reward | 30 |
| Set TP | 59 |
| Set FP | 12 |
| Set FN | 22 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 1 |
| calendar | 2 |
| clock | 32 |
| course_portal | 4 |
| email | 2 |
| laundry_status | 2 |
| library_hold | 1 |
| price_tracker | 4 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 72.8% |
| Late rate | 0.0% |
| Miss rate | 27.2% |
| False alarm/step | 14.3% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 8.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 83.1% |
| Precision any | 83.1% |
| Exact-set match rate | 67.9% |
| Exact-set avg reward | 0.357 |
| Set precision | 83.1% |
| Set recall | 72.8% |
| Set F1 | 77.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 56 | 71.4% |
| Time (time + time_check) | 19 | 25 | 76.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 21 | 0 | 20 | 41 | 51.2% | 51.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 19 | 0 | 6 | 25 | 76.0% | 76.0% |
| course_portal | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 3 | 4 | 25.0% | 25.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 30.8% | 15.4% | 60.0% | 75.0% | 75.0% | 60.0% | 69.2% | 0.385 | 60.0% | 66.7% | 63.2% |
| Tuesday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 9.1% | 0.0% | 75.0% | 75.0% | 100.0% | 50.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 14.3% | 7.1% | 60.0% | 100.0% | 75.0% | 80.0% | 78.6% | 0.571 | 77.8% | 77.8% | 77.8% |
| Thursday | 11 | 0 | 5 | 68.8% | 0.0% | 31.2% | 10.0% | 10.0% | 76.9% | 33.3% | 100.0% | 16.7% | 40.0% | -0.200 | 91.7% | 68.8% | 78.6% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 25.0% | 16.7% | 87.5% | 33.3% | 100.0% | 50.0% | 66.7% | 0.333 | 72.7% | 72.7% | 72.7% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 100.0% | 57.1% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 8.3% | 8.3% | 66.7% | 100.0% | 100.0% | 50.0% | 66.7% | 0.333 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 6 |
| Monday | email | 2 |
| Tuesday | appointment_portal | 1 |
| Tuesday | clock | 5 |
| Wednesday | appointment_portal | 2 |
| Wednesday | clock | 7 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 2 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 2 |
| Friday | calendar | 2 |
| Friday | clock | 3 |
| Friday | course_portal | 3 |
| Friday | price_tracker | 1 |
| Saturday | clock | 5 |
| Saturday | laundry_status | 1 |
| Saturday | price_tracker | 1 |
| Saturday | shipment_status | 3 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |
| Sunday | course_portal | 1 |
| Sunday | library_hold | 1 |
