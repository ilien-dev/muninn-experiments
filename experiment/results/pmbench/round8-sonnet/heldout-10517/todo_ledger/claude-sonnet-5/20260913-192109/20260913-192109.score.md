# PM-Bench score report

## Summary

Hit: 53 | Late: 2 | Miss: 16 | False alarms: 6 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 24 | check_time calls: 22 | Actions: 61
Exact-set: matches 60 | mismatches 23 | reward 37
Set micro: TP 53 | FP 8 | FN 18
Cross-day: hit 5 | late 0 | miss 2 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 74.6% | late 2.8% | miss 22.5% | false alarm/step 7.2% | commission 0.0% | wrong-content 5.6% | dependency/step 0.0% | overkill/step 7.2% | cross-day miss 28.6% | update miss 22.2% | precision_hit 86.9% | precision_any 90.2% | exact-set match rate 72.3% | exact-set avg reward 0.446 | set_precision 86.9% | set_recall 74.6% | set_f1 80.3%
Hit rates (by modality): event 77.1% | time 69.6%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:21:09.887Z |
| Finished (UTC) | 2026-09-14T01:28:37.764Z |
| Duration | 7m 27.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 53 |
| Late | 2 |
| Miss | 16 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 24 |
| Check_time calls | 22 |
| Actions | 61 |
| Exact-set matches | 60 |
| Exact-set mismatches | 23 |
| Exact-set reward | 37 |
| Set TP | 53 |
| Set FP | 8 |
| Set FN | 18 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 22 |
| price_tracker | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 74.6% |
| Late rate | 2.8% |
| Miss rate | 22.5% |
| False alarm/step | 7.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 5.6% |
| Dependency/step | 0.0% |
| Overkill/step | 7.2% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 22.2% |
| Precision hit | 86.9% |
| Precision any | 90.2% |
| Exact-set match rate | 72.3% |
| Exact-set avg reward | 0.446 |
| Set precision | 86.9% |
| Set recall | 74.6% |
| Set F1 | 80.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 37 | 48 | 77.1% |
| Time (time + time_check) | 16 | 23 | 69.6% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 37 | 0 | 3 | 40 | 92.5% | 92.5% |
| proactive_monitoring_required | 16 | 2 | 13 | 31 | 51.6% | 58.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 16 | 2 | 5 | 23 | 69.6% | 78.3% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| reservation_waitlist | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 16.7% | 16.7% | 83.3% | 75.0% | 100.0% | 60.0% | 66.7% | 0.333 | 80.0% | 80.0% | 80.0% |
| Tuesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 14.3% | 14.3% | 75.0% | 33.3% | 85.7% | 25.0% | 57.1% | 0.143 | 70.0% | 63.6% | 66.7% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 66.7% | 100.0% | 80.0% | 75.0% | 91.7% | 0.833 | 100.0% | 77.8% | 87.5% |
| Thursday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 0.0% | 9.1% | 66.7% | 66.7% | 80.0% | 50.0% | 63.6% | 0.273 | 85.7% | 66.7% | 75.0% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 0.0% | 0.0% | 75.0% | 66.7% | 100.0% | 40.0% | 75.0% | 0.500 | 100.0% | 72.7% | 84.2% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 9.1% | 87.5% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 5 |
| Wednesday | clock | 3 |
| Thursday | clock | 3 |
| Friday | clock | 2 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 3 |
