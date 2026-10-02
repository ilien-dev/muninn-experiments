# PM-Bench score report

## Summary

Hit: 53 | Late: 0 | Miss: 28 | False alarms: 10 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 35 | check_time calls: 26 | Actions: 63
Exact-set: matches 54 | mismatches 30 | reward 24
Set micro: TP 53 | FP 10 | FN 28
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 65.4% | late 0.0% | miss 34.6% | false alarm/step 11.9% | commission 0.0% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 9.5% | cross-day miss 14.3% | update miss 11.1% | precision_hit 84.1% | precision_any 84.1% | exact-set match rate 64.3% | exact-set avg reward 0.286 | set_precision 84.1% | set_recall 65.4% | set_f1 73.6%
Hit rates (by modality): event 67.9% | time 60.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:32:19.699Z |
| Finished (UTC) | 2026-09-14T01:39:05.856Z |
| Duration | 6m 46.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 53 |
| Late | 0 |
| Miss | 28 |
| False alarms | 10 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 35 |
| Check_time calls | 26 |
| Actions | 63 |
| Exact-set matches | 54 |
| Exact-set mismatches | 30 |
| Exact-set reward | 24 |
| Set TP | 53 |
| Set FP | 10 |
| Set FN | 28 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 1 |
| calendar | 1 |
| clock | 26 |
| course_portal | 1 |
| laundry_status | 1 |
| library_hold | 1 |
| price_tracker | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 65.4% |
| Late rate | 0.0% |
| Miss rate | 34.6% |
| False alarm/step | 11.9% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 9.5% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 11.1% |
| Precision hit | 84.1% |
| Precision any | 84.1% |
| Exact-set match rate | 64.3% |
| Exact-set avg reward | 0.286 |
| Set precision | 84.1% |
| Set recall | 65.4% |
| Set F1 | 73.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 56 | 67.9% |
| Time (time + time_check) | 15 | 25 | 60.0% |

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
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 7.7% | 7.7% | 80.0% | 75.0% | 100.0% | 60.0% | 84.6% | 0.692 | 87.5% | 77.8% | 82.4% |
| Tuesday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 81.8% | 0.636 | 100.0% | 83.3% | 90.9% |
| Wednesday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 28.6% | 21.4% | 60.0% | 25.0% | 75.0% | 20.0% | 57.1% | 0.143 | 50.0% | 44.4% | 47.1% |
| Thursday | 9 | 0 | 7 | 56.2% | 0.0% | 43.8% | 10.0% | 10.0% | 69.2% | 0.0% | 90.0% | 0.0% | 40.0% | -0.200 | 90.0% | 56.2% | 69.2% |
| Friday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 25.0% | 16.7% | 62.5% | 33.3% | 100.0% | 16.7% | 50.0% | 0.000 | 66.7% | 54.5% | 60.0% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 100.0% | 57.1% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 8.3% | 8.3% | 66.7% | 66.7% | 100.0% | 33.3% | 58.3% | 0.167 | 88.9% | 66.7% | 76.2% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 4 |
| Wednesday | appointment_portal | 1 |
| Wednesday | clock | 7 |
| Thursday | clock | 1 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 1 |
| Friday | calendar | 1 |
| Friday | clock | 3 |
| Friday | course_portal | 1 |
| Friday | price_tracker | 1 |
| Saturday | clock | 5 |
| Saturday | price_tracker | 1 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 3 |
| Sunday | library_hold | 1 |
