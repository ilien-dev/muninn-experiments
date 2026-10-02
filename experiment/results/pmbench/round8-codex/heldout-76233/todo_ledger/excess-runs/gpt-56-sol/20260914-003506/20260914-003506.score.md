# PM-Bench score report

## Summary

Hit: 61 | Late: 0 | Miss: 18 | False alarms: 7 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 44 | check_time calls: 29 | Actions: 68
Exact-set: matches 58 | mismatches 18 | reward 40
Set micro: TP 61 | FP 7 | FN 18
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 77.2% | late 0.0% | miss 22.8% | false alarm/step 9.2% | commission 0.0% | wrong-content 3.8% | dependency/step 0.0% | overkill/step 3.9% | cross-day miss 0.0% | update miss 11.1% | precision_hit 89.7% | precision_any 89.7% | exact-set match rate 76.3% | exact-set avg reward 0.526 | set_precision 89.7% | set_recall 77.2% | set_f1 83.0%
Hit rates (by modality): event 74.1% | time 84.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:35:06.932Z |
| Finished (UTC) | 2026-09-14T06:47:41.297Z |
| Duration | 12m 34.4s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 0 |
| Miss | 18 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 44 |
| Check_time calls | 29 |
| Actions | 68 |
| Exact-set matches | 58 |
| Exact-set mismatches | 18 |
| Exact-set reward | 40 |
| Set TP | 61 |
| Set FP | 7 |
| Set FN | 18 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 4 |
| bank_balance | 1 |
| calendar | 2 |
| clock | 29 |
| course_portal | 1 |
| email | 1 |
| laundry_status | 2 |
| price_tracker | 2 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 77.2% |
| Late rate | 0.0% |
| Miss rate | 22.8% |
| False alarm/step | 9.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.8% |
| Dependency/step | 0.0% |
| Overkill/step | 3.9% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 89.7% |
| Precision any | 89.7% |
| Exact-set match rate | 76.3% |
| Exact-set avg reward | 0.526 |
| Set precision | 89.7% |
| Set recall | 77.2% |
| Set F1 | 83.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 54 | 74.1% |
| Time (time + time_check) | 21 | 25 | 84.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 40 | 0 | 0 | 40 | 100.0% | 100.0% |
| proactive_monitoring_required | 21 | 0 | 18 | 39 | 53.8% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 21 | 0 | 4 | 25 | 84.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 16.7% | 8.3% | 71.4% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 80.0% | 72.7% | 76.2% |
| Tuesday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 0.0% | 0.0% | 77.8% | 100.0% | 100.0% | 66.7% | 90.0% | 0.800 | 100.0% | 84.6% | 91.7% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 10.0% | 0.0% | 57.1% | 66.7% | 100.0% | 33.3% | 70.0% | 0.400 | 85.7% | 60.0% | 70.6% |
| Thursday | 9 | 0 | 4 | 69.2% | 0.0% | 30.8% | 22.2% | 11.1% | 77.8% | 50.0% | 100.0% | 33.3% | 44.4% | -0.111 | 81.8% | 69.2% | 75.0% |
| Friday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 100.0% | 80.0% | 88.9% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 16.7% | 8.3% | 75.0% | 100.0% | 100.0% | 50.0% | 83.3% | 0.667 | 80.0% | 80.0% | 80.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 87.5% | 100.0% | 100.0% | 80.0% | 92.3% | 0.846 | 100.0% | 91.7% | 95.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | bank_balance | 1 |
| Monday | clock | 4 |
| Tuesday | clock | 4 |
| Tuesday | email | 1 |
| Wednesday | calendar | 1 |
| Wednesday | clock | 3 |
| Wednesday | laundry_status | 2 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 4 |
| Friday | calendar | 1 |
| Friday | clock | 5 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 5 |
| Saturday | course_portal | 1 |
| Sunday | clock | 4 |
| Sunday | shipment_status | 2 |
