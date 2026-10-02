# PM-Bench score report

## Summary

Hit: 61 | Late: 5 | Miss: 5 | False alarms: 3 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 56 | check_time calls: 38 | Actions: 69
Exact-set: matches 66 | mismatches 17 | reward 49
Set micro: TP 61 | FP 8 | FN 10
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 85.9% | late 7.0% | miss 7.0% | false alarm/step 3.6% | commission 0.0% | wrong-content 4.2% | dependency/step 0.0% | overkill/step 8.4% | cross-day miss 0.0% | update miss 11.1% | precision_hit 88.4% | precision_any 95.7% | exact-set match rate 79.5% | exact-set avg reward 0.590 | set_precision 88.4% | set_recall 85.9% | set_f1 87.1%
Hit rates (by modality): event 87.5% | time 82.6%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:46:45.006Z |
| Finished (UTC) | 2026-09-14T03:06:00.364Z |
| Duration | 19m 15.4s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 5 |
| Miss | 5 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 56 |
| Check_time calls | 38 |
| Actions | 69 |
| Exact-set matches | 66 |
| Exact-set mismatches | 17 |
| Exact-set reward | 49 |
| Set TP | 61 |
| Set FP | 8 |
| Set FN | 10 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 1 |
| clock | 38 |
| email | 5 |
| laundry_status | 1 |
| price_tracker | 3 |
| reservation_waitlist | 3 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 85.9% |
| Late rate | 7.0% |
| Miss rate | 7.0% |
| False alarm/step | 3.6% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.2% |
| Dependency/step | 0.0% |
| Overkill/step | 8.4% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 88.4% |
| Precision any | 95.7% |
| Exact-set match rate | 79.5% |
| Exact-set avg reward | 0.590 |
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
| no_proactive_monitoring | 40 | 0 | 0 | 40 | 100.0% | 100.0% |
| proactive_monitoring_required | 21 | 5 | 5 | 31 | 67.7% | 83.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 19 | 2 | 2 | 23 | 82.6% | 91.3% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 0 | 90.0% | 10.0% | 0.0% | 0.0% | 8.3% | 83.3% | 100.0% | 100.0% | 80.0% | 83.3% | 0.667 | 90.0% | 90.0% | 90.0% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 0.0% | 7.1% | 87.5% | 66.7% | 100.0% | 50.0% | 78.6% | 0.571 | 90.0% | 81.8% | 85.7% |
| Wednesday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 91.7% | 0.833 | 100.0% | 88.9% | 94.1% |
| Thursday | 8 | 1 | 0 | 88.9% | 11.1% | 0.0% | 0.0% | 9.1% | 83.3% | 100.0% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Friday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 8.3% | 8.3% | 75.0% | 100.0% | 100.0% | 60.0% | 75.0% | 0.500 | 81.8% | 81.8% | 81.8% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 100.0% | 66.7% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Sunday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 9.1% | 18.2% | 100.0% | 50.0% | 100.0% | 60.0% | 63.6% | 0.273 | 83.3% | 83.3% | 83.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 9 |
| Monday | email | 1 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 6 |
| Tuesday | email | 3 |
| Wednesday | clock | 4 |
| Wednesday | shipment_status | 4 |
| Thursday | clock | 7 |
| Thursday | email | 1 |
| Friday | appointment_portal | 1 |
| Friday | clock | 4 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 3 |
| Sunday | clock | 5 |
| Sunday | reservation_waitlist | 3 |
