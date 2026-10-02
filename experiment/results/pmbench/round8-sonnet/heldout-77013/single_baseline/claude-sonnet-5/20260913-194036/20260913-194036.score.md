# PM-Bench score report

## Summary

Hit: 53 | Late: 0 | Miss: 28 | False alarms: 8 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 32 | check_time calls: 23 | Actions: 61
Exact-set: matches 56 | mismatches 28 | reward 28
Set micro: TP 53 | FP 8 | FN 28
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 1
Rates: hit 65.4% | late 0.0% | miss 34.6% | false alarm/step 9.5% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 8.3% | cross-day miss 14.3% | update miss 33.3% | precision_hit 86.9% | precision_any 86.9% | exact-set match rate 66.7% | exact-set avg reward 0.333 | set_precision 86.9% | set_recall 65.4% | set_f1 74.6%
Hit rates (by modality): event 71.4% | time 52.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:40:36.471Z |
| Finished (UTC) | 2026-09-14T01:47:24.231Z |
| Duration | 6m 47.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 53 |
| Late | 0 |
| Miss | 28 |
| False alarms | 8 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 32 |
| Check_time calls | 23 |
| Actions | 61 |
| Exact-set matches | 56 |
| Exact-set mismatches | 28 |
| Exact-set reward | 28 |
| Set TP | 53 |
| Set FP | 8 |
| Set FN | 28 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 1 |
| calendar | 1 |
| clock | 23 |
| course_portal | 2 |
| library_hold | 1 |
| price_tracker | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 65.4% |
| Late rate | 0.0% |
| Miss rate | 34.6% |
| False alarm/step | 9.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 8.3% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 86.9% |
| Precision any | 86.9% |
| Exact-set match rate | 66.7% |
| Exact-set avg reward | 0.333 |
| Set precision | 86.9% |
| Set recall | 65.4% |
| Set F1 | 74.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 56 | 71.4% |
| Time (time + time_check) | 13 | 25 | 52.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 15 | 0 | 26 | 41 | 36.6% | 36.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 13 | 0 | 12 | 25 | 52.0% | 52.0% |
| course_portal | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 92.3% | 0.846 | 100.0% | 77.8% | 87.5% |
| Tuesday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 75.0% | 75.0% | 100.0% | 50.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Wednesday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 14.3% | 14.3% | 60.0% | 25.0% | 75.0% | 20.0% | 64.3% | 0.286 | 66.7% | 44.4% | 53.3% |
| Thursday | 9 | 0 | 7 | 56.2% | 0.0% | 43.8% | 10.0% | 10.0% | 69.2% | 0.0% | 90.0% | 0.0% | 40.0% | -0.200 | 90.0% | 56.2% | 69.2% |
| Friday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 25.0% | 16.7% | 75.0% | 33.3% | 100.0% | 33.3% | 58.3% | 0.167 | 70.0% | 63.6% | 66.7% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 100.0% | 57.1% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 16.7% | 16.7% | 77.8% | 33.3% | 100.0% | 33.3% | 50.0% | 0.000 | 80.0% | 66.7% | 72.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 3 |
| Wednesday | appointment_portal | 1 |
| Wednesday | clock | 5 |
| Thursday | clock | 1 |
| Thursday | price_tracker | 1 |
| Friday | calendar | 1 |
| Friday | clock | 2 |
| Friday | course_portal | 2 |
| Friday | price_tracker | 1 |
| Saturday | clock | 5 |
| Saturday | price_tracker | 1 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |
| Sunday | library_hold | 1 |
