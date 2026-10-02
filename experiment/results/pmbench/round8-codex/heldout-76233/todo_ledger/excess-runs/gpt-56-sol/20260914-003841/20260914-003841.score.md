# PM-Bench score report

## Summary

Hit: 59 | Late: 2 | Miss: 18 | False alarms: 6 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 44 | check_time calls: 27 | Actions: 67
Exact-set: matches 57 | mismatches 19 | reward 38
Set micro: TP 59 | FP 8 | FN 20
Cross-day: hit 6 | late 1 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 74.7% | late 2.5% | miss 22.8% | false alarm/step 7.9% | commission 0.0% | wrong-content 7.6% | dependency/step 0.0% | overkill/step 5.3% | cross-day miss 0.0% | update miss 11.1% | precision_hit 88.1% | precision_any 91.0% | exact-set match rate 75.0% | exact-set avg reward 0.500 | set_precision 88.1% | set_recall 74.7% | set_f1 80.8%
Hit rates (by modality): event 72.2% | time 80.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:38:41.782Z |
| Finished (UTC) | 2026-09-14T06:50:54.814Z |
| Duration | 12m 13.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 2 |
| Miss | 18 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 44 |
| Check_time calls | 27 |
| Actions | 67 |
| Exact-set matches | 57 |
| Exact-set mismatches | 19 |
| Exact-set reward | 38 |
| Set TP | 59 |
| Set FP | 8 |
| Set FN | 20 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 4 |
| bank_balance | 1 |
| calendar | 1 |
| clock | 27 |
| course_portal | 1 |
| email | 1 |
| laundry_status | 2 |
| price_tracker | 3 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 74.7% |
| Late rate | 2.5% |
| Miss rate | 22.8% |
| False alarm/step | 7.9% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.6% |
| Dependency/step | 0.0% |
| Overkill/step | 5.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 88.1% |
| Precision any | 91.0% |
| Exact-set match rate | 75.0% |
| Exact-set avg reward | 0.500 |
| Set precision | 88.1% |
| Set recall | 74.7% |
| Set F1 | 80.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 54 | 72.2% |
| Time (time + time_check) | 20 | 25 | 80.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 1 | 0 | 40 | 97.5% | 100.0% |
| proactive_monitoring_required | 20 | 1 | 18 | 39 | 51.3% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 20 | 1 | 4 | 25 | 80.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 0.0% | 71.4% | 75.0% | 100.0% | 50.0% | 75.0% | 0.500 | 88.9% | 72.7% | 80.0% |
| Tuesday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 0.0% | 0.0% | 77.8% | 100.0% | 100.0% | 66.7% | 90.0% | 0.800 | 100.0% | 84.6% | 91.7% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 10.0% | 0.0% | 57.1% | 66.7% | 100.0% | 33.3% | 70.0% | 0.400 | 85.7% | 60.0% | 70.6% |
| Thursday | 9 | 0 | 4 | 69.2% | 0.0% | 30.8% | 22.2% | 11.1% | 77.8% | 50.0% | 100.0% | 33.3% | 44.4% | -0.111 | 81.8% | 69.2% | 75.0% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 0.0% | 10.0% | 66.7% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 87.5% | 70.0% | 77.8% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 16.7% | 8.3% | 75.0% | 100.0% | 100.0% | 50.0% | 83.3% | 0.667 | 80.0% | 80.0% | 80.0% |
| Sunday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 7.7% | 75.0% | 100.0% | 85.7% | 80.0% | 84.6% | 0.692 | 90.9% | 83.3% | 87.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | bank_balance | 1 |
| Monday | clock | 4 |
| Tuesday | clock | 5 |
| Tuesday | email | 1 |
| Wednesday | clock | 4 |
| Wednesday | laundry_status | 2 |
| Wednesday | price_tracker | 1 |
| Thursday | appointment_portal | 1 |
| Thursday | clock | 4 |
| Friday | calendar | 1 |
| Friday | clock | 3 |
| Friday | price_tracker | 2 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 3 |
| Saturday | course_portal | 1 |
| Sunday | clock | 4 |
| Sunday | shipment_status | 4 |
