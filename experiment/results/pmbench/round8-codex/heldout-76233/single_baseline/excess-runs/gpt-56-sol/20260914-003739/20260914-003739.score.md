# PM-Bench score report

## Summary

Hit: 62 | Late: 3 | Miss: 14 | False alarms: 10 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 69 | check_time calls: 31 | Actions: 75
Exact-set: matches 55 | mismatches 21 | reward 34
Set micro: TP 62 | FP 13 | FN 17
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 3
Rates: hit 78.5% | late 3.8% | miss 17.7% | false alarm/step 13.2% | commission 0.0% | wrong-content 7.6% | dependency/step 0.0% | overkill/step 10.5% | cross-day miss 0.0% | update miss 22.2% | precision_hit 82.7% | precision_any 86.7% | exact-set match rate 72.4% | exact-set avg reward 0.447 | set_precision 82.7% | set_recall 78.5% | set_f1 80.5%
Hit rates (by modality): event 77.8% | time 80.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:37:39.521Z |
| Finished (UTC) | 2026-09-14T06:49:06.666Z |
| Duration | 11m 27.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 62 |
| Late | 3 |
| Miss | 14 |
| False alarms | 10 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 69 |
| Check_time calls | 31 |
| Actions | 75 |
| Exact-set matches | 55 |
| Exact-set mismatches | 21 |
| Exact-set reward | 34 |
| Set TP | 62 |
| Set FP | 13 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 8 |
| bank_balance | 2 |
| calendar | 7 |
| clock | 31 |
| email | 4 |
| laundry_status | 4 |
| library_hold | 4 |
| price_tracker | 4 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 78.5% |
| Late rate | 3.8% |
| Miss rate | 17.7% |
| False alarm/step | 13.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.6% |
| Dependency/step | 0.0% |
| Overkill/step | 10.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 82.7% |
| Precision any | 86.7% |
| Exact-set match rate | 72.4% |
| Exact-set avg reward | 0.447 |
| Set precision | 82.7% |
| Set recall | 78.5% |
| Set F1 | 80.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 54 | 77.8% |
| Time (time + time_check) | 20 | 25 | 80.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 23 | 3 | 13 | 39 | 59.0% | 66.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 2 | 1 | 4 | 25.0% | 75.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 20 | 1 | 4 | 25 | 80.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| library_hold | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 2 | 81.8% | 0.0% | 18.2% | 8.3% | 8.3% | 71.4% | 100.0% | 100.0% | 66.7% | 75.0% | 0.500 | 90.0% | 81.8% | 85.7% |
| Tuesday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 30.0% | 10.0% | 77.8% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 76.9% | 76.9% | 76.9% |
| Wednesday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 20.0% | 10.0% | 71.4% | 66.7% | 100.0% | 50.0% | 70.0% | 0.400 | 77.8% | 70.0% | 73.7% |
| Thursday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 22.2% | 11.1% | 100.0% | 50.0% | 100.0% | 66.7% | 66.7% | 0.333 | 84.6% | 84.6% | 84.6% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 10.0% | 20.0% | 66.7% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 77.8% | 70.0% | 73.7% |
| Saturday | 7 | 2 | 1 | 70.0% | 20.0% | 10.0% | 8.3% | 16.7% | 62.5% | 100.0% | 83.3% | 50.0% | 66.7% | 0.333 | 70.0% | 70.0% | 70.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 87.5% | 100.0% | 100.0% | 80.0% | 92.3% | 0.846 | 100.0% | 91.7% | 95.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 3 |
| Monday | bank_balance | 2 |
| Monday | clock | 5 |
| Tuesday | clock | 4 |
| Tuesday | email | 2 |
| Tuesday | library_hold | 3 |
| Wednesday | calendar | 3 |
| Wednesday | clock | 4 |
| Wednesday | laundry_status | 4 |
| Wednesday | price_tracker | 2 |
| Thursday | appointment_portal | 2 |
| Thursday | clock | 4 |
| Thursday | library_hold | 1 |
| Friday | calendar | 4 |
| Friday | clock | 4 |
| Friday | price_tracker | 2 |
| Saturday | appointment_portal | 3 |
| Saturday | clock | 6 |
| Sunday | clock | 4 |
| Sunday | email | 2 |
| Sunday | shipment_status | 5 |
