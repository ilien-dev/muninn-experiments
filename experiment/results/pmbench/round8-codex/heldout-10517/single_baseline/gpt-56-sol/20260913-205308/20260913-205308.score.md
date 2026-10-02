# PM-Bench score report

## Summary

Hit: 59 | Late: 5 | Miss: 7 | False alarms: 7 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 11 | state query calls: 57 | check_time calls: 33 | Actions: 71
Exact-set: matches 60 | mismatches 23 | reward 37
Set micro: TP 59 | FP 12 | FN 12
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 83.1% | late 7.0% | miss 9.9% | false alarm/step 8.4% | commission 0.0% | wrong-content 7.0% | dependency/step 0.0% | overkill/step 13.3% | cross-day miss 0.0% | update miss 11.1% | precision_hit 83.1% | precision_any 90.1% | exact-set match rate 72.3% | exact-set avg reward 0.446 | set_precision 83.1% | set_recall 83.1% | set_f1 83.1%
Hit rates (by modality): event 87.5% | time 73.9%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:53:08.206Z |
| Finished (UTC) | 2026-09-14T03:06:03.536Z |
| Duration | 12m 55.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 5 |
| Miss | 7 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 11 |
| State query calls | 57 |
| Check_time calls | 33 |
| Actions | 71 |
| Exact-set matches | 60 |
| Exact-set mismatches | 23 |
| Exact-set reward | 37 |
| Set TP | 59 |
| Set FP | 12 |
| Set FN | 12 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 2 |
| clock | 33 |
| email | 7 |
| laundry_status | 1 |
| price_tracker | 4 |
| reservation_waitlist | 3 |
| shipment_status | 6 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 83.1% |
| Late rate | 7.0% |
| Miss rate | 9.9% |
| False alarm/step | 8.4% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.0% |
| Dependency/step | 0.0% |
| Overkill/step | 13.3% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 83.1% |
| Precision any | 90.1% |
| Exact-set match rate | 72.3% |
| Exact-set avg reward | 0.446 |
| Set precision | 83.1% |
| Set recall | 83.1% |
| Set F1 | 83.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 42 | 48 | 87.5% |
| Time (time + time_check) | 17 | 23 | 73.9% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 20 | 5 | 6 | 31 | 64.5% | 80.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| clock | 17 | 3 | 3 | 23 | 73.9% | 87.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 1 | 1 | 80.0% | 10.0% | 10.0% | 16.7% | 25.0% | 83.3% | 75.0% | 100.0% | 60.0% | 58.3% | 0.167 | 72.7% | 80.0% | 76.2% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 7.1% | 14.3% | 87.5% | 66.7% | 85.7% | 75.0% | 71.4% | 0.429 | 81.8% | 81.8% | 81.8% |
| Wednesday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 0.0% | 8.3% | 83.3% | 66.7% | 100.0% | 50.0% | 75.0% | 0.500 | 87.5% | 77.8% | 82.4% |
| Thursday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 83.3% | 100.0% | 100.0% | 75.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |
| Friday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 8.3% | 8.3% | 75.0% | 100.0% | 100.0% | 60.0% | 75.0% | 0.500 | 81.8% | 81.8% | 81.8% |
| Saturday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 18.2% | 18.2% | 100.0% | 33.3% | 100.0% | 50.0% | 63.6% | 0.273 | 77.8% | 77.8% | 77.8% |
| Sunday | 11 | 1 | 0 | 91.7% | 8.3% | 0.0% | 0.0% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 91.7% | 91.7% | 91.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 6 |
| Monday | email | 2 |
| Tuesday | bank_balance | 2 |
| Tuesday | clock | 6 |
| Tuesday | email | 3 |
| Wednesday | clock | 4 |
| Wednesday | shipment_status | 6 |
| Thursday | clock | 5 |
| Thursday | email | 2 |
| Friday | appointment_portal | 1 |
| Friday | clock | 4 |
| Friday | laundry_status | 1 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 4 |
| Sunday | clock | 5 |
| Sunday | reservation_waitlist | 3 |
