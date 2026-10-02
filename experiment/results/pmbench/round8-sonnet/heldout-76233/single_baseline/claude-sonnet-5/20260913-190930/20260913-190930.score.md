# PM-Bench score report

## Summary

Hit: 59 | Late: 0 | Miss: 20 | False alarms: 2 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 0 | state query calls: 35 | check_time calls: 27 | Actions: 61
Exact-set: matches 60 | mismatches 16 | reward 44
Set micro: TP 59 | FP 2 | FN 20
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 2
Rates: hit 74.7% | late 0.0% | miss 25.3% | false alarm/step 2.6% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 0.0% | cross-day miss 14.3% | update miss 33.3% | precision_hit 96.7% | precision_any 96.7% | exact-set match rate 78.9% | exact-set avg reward 0.579 | set_precision 96.7% | set_recall 74.7% | set_f1 84.3%
Hit rates (by modality): event 72.2% | time 80.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:09:30.946Z |
| Finished (UTC) | 2026-09-14T01:15:59.378Z |
| Duration | 6m 28.4s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 0 |
| Miss | 20 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 0 |
| State query calls | 35 |
| Check_time calls | 27 |
| Actions | 61 |
| Exact-set matches | 60 |
| Exact-set mismatches | 16 |
| Exact-set reward | 44 |
| Set TP | 59 |
| Set FP | 2 |
| Set FN | 20 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 1 |
| clock | 27 |
| email | 2 |
| laundry_status | 1 |
| price_tracker | 2 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 74.7% |
| Late rate | 0.0% |
| Miss rate | 25.3% |
| False alarm/step | 2.6% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 0.0% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 96.7% |
| Precision any | 96.7% |
| Exact-set match rate | 78.9% |
| Exact-set avg reward | 0.579 |
| Set precision | 96.7% |
| Set recall | 74.7% |
| Set F1 | 84.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 54 | 72.2% |
| Time (time + time_check) | 20 | 25 | 80.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 20 | 0 | 19 | 39 | 51.3% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 20 | 0 | 5 | 25 | 80.0% | 80.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 0.0% | 0.0% | 71.4% | 75.0% | 100.0% | 50.0% | 75.0% | 0.500 | 100.0% | 72.7% | 84.2% |
| Tuesday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 0.0% | 0.0% | 77.8% | 75.0% | 100.0% | 50.0% | 80.0% | 0.600 | 100.0% | 76.9% | 87.0% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 10.0% | 0.0% | 57.1% | 66.7% | 100.0% | 33.3% | 70.0% | 0.400 | 85.7% | 60.0% | 70.6% |
| Thursday | 9 | 0 | 4 | 69.2% | 0.0% | 30.8% | 0.0% | 0.0% | 66.7% | 75.0% | 85.7% | 50.0% | 55.6% | 0.111 | 100.0% | 69.2% | 81.8% |
| Friday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 0.0% | 0.0% | 66.7% | 75.0% | 100.0% | 50.0% | 80.0% | 0.600 | 100.0% | 70.0% | 82.4% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 50.0% | 91.7% | 0.833 | 100.0% | 80.0% | 88.9% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 7.7% | 0.0% | 87.5% | 100.0% | 100.0% | 80.0% | 92.3% | 0.846 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | bank_balance | 1 |
| Monday | clock | 3 |
| Tuesday | clock | 2 |
| Tuesday | email | 1 |
| Wednesday | clock | 3 |
| Wednesday | laundry_status | 1 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 4 |
| Friday | clock | 4 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | clock | 6 |
| Sunday | clock | 5 |
| Sunday | email | 1 |
| Sunday | shipment_status | 1 |
