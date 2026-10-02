# PM-Bench score report

## Summary

Hit: 60 | Late: 3 | Miss: 8 | False alarms: 6 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 56 | check_time calls: 37 | Actions: 69
Exact-set: matches 65 | mismatches 18 | reward 47
Set micro: TP 60 | FP 9 | FN 11
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 84.5% | late 4.2% | miss 11.3% | false alarm/step 7.2% | commission 0.0% | wrong-content 7.0% | dependency/step 0.0% | overkill/step 8.4% | cross-day miss 0.0% | update miss 11.1% | precision_hit 87.0% | precision_any 91.3% | exact-set match rate 78.3% | exact-set avg reward 0.566 | set_precision 87.0% | set_recall 84.5% | set_f1 85.7%
Hit rates (by modality): event 85.4% | time 82.6%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:50:56.314Z |
| Finished (UTC) | 2026-09-14T07:05:28.456Z |
| Duration | 14m 32.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 60 |
| Late | 3 |
| Miss | 8 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 56 |
| Check_time calls | 37 |
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
| appointment_portal | 2 |
| bank_balance | 1 |
| clock | 37 |
| email | 6 |
| laundry_status | 1 |
| price_tracker | 3 |
| reservation_waitlist | 1 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 84.5% |
| Late rate | 4.2% |
| Miss rate | 11.3% |
| False alarm/step | 7.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.0% |
| Dependency/step | 0.0% |
| Overkill/step | 8.4% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
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
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 100.0% | 66.7% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Sunday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 9.1% | 18.2% | 100.0% | 50.0% | 100.0% | 60.0% | 63.6% | 0.273 | 83.3% | 83.3% | 83.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 9 |
| Monday | email | 1 |
| Tuesday | appointment_portal | 1 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 5 |
| Tuesday | email | 4 |
| Wednesday | clock | 4 |
| Wednesday | shipment_status | 5 |
| Thursday | clock | 6 |
| Thursday | email | 1 |
| Friday | appointment_portal | 1 |
| Friday | clock | 4 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 3 |
| Sunday | clock | 6 |
| Sunday | reservation_waitlist | 1 |
