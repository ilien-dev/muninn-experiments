# PM-Bench score report

## Summary

Hit: 63 | Late: 3 | Miss: 13 | False alarms: 7 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 67 | check_time calls: 32 | Actions: 73
Exact-set: matches 55 | mismatches 21 | reward 34
Set micro: TP 63 | FP 10 | FN 16
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 79.7% | late 3.8% | miss 16.5% | false alarm/step 9.2% | commission 0.0% | wrong-content 3.8% | dependency/step 0.0% | overkill/step 10.5% | cross-day miss 0.0% | update miss 11.1% | precision_hit 86.3% | precision_any 90.4% | exact-set match rate 72.4% | exact-set avg reward 0.447 | set_precision 86.3% | set_recall 79.7% | set_f1 82.9%
Hit rates (by modality): event 77.8% | time 84.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:34:50.991Z |
| Finished (UTC) | 2026-09-14T06:46:29.519Z |
| Duration | 11m 38.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 63 |
| Late | 3 |
| Miss | 13 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 67 |
| Check_time calls | 32 |
| Actions | 73 |
| Exact-set matches | 55 |
| Exact-set mismatches | 21 |
| Exact-set reward | 34 |
| Set TP | 63 |
| Set FP | 10 |
| Set FN | 16 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 8 |
| bank_balance | 1 |
| calendar | 5 |
| clock | 32 |
| email | 4 |
| laundry_status | 5 |
| library_hold | 3 |
| price_tracker | 5 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.7% |
| Late rate | 3.8% |
| Miss rate | 16.5% |
| False alarm/step | 9.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.8% |
| Dependency/step | 0.0% |
| Overkill/step | 10.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 86.3% |
| Precision any | 90.4% |
| Exact-set match rate | 72.4% |
| Exact-set avg reward | 0.447 |
| Set precision | 86.3% |
| Set recall | 79.7% |
| Set F1 | 82.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 54 | 77.8% |
| Time (time + time_check) | 21 | 25 | 84.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 24 | 3 | 12 | 39 | 61.5% | 69.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 2 | 1 | 4 | 25.0% | 75.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| clock | 21 | 0 | 4 | 25 | 84.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| library_hold | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 8.3% | 71.4% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 88.9% | 72.7% | 80.0% |
| Tuesday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 10.0% | 10.0% | 77.8% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 91.7% | 84.6% | 88.0% |
| Wednesday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 10.0% | 10.0% | 85.7% | 66.7% | 100.0% | 66.7% | 80.0% | 0.600 | 88.9% | 80.0% | 84.2% |
| Thursday | 10 | 1 | 2 | 76.9% | 7.7% | 15.4% | 22.2% | 22.2% | 88.9% | 50.0% | 100.0% | 50.0% | 44.4% | -0.111 | 76.9% | 76.9% | 76.9% |
| Friday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 100.0% | 80.0% | 88.9% |
| Saturday | 7 | 2 | 1 | 70.0% | 20.0% | 10.0% | 8.3% | 16.7% | 62.5% | 100.0% | 83.3% | 50.0% | 66.7% | 0.333 | 70.0% | 70.0% | 70.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 7.7% | 7.7% | 87.5% | 100.0% | 100.0% | 80.0% | 84.6% | 0.692 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 3 |
| Monday | bank_balance | 1 |
| Monday | clock | 4 |
| Tuesday | clock | 5 |
| Tuesday | email | 3 |
| Tuesday | library_hold | 2 |
| Wednesday | calendar | 2 |
| Wednesday | clock | 4 |
| Wednesday | laundry_status | 5 |
| Wednesday | price_tracker | 3 |
| Thursday | appointment_portal | 2 |
| Thursday | clock | 4 |
| Thursday | library_hold | 1 |
| Friday | calendar | 3 |
| Friday | clock | 5 |
| Friday | price_tracker | 2 |
| Saturday | appointment_portal | 3 |
| Saturday | clock | 6 |
| Sunday | clock | 4 |
| Sunday | email | 1 |
| Sunday | shipment_status | 4 |
