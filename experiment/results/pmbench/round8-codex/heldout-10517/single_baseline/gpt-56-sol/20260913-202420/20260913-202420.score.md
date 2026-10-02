# PM-Bench score report

## Summary

Hit: 60 | Late: 3 | Miss: 8 | False alarms: 6 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 56 | check_time calls: 35 | Actions: 69
Exact-set: matches 65 | mismatches 18 | reward 47
Set micro: TP 60 | FP 9 | FN 11
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 84.5% | late 4.2% | miss 11.3% | false alarm/step 7.2% | commission 0.0% | wrong-content 5.6% | dependency/step 0.0% | overkill/step 8.4% | cross-day miss 0.0% | update miss 0.0% | precision_hit 87.0% | precision_any 91.3% | exact-set match rate 78.3% | exact-set avg reward 0.566 | set_precision 87.0% | set_recall 84.5% | set_f1 85.7%
Hit rates (by modality): event 85.4% | time 82.6%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:24:20.566Z |
| Finished (UTC) | 2026-09-14T02:36:55.545Z |
| Duration | 12m 35.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 60 |
| Late | 3 |
| Miss | 8 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 56 |
| Check_time calls | 35 |
| Actions | 69 |
| Exact-set matches | 65 |
| Exact-set mismatches | 18 |
| Exact-set reward | 47 |
| Set TP | 60 |
| Set FP | 9 |
| Set FN | 11 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 2 |
| clock | 35 |
| email | 7 |
| laundry_status | 1 |
| price_tracker | 3 |
| reservation_waitlist | 2 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 84.5% |
| Late rate | 4.2% |
| Miss rate | 11.3% |
| False alarm/step | 7.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 5.6% |
| Dependency/step | 0.0% |
| Overkill/step | 8.4% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 87.0% |
| Precision any | 91.3% |
| Exact-set match rate | 78.3% |
| Exact-set avg reward | 0.566 |
| Set precision | 87.0% |
| Set recall | 84.5% |
| Set F1 | 85.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 48 | 85.4% |
| Time (time + time_check) | 19 | 23 | 82.6% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 21 | 3 | 7 | 31 | 67.7% | 77.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 19 | 2 | 2 | 23 | 82.6% | 91.3% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 8.3% | 8.3% | 83.3% | 100.0% | 100.0% | 80.0% | 83.3% | 0.667 | 90.0% | 90.0% | 90.0% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 7.1% | 7.1% | 75.0% | 66.7% | 85.7% | 50.0% | 71.4% | 0.429 | 80.0% | 72.7% | 76.2% |
| Wednesday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 91.7% | 0.833 | 100.0% | 88.9% | 94.1% |
| Thursday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 83.3% | 100.0% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Friday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 8.3% | 8.3% | 75.0% | 100.0% | 100.0% | 60.0% | 75.0% | 0.500 | 81.8% | 81.8% | 81.8% |
| Saturday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 18.2% | 18.2% | 100.0% | 33.3% | 100.0% | 50.0% | 63.6% | 0.273 | 77.8% | 77.8% | 77.8% |
| Sunday | 11 | 1 | 0 | 91.7% | 8.3% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 7 |
| Monday | email | 2 |
| Tuesday | bank_balance | 2 |
| Tuesday | clock | 6 |
| Tuesday | email | 3 |
| Wednesday | clock | 5 |
| Wednesday | shipment_status | 5 |
| Thursday | clock | 5 |
| Thursday | email | 2 |
| Friday | appointment_portal | 1 |
| Friday | clock | 4 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 3 |
| Sunday | clock | 5 |
| Sunday | reservation_waitlist | 2 |
