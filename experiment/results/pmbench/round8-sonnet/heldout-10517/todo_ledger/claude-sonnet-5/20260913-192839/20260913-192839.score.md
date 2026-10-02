# PM-Bench score report

## Summary

Hit: 53 | Late: 1 | Miss: 17 | False alarms: 2 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 23 | check_time calls: 20 | Actions: 56
Exact-set: matches 63 | mismatches 20 | reward 43
Set micro: TP 53 | FP 3 | FN 18
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 1
Rates: hit 74.6% | late 1.4% | miss 23.9% | false alarm/step 2.4% | commission 0.0% | wrong-content 1.4% | dependency/step 0.0% | overkill/step 2.4% | cross-day miss 0.0% | update miss 22.2% | precision_hit 94.6% | precision_any 96.4% | exact-set match rate 75.9% | exact-set avg reward 0.518 | set_precision 94.6% | set_recall 74.6% | set_f1 83.5%
Hit rates (by modality): event 81.2% | time 60.9%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:28:39.318Z |
| Finished (UTC) | 2026-09-14T01:36:16.577Z |
| Duration | 7m 37.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 53 |
| Late | 1 |
| Miss | 17 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 23 |
| Check_time calls | 20 |
| Actions | 56 |
| Exact-set matches | 63 |
| Exact-set mismatches | 20 |
| Exact-set reward | 43 |
| Set TP | 53 |
| Set FP | 3 |
| Set FN | 18 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 20 |
| price_tracker | 1 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 74.6% |
| Late rate | 1.4% |
| Miss rate | 23.9% |
| False alarm/step | 2.4% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.4% |
| Dependency/step | 0.0% |
| Overkill/step | 2.4% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 94.6% |
| Precision any | 96.4% |
| Exact-set match rate | 75.9% |
| Exact-set avg reward | 0.518 |
| Set precision | 94.6% |
| Set recall | 74.6% |
| Set F1 | 83.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 48 | 81.2% |
| Time (time + time_check) | 14 | 23 | 60.9% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 14 | 1 | 16 | 31 | 45.2% | 48.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 14 | 1 | 8 | 23 | 60.9% | 65.2% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| reservation_waitlist | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 8.3% | 8.3% | 83.3% | 75.0% | 100.0% | 60.0% | 75.0% | 0.500 | 88.9% | 80.0% | 84.2% |
| Tuesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 7.1% | 7.1% | 75.0% | 33.3% | 85.7% | 25.0% | 64.3% | 0.286 | 77.8% | 63.6% | 70.0% |
| Wednesday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 91.7% | 0.833 | 100.0% | 88.9% | 94.1% |
| Thursday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 83.3% | 66.7% | 100.0% | 50.0% | 81.8% | 0.636 | 100.0% | 77.8% | 87.5% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 0.0% | 0.0% | 75.0% | 66.7% | 100.0% | 40.0% | 75.0% | 0.500 | 100.0% | 72.7% | 84.2% |
| Saturday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 83.3% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 100.0% | 66.7% | 80.0% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 87.5% | 50.0% | 100.0% | 40.0% | 72.7% | 0.455 | 100.0% | 75.0% | 85.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 4 |
| Wednesday | clock | 3 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 3 |
| Friday | clock | 2 |
| Saturday | clock | 2 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 3 |
