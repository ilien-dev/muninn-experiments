# PM-Bench score report

## Summary

Hit: 61 | Late: 4 | Miss: 6 | False alarms: 5 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 52 | check_time calls: 33 | Actions: 70
Exact-set: matches 65 | mismatches 18 | reward 47
Set micro: TP 61 | FP 9 | FN 10
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 1 | miss 0 | canceled 2 | total 11 | violations 1
Rates: hit 85.9% | late 5.6% | miss 8.5% | false alarm/step 6.0% | commission 0.0% | wrong-content 4.2% | dependency/step 0.0% | overkill/step 9.6% | cross-day miss 0.0% | update miss 0.0% | precision_hit 87.1% | precision_any 92.9% | exact-set match rate 78.3% | exact-set avg reward 0.566 | set_precision 87.1% | set_recall 85.9% | set_f1 86.5%
Hit rates (by modality): event 87.5% | time 82.6%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T06:49:08.232Z |
| Finished (UTC) | 2026-09-14T06:59:21.025Z |
| Duration | 10m 12.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 4 |
| Miss | 6 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 52 |
| Check_time calls | 33 |
| Actions | 70 |
| Exact-set matches | 65 |
| Exact-set mismatches | 18 |
| Exact-set reward | 47 |
| Set TP | 61 |
| Set FP | 9 |
| Set FN | 10 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 1 |
| clock | 33 |
| email | 5 |
| laundry_status | 1 |
| price_tracker | 3 |
| reservation_waitlist | 3 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 85.9% |
| Late rate | 5.6% |
| Miss rate | 8.5% |
| False alarm/step | 6.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.2% |
| Dependency/step | 0.0% |
| Overkill/step | 9.6% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 87.1% |
| Precision any | 92.9% |
| Exact-set match rate | 78.3% |
| Exact-set avg reward | 0.566 |
| Set precision | 87.1% |
| Set recall | 85.9% |
| Set F1 | 86.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 48 | 87.5% |
| Time (time + time_check) | 19 | 23 | 82.6% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 22 | 4 | 5 | 31 | 71.0% | 83.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 19 | 3 | 1 | 23 | 82.6% | 95.7% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 0 | 90.0% | 10.0% | 0.0% | 8.3% | 16.7% | 83.3% | 100.0% | 100.0% | 80.0% | 75.0% | 0.500 | 81.8% | 90.0% | 85.7% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 7.1% | 7.1% | 75.0% | 66.7% | 85.7% | 50.0% | 71.4% | 0.429 | 80.0% | 72.7% | 76.2% |
| Wednesday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 0.0% | 8.3% | 83.3% | 66.7% | 100.0% | 50.0% | 75.0% | 0.500 | 87.5% | 77.8% | 82.4% |
| Thursday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 83.3% | 100.0% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Friday | 10 | 0 | 1 | 90.9% | 0.0% | 9.1% | 8.3% | 8.3% | 87.5% | 100.0% | 100.0% | 80.0% | 83.3% | 0.667 | 90.9% | 90.9% | 90.9% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 100.0% | 66.7% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Sunday | 11 | 1 | 0 | 91.7% | 8.3% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 7 |
| Monday | email | 1 |
| Monday | reservation_waitlist | 1 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 6 |
| Tuesday | email | 2 |
| Wednesday | clock | 4 |
| Wednesday | shipment_status | 5 |
| Thursday | clock | 5 |
| Thursday | email | 2 |
| Friday | appointment_portal | 1 |
| Friday | clock | 4 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 3 |
| Sunday | clock | 4 |
| Sunday | reservation_waitlist | 2 |
