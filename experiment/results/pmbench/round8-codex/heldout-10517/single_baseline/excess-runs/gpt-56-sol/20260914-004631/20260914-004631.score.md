# PM-Bench score report

## Summary

Hit: 61 | Late: 1 | Miss: 9 | False alarms: 7 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 5 | state query calls: 52 | check_time calls: 29 | Actions: 69
Exact-set: matches 68 | mismatches 15 | reward 53
Set micro: TP 61 | FP 8 | FN 10
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 85.9% | late 1.4% | miss 12.7% | false alarm/step 8.4% | commission 0.0% | wrong-content 5.6% | dependency/step 0.0% | overkill/step 6.0% | cross-day miss 0.0% | update miss 0.0% | precision_hit 88.4% | precision_any 89.9% | exact-set match rate 81.9% | exact-set avg reward 0.639 | set_precision 88.4% | set_recall 85.9% | set_f1 87.1%
Hit rates (by modality): event 87.5% | time 82.6%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:46:31.051Z |
| Finished (UTC) | 2026-09-14T06:56:50.511Z |
| Duration | 10m 19.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 1 |
| Miss | 9 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 5 |
| State query calls | 52 |
| Check_time calls | 29 |
| Actions | 69 |
| Exact-set matches | 68 |
| Exact-set mismatches | 15 |
| Exact-set reward | 53 |
| Set TP | 61 |
| Set FP | 8 |
| Set FN | 10 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 4 |
| clock | 29 |
| email | 5 |
| laundry_status | 1 |
| price_tracker | 3 |
| reservation_waitlist | 3 |
| shipment_status | 6 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 85.9% |
| Late rate | 1.4% |
| Miss rate | 12.7% |
| False alarm/step | 8.4% |
| Commission rate | 0.0% |
| Wrong-content rate | 5.6% |
| Dependency/step | 0.0% |
| Overkill/step | 6.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 88.4% |
| Precision any | 89.9% |
| Exact-set match rate | 81.9% |
| Exact-set avg reward | 0.639 |
| Set precision | 88.4% |
| Set recall | 85.9% |
| Set F1 | 87.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 48 | 87.5% |
| Time (time + time_check) | 19 | 23 | 82.6% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 22 | 1 | 8 | 31 | 71.0% | 74.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 19 | 1 | 3 | 23 | 82.6% | 87.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 1 | 90.0% | 0.0% | 10.0% | 8.3% | 8.3% | 83.3% | 100.0% | 100.0% | 80.0% | 83.3% | 0.667 | 90.0% | 90.0% | 90.0% |
| Tuesday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 14.3% | 0.0% | 75.0% | 66.7% | 85.7% | 50.0% | 78.6% | 0.571 | 80.0% | 72.7% | 76.2% |
| Wednesday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 91.7% | 0.833 | 100.0% | 88.9% | 94.1% |
| Thursday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 83.3% | 100.0% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Friday | 10 | 0 | 1 | 90.9% | 0.0% | 9.1% | 8.3% | 8.3% | 87.5% | 100.0% | 100.0% | 80.0% | 83.3% | 0.667 | 90.9% | 90.9% | 90.9% |
| Saturday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 18.2% | 9.1% | 100.0% | 33.3% | 100.0% | 50.0% | 72.7% | 0.455 | 77.8% | 77.8% | 77.8% |
| Sunday | 11 | 1 | 0 | 91.7% | 8.3% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 6 |
| Monday | reservation_waitlist | 1 |
| Tuesday | bank_balance | 4 |
| Tuesday | clock | 3 |
| Tuesday | email | 3 |
| Wednesday | clock | 4 |
| Wednesday | shipment_status | 6 |
| Thursday | clock | 5 |
| Thursday | email | 2 |
| Friday | appointment_portal | 1 |
| Friday | clock | 3 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 3 |
| Sunday | clock | 5 |
| Sunday | reservation_waitlist | 2 |
