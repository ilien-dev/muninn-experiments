# PM-Bench score report

## Summary

Hit: 50 | Late: 0 | Miss: 31 | False alarms: 1 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 1 | state query calls: 16 | check_time calls: 12 | Actions: 51
Exact-set: matches 58 | mismatches 26 | reward 32
Set micro: TP 50 | FP 1 | FN 31
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 0
Rates: hit 61.7% | late 0.0% | miss 38.3% | false alarm/step 1.2% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 1.2% | cross-day miss 0.0% | update miss 33.3% | precision_hit 98.0% | precision_any 98.0% | exact-set match rate 69.0% | exact-set avg reward 0.381 | set_precision 98.0% | set_recall 61.7% | set_f1 75.8%
Hit rates (by modality): event 69.6% | time 44.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:36:18.093Z |
| Finished (UTC) | 2026-09-14T01:44:05.263Z |
| Duration | 7m 47.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 50 |
| Late | 0 |
| Miss | 31 |
| False alarms | 1 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 1 |
| State query calls | 16 |
| Check_time calls | 12 |
| Actions | 51 |
| Exact-set matches | 58 |
| Exact-set mismatches | 26 |
| Exact-set reward | 32 |
| Set TP | 50 |
| Set FP | 1 |
| Set FN | 31 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| clock | 12 |
| course_portal | 1 |
| price_tracker | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 61.7% |
| Late rate | 0.0% |
| Miss rate | 38.3% |
| False alarm/step | 1.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 1.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 33.3% |
| Precision hit | 98.0% |
| Precision any | 98.0% |
| Exact-set match rate | 69.0% |
| Exact-set avg reward | 0.381 |
| Set precision | 98.0% |
| Set recall | 61.7% |
| Set F1 | 75.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 56 | 69.6% |
| Time (time + time_check) | 11 | 25 | 44.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 11 | 0 | 30 | 41 | 26.8% | 26.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 11 | 0 | 14 | 25 | 44.0% | 44.0% |
| course_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 80.0% | 50.0% | 100.0% | 40.0% | 84.6% | 0.692 | 100.0% | 66.7% | 80.0% |
| Tuesday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 75.0% | 50.0% | 100.0% | 33.3% | 72.7% | 0.455 | 100.0% | 66.7% | 80.0% |
| Wednesday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 7.1% | 7.1% | 60.0% | 25.0% | 75.0% | 20.0% | 71.4% | 0.429 | 80.0% | 44.4% | 57.1% |
| Thursday | 10 | 0 | 6 | 62.5% | 0.0% | 37.5% | 0.0% | 0.0% | 76.9% | 0.0% | 100.0% | 0.0% | 50.0% | 0.000 | 100.0% | 62.5% | 76.9% |
| Friday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 0.0% | 0.0% | 62.5% | 33.3% | 100.0% | 16.7% | 66.7% | 0.333 | 100.0% | 54.5% | 70.6% |
| Saturday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 62.5% | 75.0% | 100.0% | 42.9% | 66.7% | 0.333 | 100.0% | 66.7% | 80.0% |
| Sunday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 66.7% | 66.7% | 100.0% | 33.3% | 66.7% | 0.333 | 100.0% | 66.7% | 80.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 2 |
| Tuesday | clock | 2 |
| Wednesday | appointment_portal | 1 |
| Wednesday | clock | 2 |
| Thursday | price_tracker | 1 |
| Friday | clock | 2 |
| Friday | course_portal | 1 |
| Friday | price_tracker | 1 |
| Saturday | clock | 2 |
| Sunday | clock | 2 |
