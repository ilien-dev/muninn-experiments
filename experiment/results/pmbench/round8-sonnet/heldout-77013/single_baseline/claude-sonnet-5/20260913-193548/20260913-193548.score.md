# PM-Bench score report

## Summary

Hit: 57 | Late: 0 | Miss: 24 | False alarms: 8 | Commission: 0 | Wrong-content: 0 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 34 | check_time calls: 26 | Actions: 65
Exact-set: matches 57 | mismatches 27 | reward 30
Set micro: TP 57 | FP 8 | FN 24
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 0
Rates: hit 70.4% | late 0.0% | miss 29.6% | false alarm/step 9.5% | commission 0.0% | wrong-content 0.0% | dependency/step 0.0% | overkill/step 8.3% | cross-day miss 0.0% | update miss 22.2% | precision_hit 87.7% | precision_any 87.7% | exact-set match rate 67.9% | exact-set avg reward 0.357 | set_precision 87.7% | set_recall 70.4% | set_f1 78.1%
Hit rates (by modality): event 71.4% | time 68.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:35:48.191Z |
| Finished (UTC) | 2026-09-14T01:42:09.805Z |
| Duration | 6m 21.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 57 |
| Late | 0 |
| Miss | 24 |
| False alarms | 8 |
| Commission | 0 |
| Wrong-content | 0 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 34 |
| Check_time calls | 26 |
| Actions | 65 |
| Exact-set matches | 57 |
| Exact-set mismatches | 27 |
| Exact-set reward | 30 |
| Set TP | 57 |
| Set FP | 8 |
| Set FN | 24 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| calendar | 1 |
| clock | 26 |
| course_portal | 2 |
| library_hold | 1 |
| price_tracker | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 70.4% |
| Late rate | 0.0% |
| Miss rate | 29.6% |
| False alarm/step | 9.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 0.0% |
| Dependency/step | 0.0% |
| Overkill/step | 8.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 87.7% |
| Precision any | 87.7% |
| Exact-set match rate | 67.9% |
| Exact-set avg reward | 0.357 |
| Set precision | 87.7% |
| Set recall | 70.4% |
| Set F1 | 78.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 56 | 71.4% |
| Time (time + time_check) | 17 | 25 | 68.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 18 | 0 | 23 | 41 | 43.9% | 43.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 17 | 0 | 8 | 25 | 68.0% | 68.0% |
| course_portal | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 7.7% | 7.7% | 80.0% | 75.0% | 100.0% | 60.0% | 84.6% | 0.692 | 87.5% | 77.8% | 82.4% |
| Tuesday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 75.0% | 75.0% | 100.0% | 50.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 7.1% | 7.1% | 60.0% | 100.0% | 75.0% | 80.0% | 78.6% | 0.571 | 87.5% | 77.8% | 82.4% |
| Thursday | 10 | 0 | 6 | 62.5% | 0.0% | 37.5% | 10.0% | 10.0% | 76.9% | 0.0% | 100.0% | 0.0% | 40.0% | -0.200 | 90.9% | 62.5% | 74.1% |
| Friday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 25.0% | 16.7% | 75.0% | 33.3% | 100.0% | 33.3% | 58.3% | 0.167 | 70.0% | 63.6% | 66.7% |
| Saturday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 8.3% | 8.3% | 62.5% | 75.0% | 100.0% | 42.9% | 58.3% | 0.167 | 88.9% | 66.7% | 76.2% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 8.3% | 8.3% | 66.7% | 100.0% | 100.0% | 50.0% | 66.7% | 0.333 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 3 |
| Wednesday | appointment_portal | 1 |
| Wednesday | clock | 7 |
| Thursday | clock | 2 |
| Thursday | price_tracker | 1 |
| Friday | calendar | 1 |
| Friday | clock | 3 |
| Friday | course_portal | 2 |
| Friday | price_tracker | 1 |
| Saturday | clock | 5 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 3 |
| Sunday | library_hold | 1 |
