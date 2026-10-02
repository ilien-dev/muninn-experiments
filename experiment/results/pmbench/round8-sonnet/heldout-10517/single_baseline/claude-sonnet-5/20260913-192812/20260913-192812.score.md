# PM-Bench score report

## Summary

Hit: 55 | Late: 2 | Miss: 14 | False alarms: 4 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 29 | check_time calls: 25 | Actions: 61
Exact-set: matches 64 | mismatches 19 | reward 45
Set micro: TP 55 | FP 6 | FN 16
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 77.5% | late 2.8% | miss 19.7% | false alarm/step 4.8% | commission 0.0% | wrong-content 4.2% | dependency/step 0.0% | overkill/step 4.8% | cross-day miss 14.3% | update miss 22.2% | precision_hit 90.2% | precision_any 93.4% | exact-set match rate 77.1% | exact-set avg reward 0.542 | set_precision 90.2% | set_recall 77.5% | set_f1 83.3%
Hit rates (by modality): event 79.2% | time 73.9%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:28:12.588Z |
| Finished (UTC) | 2026-09-14T01:33:59.345Z |
| Duration | 5m 46.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 2 |
| Miss | 14 |
| False alarms | 4 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 29 |
| Check_time calls | 25 |
| Actions | 61 |
| Exact-set matches | 64 |
| Exact-set mismatches | 19 |
| Exact-set reward | 45 |
| Set TP | 55 |
| Set FP | 6 |
| Set FN | 16 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 25 |
| price_tracker | 1 |
| reservation_waitlist | 1 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 77.5% |
| Late rate | 2.8% |
| Miss rate | 19.7% |
| False alarm/step | 4.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.2% |
| Dependency/step | 0.0% |
| Overkill/step | 4.8% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 22.2% |
| Precision hit | 90.2% |
| Precision any | 93.4% |
| Exact-set match rate | 77.1% |
| Exact-set avg reward | 0.542 |
| Set precision | 90.2% |
| Set recall | 77.5% |
| Set F1 | 83.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 48 | 79.2% |
| Time (time + time_check) | 17 | 23 | 73.9% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 17 | 2 | 12 | 31 | 54.8% | 61.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 17 | 2 | 4 | 23 | 73.9% | 82.6% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| reservation_waitlist | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 8.3% | 8.3% | 83.3% | 75.0% | 100.0% | 60.0% | 75.0% | 0.500 | 88.9% | 80.0% | 84.2% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 7.1% | 7.1% | 75.0% | 66.7% | 85.7% | 50.0% | 71.4% | 0.429 | 80.0% | 72.7% | 76.2% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 66.7% | 100.0% | 80.0% | 75.0% | 91.7% | 0.833 | 100.0% | 77.8% | 87.5% |
| Thursday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 0.0% | 9.1% | 83.3% | 66.7% | 100.0% | 50.0% | 72.7% | 0.455 | 87.5% | 77.8% | 82.4% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 0.0% | 75.0% | 66.7% | 100.0% | 40.0% | 75.0% | 0.500 | 88.9% | 72.7% | 80.0% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 9.1% | 9.1% | 87.5% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 90.0% | 75.0% | 81.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 4 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 5 |
| Wednesday | clock | 3 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 3 |
| Friday | clock | 4 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 3 |
| Sunday | reservation_waitlist | 1 |
