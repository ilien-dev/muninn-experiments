# PM-Bench score report

## Summary

Hit: 60 | Late: 4 | Miss: 15 | False alarms: 9 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 47 | check_time calls: 25 | Actions: 73
Exact-set: matches 52 | mismatches 24 | reward 28
Set micro: TP 60 | FP 13 | FN 19
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 75.9% | late 5.1% | miss 19.0% | false alarm/step 11.8% | commission 0.0% | wrong-content 7.6% | dependency/step 0.0% | overkill/step 11.8% | cross-day miss 0.0% | update miss 22.2% | precision_hit 82.2% | precision_any 87.7% | exact-set match rate 68.4% | exact-set avg reward 0.368 | set_precision 82.2% | set_recall 75.9% | set_f1 78.9%
Hit rates (by modality): event 74.1% | time 80.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:12:05.591Z |
| Finished (UTC) | 2026-09-14T02:23:42.688Z |
| Duration | 11m 37.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 60 |
| Late | 4 |
| Miss | 15 |
| False alarms | 9 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 47 |
| Check_time calls | 25 |
| Actions | 73 |
| Exact-set matches | 52 |
| Exact-set mismatches | 24 |
| Exact-set reward | 28 |
| Set TP | 60 |
| Set FP | 13 |
| Set FN | 19 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 7 |
| bank_balance | 1 |
| calendar | 4 |
| clock | 25 |
| email | 3 |
| laundry_status | 1 |
| library_hold | 1 |
| price_tracker | 3 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 75.9% |
| Late rate | 5.1% |
| Miss rate | 19.0% |
| False alarm/step | 11.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.6% |
| Dependency/step | 0.0% |
| Overkill/step | 11.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 82.2% |
| Precision any | 87.7% |
| Exact-set match rate | 68.4% |
| Exact-set avg reward | 0.368 |
| Set precision | 82.2% |
| Set recall | 75.9% |
| Set F1 | 78.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 54 | 74.1% |
| Time (time + time_check) | 20 | 25 | 80.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 21 | 4 | 14 | 39 | 53.8% | 64.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 2 | 1 | 4 | 25.0% | 75.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 20 | 1 | 4 | 25 | 80.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 2 | 81.8% | 0.0% | 18.2% | 16.7% | 16.7% | 71.4% | 100.0% | 100.0% | 66.7% | 66.7% | 0.333 | 81.8% | 81.8% | 81.8% |
| Tuesday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 10.0% | 10.0% | 77.8% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 90.9% | 76.9% | 83.3% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 20.0% | 10.0% | 57.1% | 66.7% | 100.0% | 33.3% | 60.0% | 0.200 | 75.0% | 60.0% | 66.7% |
| Thursday | 10 | 1 | 2 | 76.9% | 7.7% | 15.4% | 22.2% | 22.2% | 88.9% | 50.0% | 100.0% | 50.0% | 44.4% | -0.111 | 76.9% | 76.9% | 76.9% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 10.0% | 10.0% | 66.7% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 77.8% | 70.0% | 73.7% |
| Saturday | 7 | 2 | 1 | 70.0% | 20.0% | 10.0% | 8.3% | 16.7% | 62.5% | 100.0% | 83.3% | 50.0% | 66.7% | 0.333 | 70.0% | 70.0% | 70.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 87.5% | 100.0% | 100.0% | 80.0% | 92.3% | 0.846 | 100.0% | 91.7% | 95.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 3 |
| Monday | bank_balance | 1 |
| Monday | clock | 4 |
| Tuesday | clock | 4 |
| Tuesday | email | 1 |
| Wednesday | calendar | 2 |
| Wednesday | clock | 3 |
| Wednesday | laundry_status | 1 |
| Wednesday | price_tracker | 1 |
| Thursday | appointment_portal | 2 |
| Thursday | clock | 3 |
| Thursday | library_hold | 1 |
| Friday | calendar | 2 |
| Friday | clock | 3 |
| Friday | price_tracker | 2 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 4 |
| Sunday | clock | 4 |
| Sunday | email | 2 |
| Sunday | shipment_status | 2 |
