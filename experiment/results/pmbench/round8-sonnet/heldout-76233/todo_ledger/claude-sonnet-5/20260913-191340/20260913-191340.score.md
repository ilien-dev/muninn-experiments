# PM-Bench score report

## Summary

Hit: 52 | Late: 2 | Miss: 25 | False alarms: 2 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 28 | check_time calls: 22 | Actions: 56
Exact-set: matches 52 | mismatches 24 | reward 28
Set micro: TP 52 | FP 4 | FN 27
Cross-day: hit 2 | late 0 | miss 5 | total 7
Updates: hit 5 | late 1 | miss 3 | canceled 2 | total 11 | violations 2
Rates: hit 65.8% | late 2.5% | miss 31.6% | false alarm/step 2.6% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 3.9% | cross-day miss 71.4% | update miss 33.3% | precision_hit 92.9% | precision_any 96.4% | exact-set match rate 68.4% | exact-set avg reward 0.368 | set_precision 92.9% | set_recall 65.8% | set_f1 77.0%
Hit rates (by modality): event 64.8% | time 68.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:13:40.855Z |
| Finished (UTC) | 2026-09-14T01:21:08.306Z |
| Duration | 7m 27.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 52 |
| Late | 2 |
| Miss | 25 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 28 |
| Check_time calls | 22 |
| Actions | 56 |
| Exact-set matches | 52 |
| Exact-set mismatches | 24 |
| Exact-set reward | 28 |
| Set TP | 52 |
| Set FP | 4 |
| Set FN | 27 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 22 |
| email | 2 |
| price_tracker | 2 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 65.8% |
| Late rate | 2.5% |
| Miss rate | 31.6% |
| False alarm/step | 2.6% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 3.9% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 33.3% |
| Precision hit | 92.9% |
| Precision any | 96.4% |
| Exact-set match rate | 68.4% |
| Exact-set avg reward | 0.368 |
| Set precision | 92.9% |
| Set recall | 65.8% |
| Set F1 | 77.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 35 | 54 | 64.8% |
| Time (time + time_check) | 17 | 25 | 68.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 35 | 0 | 5 | 40 | 87.5% | 87.5% |
| proactive_monitoring_required | 17 | 2 | 20 | 39 | 43.6% | 48.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 17 | 2 | 6 | 25 | 68.0% | 76.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 8.3% | 8.3% | 71.4% | 50.0% | 100.0% | 33.3% | 58.3% | 0.167 | 87.5% | 63.6% | 73.7% |
| Tuesday | 8 | 0 | 5 | 61.5% | 0.0% | 38.5% | 0.0% | 0.0% | 55.6% | 75.0% | 71.4% | 50.0% | 60.0% | 0.200 | 100.0% | 61.5% | 76.2% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 0.0% | 0.0% | 57.1% | 66.7% | 100.0% | 33.3% | 70.0% | 0.400 | 100.0% | 60.0% | 75.0% |
| Thursday | 7 | 0 | 6 | 53.8% | 0.0% | 46.2% | 11.1% | 0.0% | 55.6% | 50.0% | 71.4% | 33.3% | 44.4% | -0.111 | 87.5% | 53.8% | 66.7% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 0.0% | 10.0% | 66.7% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 87.5% | 70.0% | 77.8% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 50.0% | 91.7% | 0.833 | 100.0% | 80.0% | 88.9% |
| Sunday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 7.7% | 75.0% | 75.0% | 85.7% | 60.0% | 76.9% | 0.538 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | bank_balance | 1 |
| Monday | clock | 3 |
| Tuesday | clock | 2 |
| Tuesday | email | 1 |
| Wednesday | clock | 2 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 2 |
| Friday | clock | 4 |
| Friday | price_tracker | 1 |
| Saturday | clock | 5 |
| Sunday | clock | 4 |
| Sunday | email | 1 |
| Sunday | shipment_status | 1 |
