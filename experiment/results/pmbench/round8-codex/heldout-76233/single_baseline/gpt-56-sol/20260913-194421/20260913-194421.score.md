# PM-Bench score report

## Summary

Hit: 60 | Late: 1 | Miss: 18 | False alarms: 13 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 52 | check_time calls: 26 | Actions: 74
Exact-set: matches 53 | mismatches 23 | reward 30
Set micro: TP 60 | FP 14 | FN 19
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 3
Rates: hit 75.9% | late 1.3% | miss 22.8% | false alarm/step 17.1% | commission 0.0% | wrong-content 7.6% | dependency/step 0.0% | overkill/step 11.8% | cross-day miss 0.0% | update miss 11.1% | precision_hit 81.1% | precision_any 82.4% | exact-set match rate 69.7% | exact-set avg reward 0.395 | set_precision 81.1% | set_recall 75.9% | set_f1 78.4%
Hit rates (by modality): event 74.1% | time 80.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:44:21.001Z |
| Finished (UTC) | 2026-09-14T01:56:22.890Z |
| Duration | 12m 1.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 60 |
| Late | 1 |
| Miss | 18 |
| False alarms | 13 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 52 |
| Check_time calls | 26 |
| Actions | 74 |
| Exact-set matches | 53 |
| Exact-set mismatches | 23 |
| Exact-set reward | 30 |
| Set TP | 60 |
| Set FP | 14 |
| Set FN | 19 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 5 |
| bank_balance | 2 |
| calendar | 4 |
| clock | 26 |
| email | 2 |
| laundry_status | 4 |
| library_hold | 1 |
| price_tracker | 3 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 75.9% |
| Late rate | 1.3% |
| Miss rate | 22.8% |
| False alarm/step | 17.1% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.6% |
| Dependency/step | 0.0% |
| Overkill/step | 11.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 81.1% |
| Precision any | 82.4% |
| Exact-set match rate | 69.7% |
| Exact-set avg reward | 0.395 |
| Set precision | 81.1% |
| Set recall | 75.9% |
| Set F1 | 78.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 54 | 74.1% |
| Time (time + time_check) | 20 | 25 | 80.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 21 | 1 | 17 | 39 | 53.8% | 56.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| clock | 20 | 1 | 4 | 25 | 80.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 16.7% | 8.3% | 71.4% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 80.0% | 72.7% | 76.2% |
| Tuesday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 20.0% | 10.0% | 77.8% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 84.6% | 84.6% | 84.6% |
| Wednesday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 10.0% | 0.0% | 71.4% | 66.7% | 100.0% | 50.0% | 80.0% | 0.600 | 87.5% | 70.0% | 77.8% |
| Thursday | 9 | 0 | 4 | 69.2% | 0.0% | 30.8% | 33.3% | 22.2% | 77.8% | 50.0% | 100.0% | 33.3% | 44.4% | -0.111 | 75.0% | 69.2% | 72.0% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 10.0% | 20.0% | 66.7% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 77.8% | 70.0% | 73.7% |
| Saturday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 25.0% | 16.7% | 62.5% | 100.0% | 83.3% | 50.0% | 66.7% | 0.333 | 70.0% | 70.0% | 70.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 7.7% | 7.7% | 87.5% | 100.0% | 100.0% | 80.0% | 84.6% | 0.692 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | bank_balance | 2 |
| Monday | clock | 3 |
| Tuesday | clock | 4 |
| Tuesday | email | 2 |
| Tuesday | library_hold | 1 |
| Wednesday | calendar | 1 |
| Wednesday | clock | 3 |
| Wednesday | laundry_status | 4 |
| Wednesday | price_tracker | 2 |
| Thursday | appointment_portal | 1 |
| Thursday | clock | 3 |
| Friday | calendar | 3 |
| Friday | clock | 4 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 5 |
| Sunday | clock | 4 |
| Sunday | shipment_status | 5 |
