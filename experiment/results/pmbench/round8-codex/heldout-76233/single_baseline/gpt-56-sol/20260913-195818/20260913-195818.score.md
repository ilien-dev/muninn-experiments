# PM-Bench score report

## Summary

Hit: 63 | Late: 2 | Miss: 14 | False alarms: 9 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 68 | check_time calls: 34 | Actions: 74
Exact-set: matches 55 | mismatches 21 | reward 34
Set micro: TP 63 | FP 11 | FN 16
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 79.7% | late 2.5% | miss 17.7% | false alarm/step 11.8% | commission 0.0% | wrong-content 6.3% | dependency/step 0.0% | overkill/step 10.5% | cross-day miss 0.0% | update miss 11.1% | precision_hit 85.1% | precision_any 87.8% | exact-set match rate 72.4% | exact-set avg reward 0.447 | set_precision 85.1% | set_recall 79.7% | set_f1 82.4%
Hit rates (by modality): event 75.9% | time 88.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:58:18.793Z |
| Finished (UTC) | 2026-09-14T02:12:04.088Z |
| Duration | 13m 45.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 63 |
| Late | 2 |
| Miss | 14 |
| False alarms | 9 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 68 |
| Check_time calls | 34 |
| Actions | 74 |
| Exact-set matches | 55 |
| Exact-set mismatches | 21 |
| Exact-set reward | 34 |
| Set TP | 63 |
| Set FP | 11 |
| Set FN | 16 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 7 |
| bank_balance | 2 |
| calendar | 6 |
| clock | 34 |
| email | 2 |
| laundry_status | 4 |
| library_hold | 3 |
| price_tracker | 5 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.7% |
| Late rate | 2.5% |
| Miss rate | 17.7% |
| False alarm/step | 11.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.3% |
| Dependency/step | 0.0% |
| Overkill/step | 10.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 85.1% |
| Precision any | 87.8% |
| Exact-set match rate | 72.4% |
| Exact-set avg reward | 0.447 |
| Set precision | 85.1% |
| Set recall | 79.7% |
| Set F1 | 82.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 54 | 75.9% |
| Time (time + time_check) | 22 | 25 | 88.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 25 | 2 | 12 | 39 | 64.1% | 69.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 3 | 4 | 25.0% | 25.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| clock | 22 | 0 | 3 | 25 | 88.0% | 88.0% |
| email | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 1 | 1 | 0 | 2 | 50.0% | 100.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 25.0% | 25.0% | 57.1% | 75.0% | 80.0% | 50.0% | 41.7% | -0.167 | 70.0% | 63.6% | 66.7% |
| Tuesday | 11 | 2 | 0 | 84.6% | 15.4% | 0.0% | 0.0% | 10.0% | 77.8% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 84.6% | 84.6% | 84.6% |
| Wednesday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 0.0% | 0.0% | 71.4% | 66.7% | 100.0% | 50.0% | 80.0% | 0.600 | 100.0% | 70.0% | 82.4% |
| Thursday | 12 | 0 | 1 | 92.3% | 0.0% | 7.7% | 11.1% | 11.1% | 100.0% | 75.0% | 100.0% | 83.3% | 77.8% | 0.556 | 92.3% | 92.3% | 92.3% |
| Friday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 10.0% | 0.0% | 66.7% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 88.9% | 80.0% | 84.2% |
| Saturday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 25.0% | 16.7% | 62.5% | 100.0% | 83.3% | 50.0% | 66.7% | 0.333 | 70.0% | 70.0% | 70.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 7.7% | 7.7% | 87.5% | 100.0% | 100.0% | 80.0% | 84.6% | 0.692 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 3 |
| Monday | bank_balance | 2 |
| Monday | clock | 5 |
| Tuesday | clock | 5 |
| Tuesday | email | 2 |
| Tuesday | library_hold | 1 |
| Wednesday | calendar | 3 |
| Wednesday | clock | 4 |
| Wednesday | laundry_status | 4 |
| Wednesday | price_tracker | 3 |
| Thursday | appointment_portal | 2 |
| Thursday | clock | 4 |
| Thursday | library_hold | 2 |
| Friday | calendar | 3 |
| Friday | clock | 5 |
| Friday | price_tracker | 2 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 6 |
| Sunday | clock | 5 |
| Sunday | shipment_status | 5 |
