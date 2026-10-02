# PM-Bench score report

## Summary

Hit: 62 | Late: 2 | Miss: 7 | False alarms: 6 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 62 | check_time calls: 39 | Actions: 70
Exact-set: matches 68 | mismatches 15 | reward 53
Set micro: TP 62 | FP 8 | FN 9
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 87.3% | late 2.8% | miss 9.9% | false alarm/step 7.2% | commission 0.0% | wrong-content 5.6% | dependency/step 0.0% | overkill/step 7.2% | cross-day miss 0.0% | update miss 0.0% | precision_hit 88.6% | precision_any 91.4% | exact-set match rate 81.9% | exact-set avg reward 0.639 | set_precision 88.6% | set_recall 87.3% | set_f1 87.9%
Hit rates (by modality): event 83.3% | time 95.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:38:33.354Z |
| Finished (UTC) | 2026-09-14T02:53:04.533Z |
| Duration | 14m 31.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 62 |
| Late | 2 |
| Miss | 7 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 62 |
| Check_time calls | 39 |
| Actions | 70 |
| Exact-set matches | 68 |
| Exact-set mismatches | 15 |
| Exact-set reward | 53 |
| Set TP | 62 |
| Set FP | 8 |
| Set FN | 9 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 3 |
| clock | 39 |
| email | 5 |
| laundry_status | 1 |
| price_tracker | 4 |
| reservation_waitlist | 2 |
| shipment_status | 7 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 87.3% |
| Late rate | 2.8% |
| Miss rate | 9.9% |
| False alarm/step | 7.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 5.6% |
| Dependency/step | 0.0% |
| Overkill/step | 7.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 88.6% |
| Precision any | 91.4% |
| Exact-set match rate | 81.9% |
| Exact-set avg reward | 0.639 |
| Set precision | 88.6% |
| Set recall | 87.3% |
| Set F1 | 87.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 48 | 83.3% |
| Time (time + time_check) | 22 | 23 | 95.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 24 | 2 | 5 | 31 | 77.4% | 83.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 22 | 1 | 0 | 23 | 95.7% | 100.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 16.7% | 16.7% | 83.3% | 100.0% | 100.0% | 80.0% | 75.0% | 0.500 | 81.8% | 90.0% | 85.7% |
| Tuesday | 9 | 0 | 2 | 81.8% | 0.0% | 18.2% | 7.1% | 0.0% | 75.0% | 100.0% | 85.7% | 75.0% | 85.7% | 0.714 | 90.0% | 81.8% | 85.7% |
| Wednesday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 91.7% | 0.833 | 100.0% | 88.9% | 94.1% |
| Thursday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 18.2% | 18.2% | 66.7% | 100.0% | 80.0% | 75.0% | 63.6% | 0.273 | 77.8% | 77.8% | 77.8% |
| Friday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 8.3% | 8.3% | 75.0% | 100.0% | 100.0% | 60.0% | 75.0% | 0.500 | 81.8% | 81.8% | 81.8% |
| Saturday | 9 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Sunday | 11 | 1 | 0 | 91.7% | 8.3% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 8 |
| Monday | email | 2 |
| Tuesday | bank_balance | 3 |
| Tuesday | clock | 7 |
| Tuesday | email | 2 |
| Wednesday | clock | 5 |
| Wednesday | shipment_status | 7 |
| Thursday | clock | 7 |
| Thursday | email | 1 |
| Friday | appointment_portal | 1 |
| Friday | clock | 4 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 4 |
| Sunday | clock | 5 |
| Sunday | reservation_waitlist | 2 |
