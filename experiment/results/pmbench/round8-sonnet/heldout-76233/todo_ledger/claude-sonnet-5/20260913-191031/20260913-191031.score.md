# PM-Bench score report

## Summary

Hit: 55 | Late: 0 | Miss: 24 | False alarms: 0 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 0 | state query calls: 26 | check_time calls: 21 | Actions: 55
Exact-set: matches 56 | mismatches 20 | reward 36
Set micro: TP 55 | FP 0 | FN 24
Cross-day: hit 4 | late 0 | miss 3 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 0
Rates: hit 69.6% | late 0.0% | miss 30.4% | false alarm/step 0.0% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 0.0% | cross-day miss 42.9% | update miss 33.3% | precision_hit 100.0% | precision_any 100.0% | exact-set match rate 73.7% | exact-set avg reward 0.474 | set_precision 100.0% | set_recall 69.6% | set_f1 82.1%
Hit rates (by modality): event 68.5% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:10:31.849Z |
| Finished (UTC) | 2026-09-14T01:18:16.742Z |
| Duration | 7m 44.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 0 |
| Miss | 24 |
| False alarms | 0 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 0 |
| State query calls | 26 |
| Check_time calls | 21 |
| Actions | 55 |
| Exact-set matches | 56 |
| Exact-set mismatches | 20 |
| Exact-set reward | 36 |
| Set TP | 55 |
| Set FP | 0 |
| Set FN | 24 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 21 |
| email | 1 |
| price_tracker | 2 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.6% |
| Late rate | 0.0% |
| Miss rate | 30.4% |
| False alarm/step | 0.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 0.0% |
| Cross-day miss rate | 42.9% |
| Update miss rate | 33.3% |
| Precision hit | 100.0% |
| Precision any | 100.0% |
| Exact-set match rate | 73.7% |
| Exact-set avg reward | 0.474 |
| Set precision | 100.0% |
| Set recall | 69.6% |
| Set F1 | 82.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 37 | 54 | 68.5% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 37 | 0 | 3 | 40 | 92.5% | 92.5% |
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
| Thursday | 8 | 0 | 5 | 61.5% | 0.0% | 38.5% | 0.0% | 0.0% | 66.7% | 50.0% | 85.7% | 33.3% | 44.4% | -0.111 | 100.0% | 61.5% | 76.2% |
| Friday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 0.0% | 0.0% | 66.7% | 75.0% | 100.0% | 50.0% | 80.0% | 0.600 | 100.0% | 70.0% | 82.4% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 50.0% | 91.7% | 0.833 | 100.0% | 80.0% | 88.9% |
| Sunday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 87.5% | 75.0% | 100.0% | 60.0% | 84.6% | 0.692 | 100.0% | 83.3% | 90.9% |

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
| Saturday | clock | 4 |
| Sunday | clock | 4 |
| Sunday | shipment_status | 1 |
