# PM-Bench score report

## Summary

Hit: 56 | Late: 1 | Miss: 14 | False alarms: 4 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 28 | check_time calls: 24 | Actions: 61
Exact-set: matches 67 | mismatches 16 | reward 51
Set micro: TP 56 | FP 5 | FN 15
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 1
Rates: hit 78.9% | late 1.4% | miss 19.7% | false alarm/step 4.8% | commission 0.0% | wrong-content 4.2% | dependency/step 0.0% | overkill/step 3.6% | cross-day miss 14.3% | update miss 22.2% | precision_hit 91.8% | precision_any 93.4% | exact-set match rate 80.7% | exact-set avg reward 0.614 | set_precision 91.8% | set_recall 78.9% | set_f1 84.8%
Hit rates (by modality): event 79.2% | time 78.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:25:29.101Z |
| Finished (UTC) | 2026-09-14T01:31:19.860Z |
| Duration | 5m 50.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 1 |
| Miss | 14 |
| False alarms | 4 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 28 |
| Check_time calls | 24 |
| Actions | 61 |
| Exact-set matches | 67 |
| Exact-set mismatches | 16 |
| Exact-set reward | 51 |
| Set TP | 56 |
| Set FP | 5 |
| Set FN | 15 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 24 |
| email | 1 |
| price_tracker | 1 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 78.9% |
| Late rate | 1.4% |
| Miss rate | 19.7% |
| False alarm/step | 4.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.2% |
| Dependency/step | 0.0% |
| Overkill/step | 3.6% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 22.2% |
| Precision hit | 91.8% |
| Precision any | 93.4% |
| Exact-set match rate | 80.7% |
| Exact-set avg reward | 0.614 |
| Set precision | 91.8% |
| Set recall | 78.9% |
| Set F1 | 84.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 48 | 79.2% |
| Time (time + time_check) | 18 | 23 | 78.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 2 | 40 | 95.0% | 95.0% |
| proactive_monitoring_required | 18 | 1 | 12 | 31 | 58.1% | 61.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 18 | 1 | 4 | 23 | 78.3% | 82.6% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| reservation_waitlist | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 8.3% | 8.3% | 83.3% | 50.0% | 100.0% | 40.0% | 75.0% | 0.500 | 87.5% | 70.0% | 77.8% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 7.1% | 7.1% | 75.0% | 66.7% | 85.7% | 50.0% | 71.4% | 0.429 | 80.0% | 72.7% | 76.2% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 66.7% | 100.0% | 80.0% | 75.0% | 91.7% | 0.833 | 100.0% | 77.8% | 87.5% |
| Thursday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 0.0% | 75.0% | 66.7% | 100.0% | 40.0% | 75.0% | 0.500 | 88.9% | 72.7% | 80.0% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Sunday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 9.1% | 9.1% | 87.5% | 75.0% | 100.0% | 60.0% | 72.7% | 0.455 | 90.9% | 83.3% | 87.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 4 |
| Tuesday | email | 1 |
| Wednesday | clock | 3 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 4 |
| Friday | clock | 3 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 4 |
