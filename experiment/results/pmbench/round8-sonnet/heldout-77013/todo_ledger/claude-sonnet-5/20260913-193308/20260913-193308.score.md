# PM-Bench score report

## Summary

Hit: 51 | Late: 0 | Miss: 30 | False alarms: 5 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 23 | check_time calls: 20 | Actions: 56
Exact-set: matches 57 | mismatches 27 | reward 30
Set micro: TP 51 | FP 5 | FN 30
Cross-day: hit 4 | late 0 | miss 3 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 0
Rates: hit 63.0% | late 0.0% | miss 37.0% | false alarm/step 6.0% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 4.8% | cross-day miss 42.9% | update miss 33.3% | precision_hit 91.1% | precision_any 91.1% | exact-set match rate 67.9% | exact-set avg reward 0.357 | set_precision 91.1% | set_recall 63.0% | set_f1 74.5%
Hit rates (by modality): event 64.3% | time 60.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:33:08.421Z |
| Finished (UTC) | 2026-09-14T01:40:34.981Z |
| Duration | 7m 26.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 51 |
| Late | 0 |
| Miss | 30 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 23 |
| Check_time calls | 20 |
| Actions | 56 |
| Exact-set matches | 57 |
| Exact-set mismatches | 27 |
| Exact-set reward | 30 |
| Set TP | 51 |
| Set FP | 5 |
| Set FN | 30 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| clock | 20 |
| course_portal | 1 |
| price_tracker | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 63.0% |
| Late rate | 0.0% |
| Miss rate | 37.0% |
| False alarm/step | 6.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 4.8% |
| Cross-day miss rate | 42.9% |
| Update miss rate | 33.3% |
| Precision hit | 91.1% |
| Precision any | 91.1% |
| Exact-set match rate | 67.9% |
| Exact-set avg reward | 0.357 |
| Set precision | 91.1% |
| Set recall | 63.0% |
| Set F1 | 74.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 36 | 56 | 64.3% |
| Time (time + time_check) | 15 | 25 | 60.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 36 | 0 | 4 | 40 | 90.0% | 90.0% |
| proactive_monitoring_required | 15 | 0 | 26 | 41 | 36.6% | 36.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 15 | 0 | 10 | 25 | 60.0% | 60.0% |
| course_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 7.7% | 7.7% | 80.0% | 50.0% | 100.0% | 40.0% | 76.9% | 0.538 | 85.7% | 66.7% | 75.0% |
| Tuesday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 75.0% | 75.0% | 100.0% | 50.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Wednesday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 7.1% | 7.1% | 60.0% | 75.0% | 75.0% | 60.0% | 71.4% | 0.429 | 85.7% | 66.7% | 75.0% |
| Thursday | 8 | 0 | 8 | 50.0% | 0.0% | 50.0% | 10.0% | 0.0% | 61.5% | 0.0% | 80.0% | 0.0% | 50.0% | 0.000 | 88.9% | 50.0% | 64.0% |
| Friday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 0.0% | 0.0% | 62.5% | 33.3% | 100.0% | 16.7% | 66.7% | 0.333 | 100.0% | 54.5% | 70.6% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 8.3% | 8.3% | 62.5% | 100.0% | 100.0% | 57.1% | 66.7% | 0.333 | 90.0% | 75.0% | 81.8% |
| Sunday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 8.3% | 8.3% | 55.6% | 66.7% | 83.3% | 33.3% | 58.3% | 0.167 | 87.5% | 58.3% | 70.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 2 |
| Tuesday | clock | 3 |
| Wednesday | appointment_portal | 1 |
| Wednesday | clock | 5 |
| Thursday | clock | 1 |
| Thursday | price_tracker | 1 |
| Friday | clock | 2 |
| Friday | course_portal | 1 |
| Saturday | clock | 4 |
| Sunday | clock | 3 |
