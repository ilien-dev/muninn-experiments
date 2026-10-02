# PM-Bench score report

## Summary

Hit: 61 | Late: 1 | Miss: 17 | False alarms: 6 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 48 | check_time calls: 29 | Actions: 68
Exact-set: matches 58 | mismatches 18 | reward 40
Set micro: TP 61 | FP 7 | FN 18
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 77.2% | late 1.3% | miss 21.5% | false alarm/step 7.9% | commission 0.0% | wrong-content 5.1% | dependency/step 0.0% | overkill/step 5.3% | cross-day miss 0.0% | update miss 11.1% | precision_hit 89.7% | precision_any 91.2% | exact-set match rate 76.3% | exact-set avg reward 0.526 | set_precision 89.7% | set_recall 77.2% | set_f1 83.0%
Hit rates (by modality): event 74.1% | time 84.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:47:14.237Z |
| Finished (UTC) | 2026-09-14T02:03:01.931Z |
| Duration | 15m 47.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 1 |
| Miss | 17 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 48 |
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
| bank_balance | 2 |
| calendar | 3 |
| clock | 29 |
| course_portal | 1 |
| email | 2 |
| laundry_status | 2 |
| price_tracker | 2 |
| shipment_status | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 77.2% |
| Late rate | 1.3% |
| Miss rate | 21.5% |
| False alarm/step | 7.9% |
| Commission rate | 0.0% |
| Wrong-content rate | 5.1% |
| Dependency/step | 0.0% |
| Overkill/step | 5.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 89.7% |
| Precision any | 91.2% |
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
| proactive_monitoring_required | 21 | 1 | 17 | 39 | 53.8% | 56.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 21 | 1 | 3 | 25 | 84.0% | 88.0% |
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
| Thursday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 11.1% | 11.1% | 77.8% | 75.0% | 100.0% | 50.0% | 55.6% | 0.111 | 90.9% | 76.9% | 83.3% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 0.0% | 10.0% | 66.7% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 87.5% | 70.0% | 77.8% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 16.7% | 8.3% | 75.0% | 100.0% | 100.0% | 50.0% | 83.3% | 0.667 | 80.0% | 80.0% | 80.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 87.5% | 100.0% | 100.0% | 80.0% | 92.3% | 0.846 | 100.0% | 91.7% | 95.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | bank_balance | 2 |
| Monday | clock | 3 |
| Tuesday | clock | 5 |
| Tuesday | email | 1 |
| Wednesday | calendar | 1 |
| Wednesday | clock | 3 |
| Wednesday | laundry_status | 2 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 5 |
| Friday | calendar | 2 |
| Friday | clock | 5 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 4 |
| Saturday | course_portal | 1 |
| Sunday | clock | 4 |
| Sunday | email | 1 |
| Sunday | shipment_status | 3 |
