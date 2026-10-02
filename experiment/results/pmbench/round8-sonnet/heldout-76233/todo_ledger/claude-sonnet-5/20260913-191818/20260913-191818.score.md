# PM-Bench score report

## Summary

Hit: 52 | Late: 0 | Miss: 27 | False alarms: 3 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 0 | state query calls: 27 | check_time calls: 24 | Actions: 55
Exact-set: matches 56 | mismatches 20 | reward 36
Set micro: TP 52 | FP 3 | FN 27
Cross-day: hit 2 | late 0 | miss 5 | total 7
Updates: hit 5 | late 0 | miss 4 | canceled 2 | total 11 | violations 1
Rates: hit 65.8% | late 0.0% | miss 34.2% | false alarm/step 3.9% | commission 0.0% | wrong-content 3.8% | dependency/step 0.0% | overkill/step 0.0% | cross-day miss 71.4% | update miss 44.4% | precision_hit 94.5% | precision_any 94.5% | exact-set match rate 73.7% | exact-set avg reward 0.474 | set_precision 94.5% | set_recall 65.8% | set_f1 77.6%
Hit rates (by modality): event 63.0% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:18:18.254Z |
| Finished (UTC) | 2026-09-14T01:25:27.569Z |
| Duration | 7m 9.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 52 |
| Late | 0 |
| Miss | 27 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 0 |
| State query calls | 27 |
| Check_time calls | 24 |
| Actions | 55 |
| Exact-set matches | 56 |
| Exact-set mismatches | 20 |
| Exact-set reward | 36 |
| Set TP | 52 |
| Set FP | 3 |
| Set FN | 27 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 24 |
| price_tracker | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 65.8% |
| Late rate | 0.0% |
| Miss rate | 34.2% |
| False alarm/step | 3.9% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.8% |
| Dependency/step | 0.0% |
| Overkill/step | 0.0% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 44.4% |
| Precision hit | 94.5% |
| Precision any | 94.5% |
| Exact-set match rate | 73.7% |
| Exact-set avg reward | 0.474 |
| Set precision | 94.5% |
| Set recall | 65.8% |
| Set F1 | 77.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 34 | 54 | 63.0% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 34 | 0 | 6 | 40 | 85.0% | 85.0% |
| proactive_monitoring_required | 18 | 0 | 21 | 39 | 46.2% | 46.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 18 | 0 | 7 | 25 | 72.0% | 72.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 0.0% | 0.0% | 71.4% | 75.0% | 100.0% | 50.0% | 75.0% | 0.500 | 100.0% | 72.7% | 84.2% |
| Tuesday | 8 | 0 | 5 | 61.5% | 0.0% | 38.5% | 0.0% | 0.0% | 55.6% | 75.0% | 71.4% | 50.0% | 60.0% | 0.200 | 100.0% | 61.5% | 76.2% |
| Wednesday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 0.0% | 0.0% | 57.1% | 66.7% | 100.0% | 33.3% | 70.0% | 0.400 | 100.0% | 60.0% | 75.0% |
| Thursday | 7 | 0 | 6 | 53.8% | 0.0% | 46.2% | 11.1% | 0.0% | 55.6% | 50.0% | 71.4% | 33.3% | 44.4% | -0.111 | 87.5% | 53.8% | 66.7% |
| Friday | 6 | 0 | 4 | 60.0% | 0.0% | 40.0% | 10.0% | 0.0% | 66.7% | 50.0% | 100.0% | 33.3% | 80.0% | 0.600 | 85.7% | 60.0% | 70.6% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 50.0% | 91.7% | 0.833 | 100.0% | 80.0% | 88.9% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 7.7% | 0.0% | 62.5% | 100.0% | 71.4% | 80.0% | 84.6% | 0.692 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | bank_balance | 1 |
| Monday | clock | 3 |
| Tuesday | clock | 3 |
| Wednesday | clock | 3 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 2 |
| Friday | clock | 4 |
| Friday | price_tracker | 1 |
| Saturday | clock | 4 |
| Sunday | clock | 5 |
